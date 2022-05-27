# -*- coding: utf-8 -*-

import unittest
from tests import load_tests
load_tests.__module__ = __name__

from mtgcard.parser import parser
from mtgcard.parser import sql_where_card_or_otherids

from mtgcard import settings

class TestSqlWhereCardOrOtherids(unittest.TestCase):

    def test_one_arg(self):
        expected_result = '''

    (
        (
            condition
        )


        


    )

    '''
        actual_result = sql_where_card_or_otherids("condition")
        self.assertEqual(actual_result, expected_result)


class TestParser(unittest.TestCase):

    def test_no_keywords_single_search(self):
        expected_result = (sql_where_card_or_otherids(
                               "lower(v_name) LIKE lower(?)",
                               "lower(cards.faceName) LIKE lower(?)"),
                           ('%angel%','%angel%'))
        actual_result = parser.parse('angel')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_name_case(self):
        expected_result = (sql_where_card_or_otherids(
                               "lower(v_name) LIKE lower(?)",
                               "lower(cards.faceName) LIKE lower(?)"),
                           ('%angel%','%angel%'))
        actual_result = parser.parse('name:angel')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_name_keyword(self):
        expected_result = (sql_where_card_or_otherids(
                               "lower(v_name) LIKE lower(?)",
                               "lower(cards.faceName) LIKE lower(?)"),
                           ('%angel%','%angel%'))
        actual_result = parser.parse('name:angel')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_name_keyword_exact(self):
        expected_result = (sql_where_card_or_otherids(
                "lower(v_name) = lower(?)",
                "lower(cards.faceName) = lower(?)"),
            ('angel','angel'))
        actual_result = parser.parse('name:!angel')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_name_keyword_double_quotes(self):
        expected_result = (sql_where_card_or_otherids(
                               "lower(v_name) LIKE lower(?)",
                               "lower(cards.faceName) LIKE lower(?)"),
                           ('%angel%','%angel%'))
        actual_result = parser.parse('name:"angel"')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_name_keyword_single_quotes(self):
        expected_result = (sql_where_card_or_otherids(
                               "lower(v_name) LIKE lower(?)",
                               "lower(cards.faceName) LIKE lower(?)"),
                           ('%angel%','%angel%'))
        actual_result = parser.parse('name:\'angel\'')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_name_keyword_with_spaces(self):
        expected_result = (sql_where_card_or_otherids(
                               "lower(v_name) LIKE lower(?)",
                               "lower(cards.faceName) LIKE lower(?)"),
                           ('%serra angel%','%serra angel%'))
        actual_result = parser.parse('name:"serra angel"')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_set(self):
        expected_result = (sql_where_card_or_otherids(
                "lower(cards.setCode) = lower(?)"),
            ('eld',))
        actual_result = parser.parse('set = eld')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_format(self):
        expected_result = (sql_where_card_or_otherids(
                "lower(legalities.format) = lower(?)"),
            ('modern',))
        actual_result = parser.parse('legal:modern')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_type_keyword(self):
        sql_query = '''
        (csv_in(lower(cards.subtypes), lower(?)) OR
        csv_in(lower(cards.supertypes), lower(?)) OR
        csv_in(lower(cards.types), lower(?)))
        '''
        expected_result = (sql_where_card_or_otherids(
                sql_query,
                sql_query),
            ('angel', 'angel', 'angel', 'angel', 'angel', 'angel'))
        actual_result = parser.parse('type:angel')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_text(self):
        expected_result = (sql_where_card_or_otherids(
                "lower(cards.text) LIKE lower(?)",
                "lower(cards.text) LIKE lower(?)"),
            ('%angel%','%angel%'))
        actual_result = parser.parse('text:angel')
        self.assertEqual(actual_result[0:2], expected_result[0:2])


    # numbers

    def test_cmc_gt(self):
        expected_result = (sql_where_card_or_otherids(
                "cards.convertedManaCost > ?"),
            (3,))
        actual_result = parser.parse('cmc > 3')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_cmc_eq(self):
        expected_result = (sql_where_card_or_otherids(
                "cards.convertedManaCost = ?"),
            (3,))
        actual_result = parser.parse('cmc:3')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_power_lt(self):
        expected_result = (sql_where_card_or_otherids(
                "cards.power < ?",
                "cards.power < ?",
                ("'aftermath'","'flip'","'transform'","'meld'")),
            (3,3,))
        actual_result = parser.parse('power < 3')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_toughness_ge(self):
        expected_result = (sql_where_card_or_otherids(
                "cards.toughness >= ?",
                "cards.toughness >= ?",
                ("'aftermath'","'flip'","'transform'","'meld'")),
            (3,3,))
        actual_result = parser.parse('toughness >= 3')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_loyalty_le(self):
        expected_result = (sql_where_card_or_otherids(
                "cards.loyalty <= ?"),
            (4,))
        actual_result = parser.parse('loyalty <= 4')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_year_ne(self):
        expected_result = (sql_where_card_or_otherids(
                "CAST(strftime('%Y', DATE(sets.releaseDate)) AS INTEGER) != ?"),
            (2010,2010))
        actual_result = parser.parse('year != 2010')
        self.assertEqual(actual_result[0:2], expected_result[0:2])


    # floats

    def test_price_le(self):
        expected_result = (sql_where_card_or_otherids('''
        ( prices.price = round(?,2) AND prices.type = 'paper' )
        '''),
        (float( 0.5 / settings.US_TO_CUR_RATE),))
        actual_result = parser.parse('price = 0.5')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_price_integer(self):
        expected_result = (sql_where_card_or_otherids('''
        ( prices.price = round(?,2) AND prices.type = 'paper' )
        '''),
        (float( 1 / settings.US_TO_CUR_RATE),))
        actual_result = parser.parse('price = 1')
        self.assertEqual(actual_result[0:2], expected_result[0:2])


    # colors

    # colors        = colors in manacost (casting cost)
    # colorIdentity = colors in whole card

    def test_colors_lt(self):
        expected_result = (sql_where_card_or_otherids('''
        ( csv_len(colors_sp) < csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower(colors_sp)) )
        ''', '''
        ( csv_len(cards.colors) < csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower(cards.colors)) )
        ''', other_layouts=("'transform'","'meld'")),
        ('u,b','u,b','u,b','u,b'))
        actual_result = parser.parse('colors<ub')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_colors_gt(self):
        expected_result = (sql_where_card_or_otherids('''
        ( csv_len(colors_sp) > csv_len(lower(?)) AND
        csv_set_contains(lower(colors_sp), lower(?)) )
        ''', '''
        ( csv_len(cards.colors) > csv_len(lower(?)) AND
        csv_set_contains(lower(cards.colors), lower(?)) )
        ''', other_layouts=("'transform'","'meld'")),
        ('u,b','u,b','u,b','u,b'))
        actual_result = parser.parse('colors>ub')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_colors_eq(self):
        expected_result = (sql_where_card_or_otherids('''
        ( csv_len(colors_sp) = csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower(colors_sp)) AND
        csv_set_contains(lower(colors_sp), lower(?)) )
        ''', '''
        ( csv_len(cards.colors) = csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower(cards.colors)) AND
        csv_set_contains(lower(cards.colors), lower(?)) )
        ''', other_layouts=("'transform'","'meld'")),
        ('u,b','u,b','u,b','u,b','u,b','u,b'))
        actual_result = parser.parse('colors=ub')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_colors_colon(self):
        expected_result = ('u,b','u,b','u,b','u,b')
        actual_result = parser.parse('colors:ub')
        self.assertEqual(expected_result, actual_result[1])


    # mana>2WUU : card.cmc > 5 AND 1,1,2,u,u in card.mana
    # mana>=2WUU: card.cmc >= 5 AND 1,1,2,u,u in card.mana
    # mana=2WUU : card.cmc = 5 AND card.mana in 1,1,2,u,u
    # mana<=2WUU: cmc <= 5 AND card.mana in 1,2,2,u,u
    # mana<2WUU : cmc < 5 AND card.mana in 1,1,2,u,u

    def test_mana_eq(self):
        expected_result = (sql_where_card_or_otherids('''
        ( manacost_to_cmc(cards.manaCost) = manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(?), lower(cards.manaCost)) AND
        manacost_contains(lower(cards.manaCost), lower(?)) )
        ''', '''
        ( manacost_to_cmc(cards.manaCost) = manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(?), lower(cards.manaCost)) AND
        manacost_contains(lower(cards.manaCost), lower(?)) )
        ''', ("'adventure'","'split'","'aftermath'")),
        ('ub','ub','ub','ub','ub','ub'))
        actual_result = parser.parse('mana=ub')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_mana_lt(self):
        expected_result = (sql_where_card_or_otherids('''
        ( manacost_to_cmc(cards.manaCost) < manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(?), lower(cards.manaCost)) )
        ''', '''
        ( manacost_to_cmc(cards.manaCost) < manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(?), lower(cards.manaCost)) )
        ''', ("'adventure'","'split'","'aftermath'")),
        ('1ub','1ub','1ub','1ub'))
        actual_result = parser.parse('mana<1ub')
        self.assertEqual(actual_result[0:2], expected_result[0:2])

    def test_mana_gt(self):
        expected_result = (sql_where_card_or_otherids('''
        ( manacost_to_cmc(cards.manaCost) > manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(cards.manaCost), lower(?)) )
        ''', '''
        ( manacost_to_cmc(cards.manaCost) > manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(cards.manaCost), lower(?)) )
        ''', ("'adventure'","'split'","'aftermath'")),
        ('1ub','1ub','1ub','1ub'))
        actual_result = parser.parse('mana>1ub')
        self.assertEqual(actual_result[0:2], expected_result[0:2])


    # strings

    def test_strings_empty_quotes(self):
        expected_result = (sql_where_card_or_otherids(
                'lower(v_name) = lower(?)'.strip(),
                'lower(cards.faceName) = lower(?)'.strip()),
            ('',''))
        actual_result = parser.parse("name:!''")
        self.assertEqual(actual_result[0:2], expected_result[0:2])


    # operators

    # just matching the parameters tuple now, as the query is too volatile

    def test_not(self):
        # expected_result = ('NOT lower(v_name) LIKE lower(?)'.strip(),
        #                    ('%serra angel%',))
        expected_result = ('%serra angel%','%serra angel%')
        actual_result = parser.parse("-'serra angel'")
        self.assertEqual(expected_result, actual_result[1])

    def test_brackets_name_or_name(self):
        # expected_result = ('''
        # ( lower(v_name) LIKE lower(?) OR lower(v_name) LIKE lower(?) )
        # '''.strip(), ('%serra angel%', '%shivan dragon%'))
        expected_result = ('%serra angel%','%serra angel%',
                           '%shivan dragon%','%shivan dragon%')
        actual_result = parser.parse("('serra angel' or 'shivan dragon')")
        self.assertEqual(expected_result, actual_result[1])

    def test_brackets_not_first(self):
        expected_result = ('eld', 'b', 'b', 'b', 'b', 'b', 'b',
                                  'w', 'w', 'w', 'w', 'w', 'w')
        actual_result = parser.parse("set:eld (colors=b or colors=w)")
        self.assertEqual(expected_result, actual_result[1])

    # combinations and options

    def test_no_keywords_or_search(self):
        # expected_result = ("lower(v_name) LIKE lower(?) OR lower(v_name) LIKE lower(?)", ('%angel%','%bird%') )
        expected_result = ('%angel%','%angel%','%bird%','%bird%')
        actual_result = parser.parse('angel or bird')
        self.assertEqual(expected_result, actual_result[1])

    def test_name_keyword_twice(self):
        # expected_result = (sql_where_card_or_otherids(
        #         "lower(v_name) LIKE lower(?) AND lower(v_name) LIKE lower(?)",
        #         "lower(v_name) LIKE lower(?) AND lower(v_name) LIKE lower(?)"),
        #     ('%serra%','%serra%','%angel%','%angel%'))
        expected_result = ('%serra%','%serra%','%angel%','%angel%')
        actual_result = parser.parse('name:serra angel')
        self.assertEqual(expected_result, actual_result[1])

    def test_name_and_type_keyword(self):
        # expected_result = ("lower(v_name) LIKE lower(?) AND "+self.type_term,
        #         ('%serra%', 'angel', 'angel'))
        expected_result = ('%serra%','%serra%','angel','angel','angel','angel','angel','angel')
        actual_result = parser.parse('name:serra type:angel')
        self.assertEqual(expected_result, actual_result[1])

    def test_brackets(self):
        # expected_result = ('''
        # ( lower(v_name) LIKE lower(?) OR lower(v_name) LIKE lower(?) )
        # '''.strip(), ('%serra angel%', '%shivan dragon%'))
        expected_result = ('%serra angel%','%serra angel%',
                           '%shivan dragon%','%shivan dragon%')
        actual_result = parser.parse("('serra angel' or 'shivan dragon')")
        self.assertEqual(expected_result, actual_result[1])

    def test_exact_name_and_set(self):
        # expected_result = (sql_where_card_or_otherids('''
        # lower(cards.setCode) = lower(?) AND lower(v_name) = lower(?)
        # '''.strip(), ('m15', 'Serra Angel'))
        expected_result = ('m15','Serra Angel','Serra Angel')
        actual_result = parser.parse("set:m15 !'Serra Angel'")
        self.assertEqual(expected_result, actual_result[1])

    def test_color_and_color(self):
        expected_result = ('b', 'b', 'b', 'b', 'b', 'b',
                           'w', 'w', 'w', 'w', 'w', 'w')
        actual_result = parser.parse("colors=b colors=w")
        self.assertEqual(expected_result, actual_result[1])


    ##################
    #  value errors  #
    ##################

    def test_invalid_eq_keyword(self):
        self.assertRaises(SyntaxError, parser.parse, "badkey:ral")
        self.assertRaises(SyntaxError, parser.parse, "badkey=ral")
        self.assertRaises(SyntaxError, parser.parse, "badkey:!ral")
        self.assertRaises(SyntaxError, parser.parse, "badkey<0")

    def test_invalid_keyword_and_valid_keyword(self):
        self.assertRaises(SyntaxError, parser.parse, "badkey:ral name:ral")
