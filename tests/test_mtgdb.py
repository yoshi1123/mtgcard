# -*- coding: utf-8 -*-

import unittest
from tests import load_tests
load_tests.__module__ = __name__

import sqlite3

from mtgcard.card import Card
from mtgcard import mtgdb
from mtgcard.mtgdb import csv_len, csv_set_contains, manacost_contains
from mtgcard.mtgdb import manacost_to_cmc, csv_element, csv_in
from mtgcard.mtgdb import r_unbraced_char
from mtgcard.mtgdb import collate_exp_core_first
from mtgcard.parser import parser
from mtgcard import util
from mtgcard import settings


class setUpModule():
    global db_mtgjson_sqlite
    db_mtgjson_sqlite = mtgdb.Interface()

class TestMTGDatabaseSQLiteInCSV(unittest.TestCase):

    def test_in(self):
        self.assertTrue(csv_in('a,b,c', 'c'))

    def test_not_in(self):
        self.assertFalse(csv_in('a,b,c', 'd'))

    def test_none_value(self):
        self.assertFalse(csv_in('a,b,c', None))

    def test_none_list(self):
        self.assertFalse(csv_in(None, 'c'))


class TestMTGDatabaseSQLiteCSVElement(unittest.TestCase):

    def test_get_first_element(self):
        text = '''
        Bruna, the Fading Light,Brisela, Voice of Nightmares,Gisela, the Broken Blade
        '''.strip()
        actual_result = csv_element(text, 0)
        expected_result = 'Bruna, the Fading Light'
        self.assertEqual(actual_result, expected_result)

    def test_get_second_element(self):
        text = '''
        Bruna, the Fading Light,Brisela, Voice of Nightmares,Gisela, the Broken Blade
        '''.strip()
        actual_result = csv_element(text, 1)
        expected_result = 'Brisela, Voice of Nightmares'
        self.assertEqual(actual_result, expected_result)


class TestMTGDatabaseSQLiteUnbracedRE(unittest.TestCase):

    def test_letter(self):
        manacost = 'w'
        expected_result = '{w}'
        actual_result = r_unbraced_char.subn(r'{\1}', manacost)[0]
        self.assertEqual(actual_result, expected_result)

    def test_two_letters(self):
        manacost = 'wu'
        expected_result = '{w}{u}'
        actual_result = r_unbraced_char.subn(r'{\1}', manacost)[0]
        self.assertEqual(actual_result, expected_result)

    def test_number(self):
        manacost = '1'
        expected_result = '{1}'
        actual_result = r_unbraced_char.subn(r'{\1}', manacost)[0]
        self.assertEqual(actual_result, expected_result)

    def test_letter_number(self):
        manacost = 'w1'
        expected_result = '{w}{1}'
        actual_result = r_unbraced_char.subn(r'{\1}', manacost)[0]
        self.assertEqual(actual_result, expected_result)


class TestMTGDatabaseSQLiteNoColors(unittest.TestCase):

    def test_none(self):
        colors = None
        expected_result = 0
        actual_result = csv_len(colors)
        self.assertEqual(actual_result, expected_result)

    def test_zero(self):
        colors = ''
        expected_result = 0
        actual_result = csv_len(colors)
        self.assertEqual(actual_result, expected_result)

    def test_one(self):
        colors = 'c'
        expected_result = 1
        actual_result = csv_len(colors)
        self.assertEqual(actual_result, expected_result)

    def test_two(self):
        colors = 'c,u'
        expected_result = 2
        actual_result = csv_len(colors)
        self.assertEqual(actual_result, expected_result)

    def test_same(self):
        colors = 'u,u'
        expected_result = 1
        actual_result = csv_len(colors)
        self.assertEqual(actual_result, expected_result)


class TestMTGDatabaseSQLiteColorSetContains(unittest.TestCase):

    def test_subset(self):
        a = 'w,u'
        b = 'u'
        actual_result = csv_set_contains(a, b)
        self.assertTrue(actual_result)

    def test_subset(self):
        a = 'w,u'
        b = 'u'
        actual_result = csv_set_contains(a, b)
        self.assertTrue(actual_result)

    def test_superset_false(self):
        a = 'u'
        b = 'w,u'
        actual_result = csv_set_contains(a, b)
        self.assertFalse(actual_result)

    def test_none_none(self):
        a = None
        b = None
        actual_result = csv_set_contains(a, b)
        self.assertTrue(actual_result)

    def test_empty_none(self):
        a = ''
        b = None
        actual_result = csv_set_contains(a, b)
        self.assertTrue(actual_result)

    def test_none_empty(self):
        a = None
        b = ''
        actual_result = csv_set_contains(a, b)
        self.assertTrue(actual_result)

    def test_none_not_none(self):
        a = None
        b = 'w'
        actual_result = csv_set_contains(a, b)
        self.assertFalse(actual_result)

    def test_subset_three(self):
        a = 'w,u,b'
        b = 'u,b'
        actual_result = csv_set_contains(a, b)
        self.assertTrue(actual_result)


class TestMTGDatabaseSQLiteManaCostToCMC(unittest.TestCase):

    def test_one(self):
        manacost = '{w}'
        expected_result = 1
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_two_same(self):
        manacost = '{w}{w}'
        expected_result = 2
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_two_same_number(self):
        manacost = '{w}{w}{1}'
        expected_result = 3
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_two_same_number_two(self):
        manacost = '{w}{w}{2}'
        expected_result = 4
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_plain_letter(self):
        manacost = 'w'
        expected_result = 1
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_plain_letter_two(self):
        manacost = 'wu'
        expected_result = 2
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_plain_letter_number(self):
        manacost = 'wu1'
        expected_result = 3
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_mix(self):
        manacost = '{w}u4{u}'
        expected_result = 7
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_empty(self):
        manacost = ''
        expected_result = 0
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_zero_letter(self):
        manacost = '0'
        expected_result = 0
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_one_letter(self):
        manacost = '1'
        expected_result = 1
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_two_letter(self):
        manacost = '2'
        expected_result = 2
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_double_digit(self):
        manacost = '11'
        expected_result = 11
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)


    def test_x_letter(self):
        manacost = 'X'
        expected_result = 0
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_hybrid_mono_color(self):
        manacost = '{2/R}{2/R}{2/R}'
        expected_result = 6
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_phyrexian_mana_symbols(self):
        manacost = '{3}{W/P}{W/P}'
        expected_result = 5
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_snow_mana_symbols(self):
        manacost = '{3}{S}'
        expected_result = 4
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)

    def test_snow_mana_symbols_unbraced(self):
        manacost = '3ss'
        expected_result = 5
        actual_result = manacost_to_cmc(manacost)
        self.assertEqual(actual_result, expected_result)


    def test_no_braces_one(self):
        colors = 'w'
        expected_result = 1
        actual_result = manacost_to_cmc(colors)
        self.assertEqual(actual_result, expected_result)

    def test_no_braces_with_generic(self):
        colors = '2w3'
        expected_result = 6
        actual_result = manacost_to_cmc(colors)
        self.assertEqual(actual_result, expected_result)

    def test_query_manacost_to_cmc_equal_cmc_for_all(self):

        query1 = '''
        SELECT name,manaCost,convertedManaCost,layout FROM cards
        WHERE manacost_to_cmc(manaCost) != convertedManaCost AND
            layout NOT IN
            ('transform','split','flip','aftermath','adventure','meld')
            AND name NOT IN ('Gleemax', 'Little Girl',
            'The Ultimate Nightmare of Wizards of the Coast® Customer Service')
        '''.strip()

        actual_result = db_mtgjson_sqlite.cursor.execute(query1).fetchall()
        expected_result = []
        # print( len(actual_result) )
        # for row in actual_result:
        #     print( list(row) )
        self.assertEqual(actual_result, expected_result)


class TestMTGDatabaseSQLiteManaListContains(unittest.TestCase):

    def setUp(self):
        db_mtgjson_sqlite.cursor.row_factory = None

    def tearDown(self):
        db_mtgjson_sqlite.cursor.row_factory = sqlite3.Row


    def test_sublist(self):
        a = '{w}{u}'
        b = '{w}'
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_numbers(self):
        a = '{w}{u}'
        b = '{1}{w}'
        actual_result = manacost_contains(a, b)
        self.assertFalse(actual_result)

    def test_superlist_false(self):
        a = '{w}'
        b = '{w}{u}'
        actual_result = manacost_contains(a, b)
        self.assertFalse(actual_result)

    def test_empty_b_sublist(self):
        a = '{w}'
        b = ''
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_empty_a_sublist(self):
        a = ''
        b = ''
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_plain(self):
        a = '{w}'
        b = 'w'
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_plain_number(self):
        a = '{w}{1}'
        b = 'w1'
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_plain_two_colors(self):
        a = '{w}{1}{u}'
        b = 'wu'
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_none_none(self):
        a = None
        b = None
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_empty_none(self):
        a = ''
        b = None
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_none_empty(self):
        a = None
        b = ''
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_2_generic_or_1_color(self):
        # {r}, {2}
        a = '{2/r}'
        self.assertFalse(manacost_contains(a, '2'))
        self.assertFalse(manacost_contains(a, '3')) # numbers do not count
        self.assertFalse(manacost_contains(a, 'r'))
        self.assertFalse(manacost_contains(a, 'rr'))
        self.assertTrue(manacost_contains(a, '{2/r}'))

    def test_6_generic_or_3_color(self):
        # {r}{r}{r}, {2}{r}{r}, {4}{r}, {6}
        a = '{2/r}{2/r}{2/r}'
        self.assertFalse(manacost_contains(a, '2'))
        self.assertFalse(manacost_contains(a, 'r'))
        self.assertFalse(manacost_contains(a, 'rr'))
        self.assertFalse(manacost_contains(a, 'rrr'))
        self.assertFalse(manacost_contains(a, 'rrrr'))
        self.assertTrue(manacost_contains(a, '{2/r}'))
        self.assertTrue(manacost_contains(a, '{2/r}{2/r}'))
        self.assertTrue(manacost_contains(a, '{2/r}{2/r}{2/r}'))
        self.assertFalse(manacost_contains(a, '{2/r}{2/r}{2/r}{2/r}'))

    def test_a_generic(self):
        a = '2r'
        b = '1r'
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_b_generic(self):
        a = '3r'
        b = '2r'
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)

    def test_separate_generic(self):
        a = '1r1'
        b = '2r'
        actual_result = manacost_contains(a, b)
        self.assertTrue(actual_result)


class TestMTGDatabaseGetCards(unittest.TestCase):

    ###################
    #  return errors  #
    ###################

    # def test010_six_cards(self):
    #     expected_result = ['Aether Shockwave', 'Barbed Shocker', 'Shock',
    #                        'Shock Troops', 'Shockmaw Dragon', 'Sudden Shock']
    #     cards = db_mtgjson_sqlite.get_cards("Shock", format="modern",
    #                                        case_sensitive=True)
    #
    #     self.assertEqual(cards[0].name, 'Aether Shockwave')
    #     self.assertEqual(cards[1].name, 'Barbed Shocker')
    #     self.assertEqual(cards[2].name, 'Shock')
    #     self.assertEqual(cards[3].name, 'Shock Troops')
    #     self.assertEqual(cards[4].name, 'Shockmaw Dragon')
    #     self.assertEqual(cards[5].name, 'Sudden Shock')
    #
    # def test020_core_exp_by_release_date_set_select(self):
    #     cards = db_mtgjson_sqlite.get_cards("", format="modern", case_sensitive=False)
    #     for c in cards:
    #         pr_in_main = set(c.printings.split(',')).intersection(settings.main_sets)
    #         if len(pr_in_main) >= 1:
    #             expected_result = util.get_newest_exp_or_core_set(c.printings.split(','))
    #             self.assertEqual(c.setcode, expected_result)

    def test_one_card(self):
        cards = db_mtgjson_sqlite.get_cards(parser.parse("!Shock"))
        self.assertEqual(cards[0].name, 'Shock')
        self.assertEqual(len(cards), 1)

    def test_partial_name(self):
        cards = db_mtgjson_sqlite.get_cards(parser.parse("Shock"))
        self.assertEqual(cards[0].name, 'Aether Shockwave')
        self.assertEqual(cards[1].name, 'Aftershock')
        self.assertEqual(cards[2].name, 'Barbed Shocker')
        self.assertEqual(cards[3].name, 'Rumbling Aftershocks')
        self.assertEqual(cards[4].name, 'Shock')
        self.assertEqual(cards[5].name, 'Shock Troops')
        self.assertEqual(cards[6].name, 'Shocker')
        self.assertEqual(cards[7].name, 'Shockmaw Dragon')
        self.assertEqual(cards[8].name, 'Spellshock')
        self.assertEqual(cards[9].name, 'Staggershock')
        self.assertEqual(cards[10].name, 'Stoneshock Giant')
        self.assertEqual(cards[11].name, 'Sudden Shock')

    def test_partial_name_modern(self):
        cards = db_mtgjson_sqlite.get_cards(parser.parse("Shock f:modern"))
        self.assertEqual(cards[0].name, 'Aether Shockwave')
        self.assertEqual(cards[1].name, 'Barbed Shocker')
        self.assertEqual(cards[2].name, 'Rumbling Aftershocks')
        self.assertEqual(cards[3].name, 'Shock')
        self.assertEqual(cards[4].name, 'Shock Troops')
        self.assertEqual(cards[5].name, 'Shockmaw Dragon')
        self.assertEqual(cards[6].name, 'Staggershock')
        self.assertEqual(cards[7].name, 'Stoneshock Giant')
        self.assertEqual(cards[8].name, 'Sudden Shock')

    def test_no_adventure_cards(self):
        cards = db_mtgjson_sqlite.get_cards(parser.parse("!'Boulder Rush'"))
        self.assertEqual(cards[0].name, 'Rimrock Knight')

    def test_no_duplicates_adventurers(self):
        cards = db_mtgjson_sqlite.get_cards(
                parser.parse("!'Boulder Rush' or 'Rimrock Knight'"))
        self.assertEqual(len(cards), 1)

    def test_limit(self):
        cards = db_mtgjson_sqlite.get_cards(parser.parse("set:m20"), limit=10)
        self.assertEqual(len(cards), 10)


class TestMTGDatabaseGetCard(unittest.TestCase):

    ###################
    #  return errors  #
    ###################

    def test_get_types(self):
        expected_result = "Instant"
        actual_result = db_mtgjson_sqlite.get_card("Shock", "m20").type
        self.assertEqual(actual_result, expected_result)

    def test_get_another_type(self):
        expected_result = "Sorcery"
        actual_result = db_mtgjson_sqlite.get_card("Rabid Bite", "M20").type
        self.assertEqual(actual_result, expected_result)

    def test_get_whole_card(self):
        c = db_mtgjson_sqlite.get_card("Rabid Bite", "M20") # type: Card
        self.assertEqual(c.type, "Sorcery")
        self.assertEqual(c.manacost  , "1G")
        self.assertEqual(c.power      , None)
        self.assertEqual(c.toughness  , None)
        self.assertEqual(c.rarity     , "common")
        self.assertEqual(c.text       , "Target creature you control deals damage equal to its power to target creature you don't control.")

    def test_modern(self):
        c = db_mtgjson_sqlite.get_card("Shivan Dragon", format="modern")
        self.assertEqual(c.type, "Creature — Dragon")
        self.assertEqual(c.manacost  , "4RR")
        self.assertEqual(c.power      , "5")
        self.assertEqual(c.toughness  , "5")
        self.assertEqual(c.text       , "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn.")

    def test_modern_case_insensitive(self):
        c = db_mtgjson_sqlite.get_card("shivan dragon", "M20")
        self.assertEqual(c.type, "Creature — Dragon")
        self.assertEqual(c.manacost  , "4RR")
        self.assertEqual(c.power      , "5")
        self.assertEqual(c.toughness  , "5")
        self.assertEqual(c.text       , "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn.")

    def test_modern_case_insensitive(self):
        c = db_mtgjson_sqlite.get_card("shivan dragon", format="modern")
        self.assertEqual(c.type, "Creature — Dragon")
        self.assertEqual(c.manacost  , "4RR")
        self.assertEqual(c.power      , "5")
        self.assertEqual(c.toughness  , "5")
        self.assertEqual(c.text       , "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn.")

    def test_modern_setcode(self):
        c = db_mtgjson_sqlite.get_card("Shock", format="modern")
        self.assertEqual(c.type, "Instant")
        self.assertEqual(c.manacost  , "R")
        self.assertEqual(c.power      , None)
        self.assertEqual(c.toughness  , None)
        self.assertEqual(c.text       , "Shock deals 2 damage to any target.")
        self.assertEqual(c.setcode    , "M20")

    def test_modern_rarity(self):
        c = db_mtgjson_sqlite.get_card("Rabid Bite", format="modern")
        self.assertEqual(c.type, "Sorcery")
        self.assertEqual(c.manacost  , "1G")
        self.assertEqual(c.power      , None)
        self.assertEqual(c.toughness  , None)
        self.assertEqual(c.rarity     , "common")
        self.assertEqual(c.text       , "Target creature you control deals damage equal to its power to target creature you don't control.")

    def test_modern_rarity(self):
        c = db_mtgjson_sqlite.get_card("Serra Angel", format="modern")
        self.assertEqual(c.rarity     , "uncommon")

    def test_cmc(self):
        c = db_mtgjson_sqlite.get_card("Shock", format="modern")
        self.assertEqual(c.cmc, 1)


    def test_planeswalker(self):
        c = db_mtgjson_sqlite.get_card("Chandra, Torch of Defiance", format="modern")
        self.assertEqual(c.type, "Legendary Planeswalker — Chandra")
        self.assertEqual(c.manacost  , "2RR")
        self.assertEqual(c.power      , None)
        self.assertEqual(c.toughness  , None)
        self.assertEqual(c.rarity     , "mythic")
        self.assertEqual(c.text       , "[+1]: Exile the top card of your library. You may cast that card. If you don't, Chandra, Torch of Defiance deals 2 damage to each opponent.\n[+1]: Add {R}{R}.\n[−3]: Chandra, Torch of Defiance deals 4 damage to target creature.\n[−7]: You get an emblem with \"Whenever you cast a spell, this emblem deals 5 damage to any target.\"")
        self.assertEqual(c.setcode    , "KLD")
        self.assertEqual(c.loyalty    , "4")

    def test_rulings(self):
        text = "If an instant or sorcery spell has an adamant ability, you perform the spell\u2019s instructions in order. You don\u2019t perform the adamant instruction before the spell resolves or before any other effects printed above it."
        c = db_mtgjson_sqlite.get_card("Slaying Fire", "ELD", rulings=True)
        self.assertEqual(c.rulings[0]['text'], text)

    def test_rulings_no_verbose(self):
        # rulings and price should be None unless verbose is specified
        c = db_mtgjson_sqlite.get_card("Slaying Fire", "ELD", verbose=False)
        self.assertEqual(c.rulings, None)

    def test_price(self):
        c = db_mtgjson_sqlite.get_card("Rimrock Knight", "ELD", verbose=True)
        self.assertEqual(type(c.price), float)

    def test_price_none(self):
        c = db_mtgjson_sqlite.get_card("Boulder Rush", "ELD", verbose=True)
        self.assertEqual(c.price, None)

    def test_price_none_no_verbose(self):
        c = db_mtgjson_sqlite.get_card("Boulder Rush", "ELD",
                verbose=False)
        self.assertEqual(c.price, None)

    def test_price_date_none(self):
        c = db_mtgjson_sqlite.get_card("Boulder Rush", "ELD", verbose=True)
        self.assertEqual(c.price_date, None)

    def test_printings(self):
        c = db_mtgjson_sqlite.get_card("Serra Angel", "M15")
        self.assertTrue(c.printings is not None)

    def test_variable_power_toughness(self):
        c = db_mtgjson_sqlite.get_card("Abominable Treefolk", "MH1", verbose=True)
        self.assertEqual(c.name, "Abominable Treefolk")

    def test_uuid(self):
        c = db_mtgjson_sqlite.get_card("Rimrock Knight", "ELD")
        self.assertEqual(c.uuid, "be678625-f685-54be-9d21-f0337c6c4580")

    def test_formats(self):
        # NOTE: liable to change
        card = db_mtgjson_sqlite.get_card("Serra Angel", "M15", verbose=True)
        self.assertEqual(card.formats,
                {'commander': 'Legal', 'duel': 'Legal',
                 'historic': 'Legal', 'legacy': 'Legal',
                 'modern': 'Legal', 'penny': 'Legal',
                 'pioneer': 'Legal', 'vintage': 'Legal'})

    def test_formats_verbose_false(self):
        # NOTE: liable to change
        card = db_mtgjson_sqlite.get_card("Serra Angel", "M15", verbose=False)
        self.assertEqual(card.formats, None)


    def test_colors(self):
        c = db_mtgjson_sqlite.get_card("Shock", format="modern")
        self.assertEqual(c.colors[0], "R")


    ##################
    #  value errors  #
    ##################

    def test_empty_name(self):
        self.assertRaises(ValueError, db_mtgjson_sqlite.get_card, "", "m20")

    def test_unknown_set(self):
        self.assertRaises(ValueError, db_mtgjson_sqlite.get_card, "Shock", "abc")

    def test_unknown_name(self):
        self.assertRaises(ValueError, db_mtgjson_sqlite.get_card, "Pikachu",
                format="modern")


class TestMTGDatabaseGetCardAndCards(unittest.TestCase):

    def test_Card_from_both_have_same_number_of_attributes_not_none(self):
        card = db_mtgjson_sqlite.get_card("Serra Angel", "M15",
                verbose=False)
        cards = db_mtgjson_sqlite.get_cards(parser.parse("!'Serra Angel' set:m15"))
        cards[0].price = None
        cards[0].price_date = None
        cards[0].formats = None
        no_card_attrs = len( list( filter(None, vars(card).values()) ) )
        no_cards_attrs = len( list( filter(None, vars(cards[0]).values()) ) )
        self.assertEqual(no_card_attrs, no_cards_attrs)

    def test_layout(self):
        card = db_mtgjson_sqlite.get_card("Rimrock Knight", "ELD")
        cards = db_mtgjson_sqlite.get_cards(parser.parse("!'Rimrock Knight'"))
        self.assertEqual(card.layout, "adventure")
        self.assertEqual(cards[0].layout, "adventure")

    def test_names(self):
        card = db_mtgjson_sqlite.get_card("Rimrock Knight", "ELD")
        cards = db_mtgjson_sqlite.get_cards(parser.parse("!'Rimrock Knight'"))
        self.assertEqual(card.names, ["Rimrock Knight", "Boulder Rush"])
        self.assertEqual(cards[0].names, ["Rimrock Knight", "Boulder Rush"])


class TestMTGDatabaseGetRulings(unittest.TestCase):

    def test_has_rulings(self):
        text = "If an instant or sorcery spell has an adamant ability, you perform the spell\u2019s instructions in order. You don\u2019t perform the adamant instruction before the spell resolves or before any other effects printed above it."
        rulings = db_mtgjson_sqlite.get_rulings(
                db_mtgjson_sqlite.get_card("Slaying Fire", "ELD").uuid)
        self.assertTrue(rulings)
        self.assertEqual(len(rulings), 4)
        self.assertEqual(text, rulings[0]['text'])

    def test_has_no_rulings(self):
        # NOTE: liable to change, but probably not
        rulings = db_mtgjson_sqlite.get_rulings(
                db_mtgjson_sqlite.get_card("Serra Angel", "M15").uuid)
        self.assertFalse(rulings)


class TestMTGDatabaseGetFormats(unittest.TestCase):

    def test_has_formats(self):
        # NOTE: liable to change
        expected_result = {'commander': 'Legal', 'duel': 'Legal',
                           'historic': 'Legal', 'legacy': 'Legal',
                           'modern': 'Legal', 'penny': 'Legal',
                           'pioneer': 'Legal', 'vintage': 'Legal'}


        formats = db_mtgjson_sqlite.get_formats(
                db_mtgjson_sqlite.get_card("Serra Angel", "M15").uuid)
        self.assertTrue(formats)
        self.assertEqual(len(formats), 8)
        self.assertEqual(expected_result, formats)

    def test_has_no_formats(self):
        # NOTE: liable to change, but probably not
        formats = db_mtgjson_sqlite.get_formats(
                db_mtgjson_sqlite.get_card("Jund", "OPC2").uuid)
        self.assertFalse(formats)


class TestMTGDatabaseGetOtherFaces(unittest.TestCase):

    def test_flip_card(self):
        expected_result = ''
        card = db_mtgjson_sqlite.get_card('Akki Lavarunner')
        otherfaces = db_mtgjson_sqlite.get_other_faces(card)
        self.assertEqual(len(otherfaces), 1)
        self.assertEqual(otherfaces[0].name, 'Tok-Tok, Volcano Born')

    def test_flip_card_sideb(self):
        expected_result = ''
        card = db_mtgjson_sqlite.get_card('Tok-Tok, Volcano Born')
        otherfaces = db_mtgjson_sqlite.get_other_faces(card.otherfaces[0])
        self.assertEqual(len(otherfaces), 1)
        self.assertEqual(otherfaces[0].name, 'Akki Lavarunner')


class TestMTGDatabaseGetPrice(unittest.TestCase):

    def test_has_price(self):
        price = db_mtgjson_sqlite.get_price("Rimrock Knight", "ELD")
        self.assertTrue(price)
        self.assertEqual(type(price), float)

    def test_no_setcode_specified(self):
        prices = db_mtgjson_sqlite.get_price("Serra Angel")
        self.assertTrue(prices)
        self.assertEqual(type(prices), list)

    def test_price_none(self):
        price = db_mtgjson_sqlite.get_price("Boulder Rush", "ELD")
        self.assertEqual(price, None)

    def test_price_none_list(self):
        prices = db_mtgjson_sqlite.get_price("Boulder Rush")
        self.assertEqual(prices[0][1], None)


class TestMTGDatabaseGetSets(unittest.TestCase):

    def test_sets(self):
        sets = db_mtgjson_sqlite.get_sets()
        self.assertEqual(sets['M20'], 'core')


class TestMTGDatabaseGetToken(unittest.TestCase):

    def test_green_beast(self):
        card = db_mtgjson_sqlite.get_token('Beast')
        self.assertEqual(card.name, 'Beast')
        self.assertEqual(card.types[0], 'Token')
