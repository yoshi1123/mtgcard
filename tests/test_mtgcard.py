#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ┌──────────────────────────────────┐
# │Bristling Boar                  3G│
# │                                  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │  //////////////////////////////  │
# │                                  │
# │Creature ─ Boar                M20│
# │                                  │
# │ Bristling Boar can't be blocked  │
# │ by more than one creature.       │
# │                                  │
# │                               4/3│
# └──────────────────────────────────┘

# ┌──────────────────────────────┐
# │::;cclloxOOOOOdd,....'okxdo;. │
# │,;;:llldxx00xxdlll:l;';lllc'..│
# │'';:lcllddxo,oolllll;,:c;;;'. │
# │',':;dc'''','...':ldcloo,,,...│
# │;cc;;,:....'..   ..,:oo:;,....│
# │,,coc'.......  .......::''....│
# │..'clc::;.        .....,'.... │
# │...';;:ll;        ..,'...'..  │
# │...',,;:'........';'....... ..│
# │...',,'';'..;;,'........      │
# │.......''''....  ........     │
# └──────────────────────────────┘

# debugging
from pprint import pprint

import unittest
from unittest.mock import patch
from tests import load_tests
load_tests.__module__ = __name__

import re

from mtgcard import get_defaults
from mtgcard import mtgdb
from mtgcard.mtgcard import get_and_print_card
from mtgcard.mtgcard import list_cards
from mtgcard.mtgcard import list_cards_detailed
from mtgcard.mtgcard import list_cards_images
from mtgcard.card import Card
from mtgcard.colors import color, mcolor, rcolor
from mtgcard import settings


def setUpModule():

    get_defaults()

    global db
    db = mtgdb.Interface()

    mcolor.W     = "\033[1;38;5;230m"
    mcolor.U     = "\033[1;38;5;15m"
    mcolor.B     = "\033[1;38;5;250m"
    mcolor.R     = "\033[1;38;5;200m"
    mcolor.G     = "\033[1;38;5;115m"
    mcolor.C     = "\033[1;38;5;170m"
    mcolor.darkW = "\033[1;38;5;229m"
    mcolor.darkU = "\033[1;38;5;19m"
    mcolor.darkB = "\033[1;38;5;235m"
    mcolor.darkR = "\033[1;38;5;160m"
    mcolor.darkG = "\033[1;38;5;22m"
    rcolor.C     = "\033[1;38;5;231m"
    rcolor.U     = "\033[1;38;5;152m"
    rcolor.R     = "\033[1;38;5;222m"
    rcolor.M     = "\033[1;38;5;208m"
    rcolor.midU  = "\033[1;38;5;110m"
    rcolor.midR  = "\033[1;38;5;220m"
    rcolor.midM  = "\033[1;38;5;166m"
    rcolor.darkU = "\033[1;38;5;67m"
    rcolor.darkR = "\033[1;38;5;136m"
    rcolor.darkM = "\033[1;38;5;160m"


class TestGetAndPrintCard(unittest.TestCase):

    def test_get_and_print_card(self):
        expected_result = '''
┌──────────────────────────────────┐
│Barkhide Troll                  GG│
│                                  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│                                  │
│Creature — Troll               M20│
│                                  │
│ Barkhide Troll enters the        │
│ battlefield with a +1/+1 counter │
│ on it.                           │
│                                  │
│ {1}, Remove a +1/+1 counter from │
│ Barkhide Troll: Barkhide Troll   │
│ gains hexproof until end of      │
│ turn. (It can't be the target of │
│ spells or abilities your         │
│ opponents control.)              │
│                               2/2│
└──────────────────────────────────┘
        '''.strip().splitlines()
        actual_result = get_and_print_card(db, "Barkhide Troll", "m20", w=36,
                                           ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_get_and_print_sorcery_card(self):
        expected_result = '''
┌──────────────────────────────────┐
│Aerial Assault                  2W│
│                                  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│                                  │
│Sorcery                        M20│
│                                  │
│ Destroy target tapped creature.  │
│ You gain 1 life for each         │
│ creature you control with        │
│ flying.                          │
│                                  │
│                                  │
│                                  │
└──────────────────────────────────┘
        '''.strip().splitlines()
        actual_result = get_and_print_card(db, "Aerial Assault", "m20", w=36,
                                           ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)

    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_get_and_print_sorcery_card_verbose_price(self):
        cardprint = get_and_print_card(db, "Aerial Assault", "m20", w=36,
                verbose=True, ansi=False).splitlines()
        actual_result_card = cardprint[0:25]
        actual_result_price = cardprint[26]
        self.assertTrue(re.match(r'^Price \(USD\): \$(\d+.\d{2})?$', actual_result_price))

    # def test_get_and_print_sorcery_card_verbose_printings(self):
    #     cardprint = get_and_print_card(db, "Aerial Assault", "m20", w=36,
    #             verbose=True, ansi=False).splitlines()
    #     actual_result_card = cardprint[0:25]
    #     actual_result_price = cardprint[26]
    #     actual_result_printings = cardprint[29]
    #     self.assertTrue(re.match(r'^Core/expansion printings:$', actual_result_printings))
    #
    # def test_get_and_print_sorcery_card_rulings(self):
    #     # NOTE: liable to change
    #     cardprint = get_and_print_card(db, "Aerial Assault", "m20", w=36,
    #             rulings=True, ansi=False).splitlines()
    #     actual_result_card = cardprint[0:25]
    #     actual_result_rulings = cardprint[26]
    #     self.assertTrue(re.match(r'^Rulings:$', actual_result_rulings))
    #
    # def test_get_and_print_sorcery_card_formats(self):
    #     # NOTE: liable to change
    #     cardprint = get_and_print_card(db, "Aerial Assault", "m20", w=36,
    #             verbose=True, ansi=False).splitlines()
    #     actual_result_card = cardprint[0:25]
    #     actual_result_price = cardprint[26]
    #     actual_result_printings = cardprint[28]
    #     actual_result_formats = cardprint[34]
    #     self.assertTrue(re.match(r'^Standard:', actual_result_formats))
    #
    #
class TestListCards(unittest.TestCase):

    ###################
    #  return errors  #
    ###################

    def test_list_cards_m20(self):
        expected_result = '''
Angel of Vitality
Angelic Gift
Angelic Guardian
Dawning Angel
Rienne, Angel of Rebirth
        '''.strip()
        actual_result = list_cards(db, "angel set:m20", onlynames=True)[0]
        self.assertEqual(actual_result, expected_result)

    def test_list_cards_case_insensitive(self):
        expected_result = '''
Aether Shockwave
Aftershock
Barbed Shocker
Rumbling Aftershocks
Shock
Shock Troops
Shocker
Shockmaw Dragon
Spellshock
Staggershock
Stoneshock Giant
Sudden Shock
        '''.strip()
        actual_result = list_cards(db, "Shock", onlynames=True)[0]
        self.assertEqual(actual_result, expected_result)

    def test_meld_card_side_b(self):
        expected_result = '''
Gisela, Blade of Goldnight
Gisela, the Broken Blade
        '''.strip()
        actual_result = list_cards(db, "gisela", onlynames=True)[0]
        self.assertEqual(actual_result, expected_result)

class TestListCardsDetailed(unittest.TestCase):

    ###################
    #  return errors  #
    ###################


    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_list_cards_verbose_one_creature_card(self):
        expected_result = '''
NAME                          SET  MANA           TYPE          PT|L   R  USD
Angelic Guardian              M20  4WW            Creature      5/5    R  $1.00
        '''.strip().splitlines()
        c = Card()
        c.name = 'Angelic Guardian'
        c.setcode = 'M20'
        c.manacost = '4WW'
        c.types = ['Creature']
        c.power = '5'
        c.toughness = '5'
        c.rarity = 'rare'
        c.price = 1.00
        actual_result = list_cards_detailed([c], lname=30, lset=5, lmana=15,
                ltype=14, lptl=7, lr=3, ansi=False)
        self.assertEqual(actual_result, expected_result)

    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_list_cards_verbose_one_enchantment_card(self):
        expected_result = '''
NAME                          SET  MANA           TYPE          PT|L   R  USD
Angelic Gift                  M20  1W             Enchantment          C  $1.00
        '''.strip().splitlines()
        c = Card()
        c.name = 'Angelic Gift'
        c.setcode = 'M20'
        c.manacost = '1W'
        c.types = ['Enchantment']
        c.rarity = 'common'
        c.price = 1.00
        actual_result = list_cards_detailed([c], lname=30, lset=5, lmana=15,
                ltype=14, lptl=7, lr=3, ansi=False)
        self.assertEqual(actual_result, expected_result)

    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_list_cards_verbose_one_planeswalker_card(self):
        expected_result = '''
NAME                          SET  MANA           TYPE          PT|L   R  USD
Ajani, Strength of the Pride  M20  2WW            Planeswalker  5      M  $1.00
        '''.strip().splitlines()
        c = Card()
        c.name = 'Ajani, Strength of the Pride'
        c.setcode = 'M20'
        c.manacost = '2WW'
        c.types = ['Planeswalker']
        c.loyalty = '5'
        c.rarity = 'mythic'
        c.price = 1.00
        actual_result = list_cards_detailed([c], lname=30, lset=5, lmana=15,
                ltype=14, lptl=7, lr=3, ansi=False)
        self.assertEqual(actual_result, expected_result)

    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_list_cards_verbose_one_plains_card(self):
        expected_result = '''
NAME                          SET  MANA           TYPE          PT|L   R  USD
Plains                        M20                 Land                 C  
'''.strip('\n').splitlines()
        c = Card()
        c.name = 'Plains'
        c.setcode = 'M20'
        c.types = ['Land']
        c.rarity = 'common'
        actual_result = list_cards_detailed([c], lname=30, lset=5, lmana=15,
                ltype=14, lptl=7, lr=3, ansi=False)
        self.assertEqual(actual_result, expected_result)

    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_adventure_both_names(self):
        expected_result = '''
NAME                          SET  MANA           TYPE          PT|L   R  USD
Rimrock Knight // Boulder Ru  ELD  1R // R        Creature      3/1    C  $1.00
'''.strip('\n').splitlines()
        sideb = Card()
        sideb.name = 'Boulder Rush'
        sideb.side = 'b'
        sideb.manacost = 'R'
        c = Card()
        c.name = 'Rimrock Knight'
        c.names = ['Rimrock Knight', 'Boulder Rush']
        c.side = 'a'
        c.otherfaces = [sideb]
        c.setcode = 'ELD'
        c.manacost = '1R'
        c.types = ['Creature']
        c.power = '3'
        c.toughness = '1'
        c.rarity = 'common'
        c.price = 1.00
        actual_result = list_cards_detailed([c], lname=30, lset=5, lmana=15,
                ltype=14, lptl=7, lr=3, ansi=False)
        self.assertEqual(actual_result, expected_result)

    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_comma_in_three_names(self):
        expected_result = '''
NAME                          SET  MANA           TYPE          PT|L   R  USD
Bruna, the Fading Light // B  EMN  5WW            Creature      5/7    R  $1.00
'''.strip('\n').splitlines()
        sideb = Card()
        sideb.name = 'Gisela, the Broken Blade'
        sideb.side = 'b'
        sideb.manacost = '2WW'
        sidec = Card()
        sidec.name = 'Brisela, Voice of Nightmares'
        sidec.side = 'c'
        c = Card()
        c.name = 'Bruna, the Fading Light'
        c.layout = 'meld'
        c.side = 'a'
        c.names = ['Bruna, the Fading Light', 'Brisela, Voice of Nightmares', 'Gisela, the Broken Blade']
        c.otherfaces = [sideb, sidec]
        c.setcode = 'EMN'
        c.manacost = '5WW'
        c.types = ['Creature']
        c.power = '5'
        c.toughness = '7'
        c.rarity = 'rare'
        c.price = 1.00
        actual_result = list_cards_detailed([c], lname=30, lset=5, lmana=15,
                ltype=14, lptl=7, lr=3, ansi=False)
        self.assertEqual(actual_result, expected_result)

    @patch('mtgcard.settings.CURRENCY', 'USD')
    @patch('mtgcard.settings.US_TO_CUR_RATE', 1)
    def test_comma_in_three_names_side_b(self):
        expected_result = '''
NAME                             SET  MANA           TYPE          PT|L   R  USD
Gisela, the Broken Blade // Bri  EMN  2WW            Creature      4/3    M  $1.00
'''.strip('\n').splitlines()
        sidea = Card()
        sidea.name = 'Bruna, the Fading Light'
        sidea.side = 'a'
        sidea.manacost = '5WW'
        sidec = Card()
        sidec.name = 'Brisela, Voice of Nightmares'
        sidec.side = 'c'
        c = Card()
        c.name = 'Gisela, the Broken Blade'
        c.layout = 'meld'
        c.side = 'b'
        c.names = ['Bruna, the Fading Light', 'Brisela, Voice of Nightmares', 'Gisela, the Broken Blade']
        c.otherfaces = [sidea, sidec]
        c.setcode = 'EMN'
        c.manacost = '2WW'
        c.types = ['Creature']
        c.power = '4'
        c.toughness = '3'
        c.rarity = 'mythic'
        c.price = 1.00
                                                      #33
        actual_result = list_cards_detailed([c], lname=33, lset=5, lmana=15,
                ltype=14, lptl=7, lr=3, ansi=False)
        self.assertEqual(actual_result, expected_result)

class TestListCardsImages(unittest.TestCase):

    ###################
    #  return errors  #
    ###################


    def test_one_creature(self):
        expected_result = '''
┌──────────────────────────────────┐
│Serra Angel                    [1;38;5;170m3[0m[1;38;5;230mW[0m[1;38;5;230mW[0m│
│                                  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│                                  │
│Creature — Angel               [1;38;5;67mD[1;38;5;110mO[1;38;5;152mM[0m│
│                                  │
│ Flying, vigilance                │
│                                  │
│                                  │
│                                  │
│                                  │
│                                  │
│                               4/4│
└──────────────────────────────────┘
        '''.strip().splitlines()
        c = Card()
        c.name = 'Serra Angel'
        c.setcode = 'DOM'
        c.manacost = '3WW'
        c.type = 'Creature — Angel'
        c.power = '4'
        c.toughness = '4'
        c.rarity = 'uncommon'
        c.text = 'Flying, vigilance'
        actual_result = list_cards_images([c], 1, w=36, img_pad=2, min_text=6,
            image=True, ansi=True)
        self.assertEqual(actual_result, expected_result)

    def test_two_creatures(self):
        expected_result = '''
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│Serra Angel                    [1;38;5;170m3[0m[1;38;5;230mW[0m[1;38;5;230mW[0m│  │Rimrock Knight                  [1;38;5;170m1[0m[1;38;5;200mR[0m│
│                                  │  │                                  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│                                  │  │                                  │
│Creature — Angel               [1;38;5;67mD[1;38;5;110mO[1;38;5;152mM[0m│  │Creature — Dwarf Knight        [1;38;5;231mELD[0m│
│                                  │  ├─────────────────┬────────────────┤
│ Flying, vigilance                │  │Boulder Rush    [1;38;5;200mR[0m│                │
│                                  │  │Instant — Adventu│                │
│                                  │  │                 │                │
│                                  │  │ Target creature │                │
│                                  │  │ gets +2/+0      │                │
│                                  │  │ until end of    │ Rimrock Knight │
│                                  │  │ turn. (Then     │ can't block.   │
│                                  │  │ exile this      │                │
│                                  │  │ card. You may   │                │
│                                  │  │ cast the        │                │
│                                  │  │ creature later  │                │
│                                  │  │ from exile.)    │                │
│                               4/4│  │                 │             3/1│
└──────────────────────────────────┘  └─────────────────┴────────────────┘
        '''.strip().splitlines()
        c1 = Card()
        c1.name = 'Serra Angel'
        c1.setcode = 'DOM'
        c1.manacost = '3WW'
        c1.type = 'Creature — Angel'
        c1.power = '4'
        c1.toughness = '4'
        c1.rarity = 'uncommon'
        c1.text = 'Flying, vigilance'
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c2 = Card()
        c2.name = "Rimrock Knight"
        c2.side = 'a'
        c2.layout = "adventure"
        c2.manacost = "1R"
        c2.type = "Creature — Dwarf Knight"
        c2.setcode = "ELD"
        c2.power = 3
        c2.toughness = 1
        c2.rarity = "common"
        c2.text = "Rimrock Knight can't block."
        c2.otherfaces = [a]
        actual_result = list_cards_images([c1,c2], 2, w=36, img_pad=2, image=True,
                ansi=True)
        self.assertEqual(actual_result, expected_result)

    def test_two_rows(self):
        expected_result = '''
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│Serra Angel                    [1;38;5;170m3[0m[1;38;5;230mW[0m[1;38;5;230mW[0m│  │Rimrock Knight                  [1;38;5;170m1[0m[1;38;5;200mR[0m│
│                                  │  │                                  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│                                  │  │                                  │
│Creature — Angel               [1;38;5;67mD[1;38;5;110mO[1;38;5;152mM[0m│  │Creature — Dwarf Knight        [1;38;5;231mELD[0m│
│                                  │  ├─────────────────┬────────────────┤
│ Flying, vigilance                │  │Boulder Rush    [1;38;5;200mR[0m│                │
│                                  │  │Instant — Adventu│                │
│                                  │  │                 │                │
│                                  │  │ Target creature │                │
│                                  │  │ gets +2/+0      │                │
│                                  │  │ until end of    │ Rimrock Knight │
│                                  │  │ turn. (Then     │ can't block.   │
│                                  │  │ exile this      │                │
│                                  │  │ card. You may   │                │
│                                  │  │ cast the        │                │
│                                  │  │ creature later  │                │
│                                  │  │ from exile.)    │                │
│                               4/4│  │                 │             3/1│
└──────────────────────────────────┘  └─────────────────┴────────────────┘
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│Serra Angel                    [1;38;5;170m3[0m[1;38;5;230mW[0m[1;38;5;230mW[0m│  │Rimrock Knight                  [1;38;5;170m1[0m[1;38;5;200mR[0m│
│                                  │  │                                  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│  //////////////////////////////  │  │  //////////////////////////////  │
│                                  │  │                                  │
│Creature — Angel               [1;38;5;67mD[1;38;5;110mO[1;38;5;152mM[0m│  │Creature — Dwarf Knight        [1;38;5;231mELD[0m│
│                                  │  ├─────────────────┬────────────────┤
│ Flying, vigilance                │  │Boulder Rush    [1;38;5;200mR[0m│                │
│                                  │  │Instant — Adventu│                │
│                                  │  │                 │                │
│                                  │  │ Target creature │                │
│                                  │  │ gets +2/+0      │                │
│                                  │  │ until end of    │ Rimrock Knight │
│                                  │  │ turn. (Then     │ can't block.   │
│                                  │  │ exile this      │                │
│                                  │  │ card. You may   │                │
│                                  │  │ cast the        │                │
│                                  │  │ creature later  │                │
│                                  │  │ from exile.)    │                │
│                               4/4│  │                 │             3/1│
└──────────────────────────────────┘  └─────────────────┴────────────────┘
        '''.strip().splitlines()
        c1 = Card()
        c1.name = 'Serra Angel'
        c1.setcode = 'DOM'
        c1.manacost = '3WW'
        c1.type = 'Creature — Angel'
        c1.power = '4'
        c1.toughness = '4'
        c1.rarity = 'uncommon'
        c1.text = 'Flying, vigilance'
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c2 = Card()
        c2.name = "Rimrock Knight"
        c2.side = 'a'
        c2.layout = "adventure"
        c2.manacost = "1R"
        c2.type = "Creature — Dwarf Knight"
        c2.setcode = "ELD"
        c2.power = '3'
        c2.toughness = '1'
        c2.rarity = "common"
        c2.text = "Rimrock Knight can't block."
        c2.otherfaces = [a]
        actual_result = list_cards_images([c1,c2,c1,c2], 2, w=36, img_pad=2,
                image=True, ansi=True)
        self.assertEqual(actual_result, expected_result)


    def test_one_creature_no_image(self):
        expected_result = '''
┌──────────────────────────────────┐
│Serra Angel                    [1;38;5;170m3[0m[1;38;5;230mW[0m[1;38;5;230mW[0m│
│                                  │
│                                  │
│Creature — Angel               [1;38;5;67mD[1;38;5;110mO[1;38;5;152mM[0m│
│                                  │
│ Flying, vigilance                │
│                                  │
│                                  │
│                                  │
│                                  │
│                                  │
│                               4/4│
└──────────────────────────────────┘
        '''.strip().splitlines()
        c = Card()
        c.name = 'Serra Angel'
        c.setcode = 'DOM'
        c.manacost = '3WW'
        c.type = 'Creature — Angel'
        c.power = '4'
        c.toughness = '4'
        c.rarity = 'uncommon'
        c.text = 'Flying, vigilance'
        actual_result = list_cards_images([c], 1, w=36, img_pad=2, min_text=6,
            image=False, ansi=True)
        self.assertEqual(actual_result, expected_result)
