import unittest
from tests import load_tests
load_tests.__module__ = __name__

from mtgcard.card import Card
from mtgcard.colors import color, mcolor, rcolor

def setUpModule():

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


class TestPrintCard(unittest.TestCase):

    ###################
    #  return errors  #
    ###################


    def test_to_name_line(self):
        expected_result = '''
┌──────────────────────────────────┐
│Shivan Dragon                  4RR│
        '''.strip().splitlines()
        c = Card()
        c.name = "Shivan Dragon"
        c.manacost = "4RR"
        c.type = ""
        c.setcode = ""
        c.power = 0
        c.toughness = 0
        c.loyalty = 0
        c.text = ""
        actual_result = c.print_card(w=36).splitlines()[0:2]
        self.assertEqual(actual_result, expected_result)

    def test_to_name_line_variable(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bristling Boar                  3G│
        '''.strip().splitlines()
        c = Card()
        c.name = "Bristling Boar"
        c.manacost = "3G"
        c.type = ""
        c.setcode = ""
        c.power = 0
        c.toughness = 0
        c.loyalty = 0
        c.text = ""
        actual_result = c.print_card(w=36).splitlines()[0:2]
        self.assertEqual(actual_result, expected_result)

    def test_to_image(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bristling Boar                  3G│
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
        '''.strip().splitlines()
        c = Card()
        c.name = "Bristling Boar"
        c.manacost = "3G"
        c.type = ""
        c.setcode = ""
        c.power = 0
        c.toughness = 0
        c.loyalty = 0
        c.text = ""
        actual_result = c.print_card(w=36, img_pad=2).splitlines()[0:15]
        self.assertEqual(actual_result, expected_result)

    def test_to_type(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bristling Boar                  3G│
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
│Creature — Boar                M20│
        '''.strip().splitlines()
        c = Card()
        c.name = "Bristling Boar"
        c.manacost = "3G"
        c.type = "Creature — Boar"
        c.setcode = "M20"
        c.power = 0
        c.toughness = 0
        c.loyalty = 0
        c.text = ""
        actual_result = c.print_card(w=36, img_pad=2).splitlines()[0:16]
        self.assertEqual(actual_result, expected_result)

    def test_to_text(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bristling Boar                  3G│
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
│Creature — Boar                M20│
│                                  │
│ Bristling Boar can't be blocked  │
│ by more than one creature.       │
        '''.strip().splitlines()
        text = "Bristling Boar can't be blocked by more than one creature."
        c = Card()
        c.name = "Bristling Boar"
        c.manacost = "3G"
        c.type = "Creature — Boar"
        c.setcode = "M20"
        c.power = 0
        c.toughness = 0
        c.loyalty = 0
        c.text = text
        actual_result = c.print_card(w=36, img_pad=2).splitlines()[0:19]
        self.assertEqual(actual_result, expected_result)

    def test_to_power_and_toughness_full(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bristling Boar                  3G│
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
│Creature — Boar                M20│
│                                  │
│ Bristling Boar can't be blocked  │
│ by more than one creature.       │
│                                  │
│                                  │
│                                  │
│                                  │
│                               4/3│
└──────────────────────────────────┘
        '''.strip().splitlines()
        text = "Bristling Boar can't be blocked by more than one creature."
        c = Card()
        c.name = "Bristling Boar"
        c.manacost = "3G"
        c.type = "Creature — Boar"
        c.setcode = "M20"
        c.power = 4
        c.toughness = 3
        c.loyalty = 0
        c.text = text
        actual_result = c.print_card(w=36, img_pad=2, min_text=6).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_another_creature(self):
        expected_result = '''
┌──────────────────────────────────┐
│Shivan Dragon                  4RR│
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
│Creature — Dragon              M20│
│                                  │
│ Flying (This creature can't be   │
│ blocked except by creatures with │
│ flying or reach.)                │
│                                  │
│ {R}: Shivan Dragon gets +1/+0    │
│ until end of turn.               │
│                               5/5│
└──────────────────────────────────┘
        '''.strip().splitlines()
        text = "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn."
        c = Card()
        c.name = "Shivan Dragon"
        c.manacost = "4RR"
        c.type = "Creature — Dragon"
        c.setcode = "M20"
        c.power = 5
        c.toughness = 5
        c.loyalty = 0
        c.text = text
        actual_result = c.print_card(w=36, img_pad=2).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_longest_name(self):
        expected_result = '''
┌──────────────────────────────────┐
│Okina, Temple to the Grandfathers │
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
│Legendary — Land               CHK│
│                                  │
│ {T}: Add {G}. — {G}, {T}: Target │
│ legendary creature gets +1/+1    │
│ until end of turn.               │
│                                  │
│                                  │
│                                  │
│                                  │
└──────────────────────────────────┘
        '''.strip().splitlines()
        text = "{T}: Add {G}. — {G}, {T}: Target legendary creature gets +1/+1 until end of turn."
        c = Card()
        c.name = "Okina, Temple to the Grandfathers"
        c.manacost = None
        c.type = "Legendary — Land"
        c.setcode = "CHK"
        c.power = None
        c.toughness = None
        c.loyalty = None
        c.text = text
        actual_result = c.print_card(w=36, img_pad=2, min_text=6).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_long_type(self):
        expected_result = '''
┌──────────────────────────────────┐
│Vivien, Champion of the Wilds   2G│
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
│Legendary Planeswalker — Vivi  WAR│
│                                  │
│ You may cast creature spells as  │
│ though they had flash.           │
│                                  │
│ [+1]: Until your next turn, up   │
│ to one target creature gains     │
│ vigilance and reach.             │
│                                  │
│ [−2]: Look at the top three      │
│ cards of your library. Exile one │
│ face down and put the rest on    │
│ the bottom of your library in    │
│ any order. For as long as it     │
│ remains exiled, you may look at  │
│ that card and you may cast it if │
│ it's a creature card.            │
│                                  │
└──────────────────────────────────┘
        '''.strip().splitlines()
        text = "You may cast creature spells as though they had flash.\n[+1]: Until your next turn, up to one target creature gains vigilance and reach.\n[−2]: Look at the top three cards of your library. Exile one face down and put the rest on the bottom of your library in any order. For as long as it remains exiled, you may look at that card and you may cast it if it's a creature card."
        c = Card()
        c.name = "Vivien, Champion of the Wilds"
        c.manacost = "2G"
        c.type = "Legendary Planeswalker — Vivien"
        c.setcode = "WAR"
        c.power = None
        c.toughness = None
        c.loyalty = None
        c.text = text
        actual_result = c.print_card(w=36, img_pad=2).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_adventure_to_after_name(self):
        expected_result = '''
┌──────────────────────────────────┐
│Rimrock Knight                  1R│
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
│Creature — Dwarf Knight        ELD│
├─────────────────┬────────────────┤
        '''.strip().splitlines()
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c = Card()
        c.name = "Rimrock Knight"
        c.layout = "adventure"
        c.manacost = "1R"
        c.type = "Creature — Dwarf Knight"
        c.setcode = "ELD"
        c.power = 3
        c.toughness = 1
        c.text = "Rimrock Knight can't block."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2).splitlines()[0:17]
        self.assertEqual(actual_result, expected_result)

    def test_adventure_to_text(self):
        expected_result = '''
┌──────────────────────────────────┐
│Rimrock Knight                  1R│
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
│Creature — Dwarf Knight        ELD│
├─────────────────┬────────────────┤
│Boulder Rush    R│                │
│Instant — Adventu│                │
│                 │                │
│ Target creature │                │
│ gets +2/+0      │                │
│ until end of    │ Rimrock Knight │
│ turn. (Then     │ can't block.   │
│ exile this      │                │
│ card. You may   │                │
│ cast the        │                │
│ creature later  │                │
│ from exile.)    │                │
        '''.strip().splitlines()
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c = Card()
        c.name = "Rimrock Knight"
        c.layout = "adventure"
        c.manacost = "1R"
        c.type = "Creature — Dwarf Knight"
        c.setcode = "ELD"
        c.power = 3
        c.toughness = 1
        c.text = "Rimrock Knight can't block."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2).splitlines()[0:29]
        self.assertEqual(actual_result, expected_result)

    def test_adventure_end(self):
        expected_result = '''
┌──────────────────────────────────┐
│Rimrock Knight                  1R│
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
│Creature — Dwarf Knight        ELD│
├─────────────────┬────────────────┤
│Boulder Rush    R│                │
│Instant — Adventu│                │
│                 │                │
│ Target creature │                │
│ gets +2/+0      │                │
│ until end of    │ Rimrock Knight │
│ turn. (Then     │ can't block.   │
│ exile this      │                │
│ card. You may   │                │
│ cast the        │                │
│ creature later  │                │
│ from exile.)    │                │
│                 │             3/1│
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c = Card()
        c.name = "Rimrock Knight"
        c.layout = "adventure"
        c.manacost = "1R"
        c.type = "Creature — Dwarf Knight"
        c.setcode = "ELD"
        c.power = 3
        c.toughness = 1
        c.text = "Rimrock Knight can't block."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_adventure_with_sorcery(self):
        expected_result = '''
┌──────────────────────────────────┐
│Fae of Wishes                   1U│
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
│Creature — Faerie Wizard       ELD│
├─────────────────┬────────────────┤
│Granted        3U│                │
│Sorcery — Adventu│                │
│                 │ Flying         │
│ You may choose  │                │
│ a noncreature   │ {1}{U},        │
│ card you own    │ Discard two    │
│ from outside    │ cards: Return  │
│ the game,       │ Fae of Wishes  │
│ reveal it, and  │ to its owner's │
│ put it into     │ hand.          │
│ your hand.      │                │
│                 │             1/4│
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Granted"
        a.manacost = "3U"
        a.type = "Sorcery — Adventure"
        a.text = "You may choose a noncreature card you own from outside the game, reveal it, and put it into your hand."
        c = Card()
        c.name = "Fae of Wishes"
        c.layout = "adventure"
        c.manacost = "1U"
        c.type = "Creature — Faerie Wizard"
        c.setcode = "ELD"
        c.power = 1
        c.toughness = 4
        c.text = "Flying\n{1}{U}, Discard two cards: Return Fae of Wishes to its owner's hand."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_adventure_width_41(self):
        expected_result = '''
┌───────────────────────────────────────┐
│Rimrock Knight                       1R│
│                                       │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│  ///////////////////////////////////  │
│                                       │
│Creature — Dwarf Knight             ELD│
├───────────────────┬───────────────────┤
│Boulder Rush      R│                   │
│Instant — Adventure│                   │
│                   │                   │
│ Target creature   │                   │
│ gets +2/+0 until  │                   │
│ end of turn.      │ Rimrock Knight    │
│ (Then exile this  │ can't block.      │
│ card. You may     │                   │
│ cast the creature │                   │
│ later from        │                   │
│ exile.)           │                   │
│                   │                3/1│
└───────────────────┴───────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c = Card()
        c.name = "Rimrock Knight"
        c.layout = "adventure"
        c.manacost = "1R"
        c.type = "Creature — Dwarf Knight"
        c.setcode = "ELD"
        c.power = 3
        c.toughness = 1
        c.text = "Rimrock Knight can't block."
        c.otherfaces = [a]
        actual_result = c.print_card(w=41, img_pad=2).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_adventure_color(self):
        expected_result = '''
┌──────────────────────────────────┐
│Rimrock Knight                  \033[1;38;5;170m1\033[0m\033[1;38;5;200mR\033[0m│
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
│Creature — Dwarf Knight        \033[1;38;5;231mELD\033[0m│
├─────────────────┬────────────────┤
│Boulder Rush    \033[1;38;5;200mR\033[0m│                │
│Instant — Adventu│                │
│                 │                │
│ Target creature │                │
│ gets +2/+0      │                │
│ until end of    │ Rimrock Knight │
│ turn. (Then     │ can't block.   │
│ exile this      │                │
│ card. You may   │                │
│ cast the        │                │
│ creature later  │                │
│ from exile.)    │                │
│                 │             3/1│
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c = Card()
        c.name = "Rimrock Knight"
        c.layout = "adventure"
        c.manacost = "1R"
        c.type = "Creature — Dwarf Knight"
        c.setcode = "ELD"
        c.power = 3
        c.toughness = 1
        c.rarity = "common"
        c.text = "Rimrock Knight can't block."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2, ansi=True).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_text_color(self):
        expected_result = '''
┌──────────────────────────────────┐
│Shivan Dragon                  \033[1;38;5;170m4\033[0m\033[1;38;5;200mR\033[0m\033[1;38;5;200mR\033[0m│
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
│Creature — Dragon              \033[1;38;5;136mM\033[1;38;5;220m2\033[1;38;5;222m0\033[0m│
│                                  │
│ Flying (This creature can't be   │
│ blocked except by creatures with │
│ flying or reach.)                │
│                                  │
│ \033[1;38;5;200mR\033[0m: Shivan Dragon gets +1/+0      │
│ until end of turn.               │
│                               5/5│
└──────────────────────────────────┘
        '''.strip().splitlines()
        text = "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn."
        c = Card()
        c.name = "Shivan Dragon"
        c.layout = "adventure"
        c.manacost = "4RR"
        c.type = "Creature — Dragon"
        c.setcode = "M20"
        c.power = 5
        c.toughness = 5
        c.rarity = "rare"
        c.text = text
        actual_result = c.print_card(w=36, img_pad=2, ansi=True).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_adventure_text_color(self):
        expected_result = '''
┌──────────────────────────────────┐
│Fae of Wishes                   \033[1;38;5;170m1\033[0m\033[1;38;5;15mU\033[0m│
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
│Creature — Faerie Wizard       [1;38;5;136mE[1;38;5;220mL[1;38;5;222mD[0m│
├─────────────────┬────────────────┤
│Granted        \033[1;38;5;170m1\033[0m\033[1;38;5;15mU\033[0m│                │
│Sorcery — Adventu│                │
│                 │ Flying         │
│ You may choose  │                │
│ a noncreature   │ \033[1;38;5;170m1\033[0m\033[1;38;5;15mU\033[0m,            │
│ card you own    │ Discard two    │
│ from outside    │ cards: Return  │
│ the game,       │ Fae of Wishes  │
│ reveal it, and  │ to its owner's │
│ put it into     │ hand.          │
│ your hand.      │                │
│                 │             1/4│
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Granted"
        a.manacost = "1U"
        a.type = "Sorcery — Adventure"
        a.text = "You may choose a noncreature card you own from outside the game, reveal it, and put it into your hand."
        c = Card()
        c.name = "Fae of Wishes"
        c.layout = "adventure"
        c.manacost = "1U"
        c.type = "Creature — Faerie Wizard"
        c.setcode = "ELD"
        c.power = 1
        c.toughness = 4
        c.rarity = "rare"
        c.text = "Flying\n{1}{U}, Discard two cards: Return Fae of Wishes to its owner's hand."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2, ansi=True).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_coloreless_color(self):
        expected_result = '''
┌──────────────────────────────────┐
│Angel's Feather                  \033[1;38;5;170m2\033[0m│
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
│Artifact                       \033[1;38;5;67mM\033[1;38;5;110m1\033[1;38;5;152m2\033[0m│
│                                  │
│ Whenever a player casts a white  │
│ spell, you may gain 1 life.      │
│                                  │
│                                  │
│                                  │
│                                  │
│                                  │
└──────────────────────────────────┘
        '''.strip().splitlines()
        c = Card()
        c.name = "Angel's Feather"
        c.manacost = "2"
        c.type = "Artifact"
        c.setcode = "M12"
        c.rarity = "uncommon"
        c.text = "Whenever a player casts a white spell, you may gain 1 life."
        actual_result = c.print_card(w=36, img_pad=2, ansi=True).splitlines()
        self.assertEqual(actual_result, expected_result)

        # this test is for a {W/U} being displayed in one character
    #     def test181_optional_color(self):
    #         expected_result = '''
    # ┌──────────────────────────────────┐
    # │Dream Salvage                    \033[1;48;5;153m\033[1;38;5;235mB\033[0m│
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
    # │Instant                        \033[1;38;5;67mS\033[1;38;5;110mH\033[1;38;5;152mM\033[0m│
    # │                                  │
    # │ Draw cards equal to the number   │
    # │ of cards target opponent         │
    # │ discarded this turn.             │
    # │                                  │
    # │                                  │
    # │                                  │
    # │                                  │
    # └──────────────────────────────────┘
    #         '''.strip().splitlines()
    #         c = Card()
    #         c.name = "Dream Salvage"
    #         c.manacost = "U/B"
    #         c.type = "Instant"
    #         c.setcode = "SHM"
    #         c.rarity = "uncommon"
    #         c.text = "Draw cards equal to the number of cards target opponent discarded this turn."
    #         actual_result = c.print_card(w=36, img_pad=2, ansi=True).splitlines()
    #         self.assertEqual(expected_result, actual_result)


    def test_no_image(self):
        expected_result = '''
┌──────────────────────────────────┐
│Shivan Dragon                  4RR│
│                                  │
│                                  │
│Creature — Dragon              M20│
│                                  │
│ Flying (This creature can't be   │
│ blocked except by creatures with │
│ flying or reach.)                │
│                                  │
│ {R}: Shivan Dragon gets +1/+0    │
│ until end of turn.               │
│                               5/5│
└──────────────────────────────────┘
        '''.strip().splitlines()
        text = "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn."
        c = Card()
        c.name = "Shivan Dragon"
        c.manacost = "4RR"
        c.type = "Creature — Dragon"
        c.setcode = "M20"
        c.power = 5
        c.toughness = 5
        c.loyalty = 0
        c.text = text
        actual_result = c.print_card(w=36, img_pad=2, image=False).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_adventure_more_text_on_side_a(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bonecrusher Giant               2R│
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
│Creature — Giant               ELD│
├─────────────────┬────────────────┤
│Stomp          1R│                │
│Instant — Adventu│ Whenever       │
│                 │ Bonecrusher    │
│                 │ Giant becomes  │
│ Damage can’t be │ the target of  │
│ prevented this  │ a spell,       │
│ turn. Stomp     │ Bonecrusher    │
│ deals 2 damage  │ Giant deals 2  │
│ to any target.  │ damage to that │
│                 │ spell’s        │
│                 │ controller.    │
│                 │             4/3│
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Stomp"
        a.manacost = "1R"
        a.type = "Instant — Adventure"
        a.text = "Damage can’t be prevented this turn. Stomp deals 2 damage to any target."
        c = Card()
        c.name = "Bonecrusher Giant"
        c.layout = "adventure"
        c.manacost = "2R"
        c.type = "Creature — Giant"
        c.setcode = "ELD"
        c.power = 4
        c.toughness = 3
        c.text = "Whenever Bonecrusher Giant becomes the target of a spell, Bonecrusher Giant deals 2 damage to that spell’s controller."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_adventure_min_text_a(self):
        expected_result = '''
┌──────────────────────────────────┐
│Rimrock Knight                  1R│
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
│Creature — Dwarf Knight        ELD│
├─────────────────┬────────────────┤
│Boulder Rush    R│                │
│Instant — Adventu│                │
│                 │                │
│ Target creature │                │
│ gets +2/+0      │                │
│ until end of    │                │
│ turn. (Then     │ Rimrock Knight │
│ exile this      │ can't block.   │
│ card. You may   │                │
│ cast the        │                │
│ creature later  │                │
│ from exile.)    │                │
│                 │                │
│                 │             3/1│
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Boulder Rush"
        a.manacost = "R"
        a.type = "Instant — Adventure"
        a.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        c = Card()
        c.name = "Rimrock Knight"
        c.layout = "adventure"
        c.manacost = "1R"
        c.type = "Creature — Dwarf Knight"
        c.setcode = "ELD"
        c.power = 3
        c.toughness = 1
        c.text = "Rimrock Knight can't block."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2, min_text=10).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_adventure_min_text_b(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bonecrusher Giant               2R│
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
│Creature — Giant               ELD│
├─────────────────┬────────────────┤
│Stomp          1R│                │
│Instant — Adventu│ Whenever       │
│                 │ Bonecrusher    │
│                 │ Giant becomes  │
│                 │ the target of  │
│ Damage can’t be │ a spell,       │
│ prevented this  │ Bonecrusher    │
│ turn. Stomp     │ Giant deals 2  │
│ deals 2 damage  │ damage to that │
│ to any target.  │ spell’s        │
│                 │ controller.    │
│                 │                │
│                 │             4/3│
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        a = Card()
        a.name = "Stomp"
        a.manacost = "1R"
        a.type = "Instant — Adventure"
        a.text = "Damage can’t be prevented this turn. Stomp deals 2 damage to any target."
        c = Card()
        c.name = "Bonecrusher Giant"
        c.layout = "adventure"
        c.manacost = "2R"
        c.type = "Creature — Giant"
        c.setcode = "ELD"
        c.power = 4
        c.toughness = 3
        c.text = "Whenever Bonecrusher Giant becomes the target of a spell, Bonecrusher Giant deals 2 damage to that spell’s controller."
        c.otherfaces = [a]
        actual_result = c.print_card(w=36, img_pad=2, min_text=11).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_transform(self):
        expected_result = '''
┌──────────────────────────────────┐
│Voldaren Pariah                3BB│
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
│Creature — Vampire Horror      EMN│
│                                  │
│ Flying                           │
│                                  │
│ Sacrifice three other creatures: │
│ Transform Voldaren Pariah.       │
│                                  │
│ Madness {B}{B}{B} (If you        │
│ discard this card, discard it    │
│ into exile. When you do, cast it │
│ for its madness cost or put it   │
│ into your graveyard.)            │
│(6/5)                          3/3│
└──────────────────────────────────┘
        '''.strip().splitlines()
        b = Card()
        b.name = "Abolisher of Bloodlines"
        b.side = 'b'
        b.type = "Creature — Eldrazi Vampire"
        b.setcode = "EMN"
        b.power = 6
        b.toughness = 5
        b.text = "Flying\nWhen this creature transforms into Abolisher of Bloodlines, target opponent sacrifices three creatures."
        a = Card()
        a.name = "Voldaren Pariah"
        a.side = 'a'
        a.layout = 'transform'
        a.manacost = "3BB"
        a.type = "Creature — Vampire Horror"
        a.setcode = "EMN"
        a.power = 3
        a.toughness = 3
        a.text = "Flying\nSacrifice three other creatures: Transform Voldaren Pariah.\nMadness {B}{B}{B} (If you discard this card, discard it into exile. When you do, cast it for its madness cost or put it into your graveyard.)"
        a.otherfaces = [b]
        actual_result = a.print_card(w=36, img_pad=2, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_meld(self):
        expected_result = '''
┌──────────────────────────────────┐
│Bruna, the Fading Light        5WW│
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
│Legendary Creature — Angel Ho  EMN│
│                                  │
│ When you cast this spell, you    │
│ may return target Angel or Human │
│ creature card from your          │
│ graveyard to the battlefield.    │
│                                  │
│ Flying, vigilance                │
│                                  │
│ (Melds with Gisela, the Broken   │
│ Blade.)                          │
│(9/10)                         5/7│
└──────────────────────────────────┘
        '''.strip().splitlines()
        b = Card()
        b.side = 'b'
        b.power = 1
        b.toughness = 1
        c = Card()
        c.name = "Brisela, Voice of Nightmares"
        c.side = 'c'
        c.power = 9
        c.toughness = 10
        text = "When you cast this spell, you may return target Angel or Human creature card from your graveyard to the battlefield.\nFlying, vigilance\n(Melds with Gisela, the Broken Blade.)"
        a = Card()
        a.name = "Bruna, the Fading Light"
        a.side = 'a'
        a.layout = 'meld'
        a.manacost = "5WW"
        a.type = "Legendary Creature — Angel Horror"
        a.setcode = "EMN"
        a.power = 5
        a.toughness = 7
        a.text = text
        a.otherfaces = [b, c]
        actual_result = a.print_card(w=36, img_pad=2, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    ##################
    #  value errors  #
    ##################


    def test_test_values_arg1(self):
        text = "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn."
        c = Card()
        c.name = ""
        c.manacost = "4RR"
        c.type = "Creature — Dragon"
        c.setcode = "M20"
        c.power = 5
        c.toughness = 5
        c.loyalty = None
        c.text = text
        self.assertRaises(ValueError, c.print_card)

    def test_test_values_arg2(self):
        text = "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn."
        c = Card()
        c.name = "Shivan Dragon"
        c.manacost = 0
        c.type = "Creature — Dragon"
        c.setcode = "M20"
        c.power = 5
        c.toughness = 5
        c.loyalty = None
        c.text = text
        self.assertRaises(ValueError, c.print_card)


class TestPrintCardAdventurer(unittest.TestCase):

    ###################
    #  return errors  #
    ###################


    def test_to_name_line(self):
        expected_result = '''
├─────────────────┬
│Boulder Rush    R│
        '''.strip().splitlines()
        c = Card()
        c.name = "Boulder Rush"
        c.manacost = "R"
        c.type = "Instant — Adventure"
        c.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        actual_result = c.print_card_adventurer(15, w=36).splitlines()[0:2]
        self.assertEqual(actual_result, expected_result)

    def test_to_type_line(self):
        expected_result = '''
├─────────────────┬
│Boulder Rush    R│
│Instant — Adventu│
        '''.strip().splitlines()
        c = Card()
        c.name = "Boulder Rush"
        c.manacost = "R"
        c.type = "Instant — Adventure"
        c.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        actual_result = c.print_card_adventurer(15, w=36).splitlines()[0:3]
        self.assertEqual(actual_result, expected_result)

    def test_to_text(self):
        expected_result = '''
├─────────────────┬
│Boulder Rush    R│
│Instant — Adventu│
│                 │
│ Target creature │
│ gets +2/+0      │
│ until end of    │
│ turn. (Then     │
│ exile this      │
│ card. You may   │
│ cast the        │
│ creature later  │
│ from exile.)    │
        '''.strip().splitlines()
        c = Card()
        c.name = "Boulder Rush"
        c.manacost = "R"
        c.type = "Instant — Adventure"
        c.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        actual_result = c.print_card_adventurer(15, w=36).splitlines()[0:13]
        self.assertEqual(actual_result, expected_result)

    def test_instant(self):
        expected_result = '''
├─────────────────┬
│Boulder Rush    R│
│Instant — Adventu│
│                 │
│ Target creature │
│ gets +2/+0      │
│ until end of    │
│ turn. (Then     │
│ exile this      │
│ card. You may   │
│ cast the        │
│ creature later  │
│ from exile.)    │
│                 │
└─────────────────┴
        '''.strip().splitlines()
        c = Card()
        c.name = "Boulder Rush"
        c.manacost = "R"
        c.type = "Instant — Adventure"
        c.text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        actual_result = c.print_card_adventurer(15, w=36).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_sorcery(self):
        expected_result = '''
├─────────────────┬
│Granted        1U│
│Sorcery — Adventu│
│                 │
│ You may choose  │
│ a noncreature   │
│ card you own    │
│ from outside    │
│ the game,       │
│ reveal it, and  │
│ put it into     │
│ your hand.      │
│                 │
└─────────────────┴
        '''.strip().splitlines()
        c = Card()
        c.name = "Granted"
        c.manacost = "1U"
        c.type = "Sorcery — Adventure"
        c.text = "You may choose a noncreature card you own from outside the game, reveal it, and put it into your hand."
        actual_result = c.print_card_adventurer(14, w=36).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_instant(self):
        expected_result = '''
├─────────────────┬
│Stomp          1R│
│Instant — Adventu│
│                 │
│                 │
│                 │
│ Damage can’t be │
│ prevented this  │
│ turn. Stomp     │
│ deals 2 damage  │
│ to any target.  │
│                 │
│                 │
│                 │
└─────────────────┴
        '''.strip().splitlines()
        c = Card()
        c.name = "Stomp"
        c.manacost = "1R"
        c.type = "Instant — Adventure"
        c.text = "Damage can’t be prevented this turn. Stomp deals 2 damage to any target."
        actual_result = c.print_card_adventurer(15, w=36).splitlines()
        self.assertEqual(actual_result, expected_result)


class TestPrintCardFlip(unittest.TestCase):

    ###################
    #  return errors  #
    ###################

    def setUp(self):
        self.f = Card()
        self.f.name = 'Tok-Tok, Volcano Born'
        self.f.type = 'Legendary Creature — Goblin Shaman'
        self.f.manacost = None
        self.f.power = '2'
        self.f.toughness = '2'
        self.f.text = 'Protection from red\nIf a red source would deal damage to a player, it deals that much damage plus 1 to that player instead.'

        self.c = Card()
        self.c.name = "Akki Lavarunner"
        self.c.names = ['Akki Lavarunner', 'Tok-Tok, Volcano Born']
        self.c.type = "Creature — Goblin Warrior"
        self.c.manacost = "3R"
        self.c.setcode = 'CHK'
        self.c.power = '1'
        self.c.toughness = '1'
        self.c.text = "Haste\nWhenever Akki Lavarunner deals damage to an opponent, flip it."
        self.c.layout = 'flip'
        self.c.rarity = 'rare'
        self.c.otherfaces = [self.f]


    def test_to_top_name_line(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()[0:2]
        self.assertEqual(actual_result, expected_result)


    def test_to_top_text(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()[0:7]
        self.assertEqual(actual_result, expected_result)


    def test_to_top_type_line(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│Creature — Goblin Warrior      1/1│
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()[0:9]
        self.assertEqual(actual_result, expected_result)


    def test_to_image(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│Creature — Goblin Warrior      1/1│
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()[0:18]
        self.assertEqual(actual_result, expected_result)


    def test_to_bottom_type_line(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│Creature — Goblin Warrior      1/1│
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│Legendary Creature — Goblin S  2/2│
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()[0:19]
        self.assertEqual(actual_result, expected_result)


    def test_to_bottom_text(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│Creature — Goblin Warrior      1/1│
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│Legendary Creature — Goblin S  2/2│
│                                  │
│ Protection from red              │
│                                  │
│ If a red source would deal       │
│ damage to a player, it deals     │
│ that much damage plus 1 to that  │
│ player instead.                  │
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()[0:26]
        self.assertEqual(actual_result, expected_result)

    def test_to_bottom_name(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│Creature — Goblin Warrior      1/1│
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│Legendary Creature — Goblin S  2/2│
│                                  │
│ Protection from red              │
│                                  │
│ If a red source would deal       │
│ damage to a player, it deals     │
│ that much damage plus 1 to that  │
│ player instead.                  │
│                                  │
│Tok-Tok, Volcano Born          CHK│
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()[0:28]
        self.assertEqual(actual_result, expected_result)


    def test_flip_card(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│Creature — Goblin Warrior      1/1│
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│Legendary Creature — Goblin S  2/2│
│                                  │
│ Protection from red              │
│                                  │
│ If a red source would deal       │
│ damage to a player, it deals     │
│ that much damage plus 1 to that  │
│ player instead.                  │
│                                  │
│Tok-Tok, Volcano Born          CHK│
└──────────────────────────────────┘
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)

    def test_flip_card_min_text(self):
        expected_result = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│                                  │
│Creature — Goblin Warrior      1/1│
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│  //////////////////////////////  │
│Legendary Creature — Goblin S  2/2│
│                                  │
│ Protection from red              │
│                                  │
│ If a red source would deal       │
│ damage to a player, it deals     │
│ that much damage plus 1 to that  │
│ player instead.                  │
│                                  │
│Tok-Tok, Volcano Born          CHK│
└──────────────────────────────────┘
        '''.strip().splitlines()
        actual_result = self.c.print_card_flip(w=36, min_text=11, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


class TestPrintCardSplit(unittest.TestCase):

    ###################
    #  return errors  #
    ###################

    def setUp(self):
        self.b = Card()
        self.b.name = 'Ends'
        self.b.type = 'Instant'
        self.b.manacost = '3RW'
        self.b.setcode = 'DIS'
        self.b.text = 'Target player sacrifices two attacking creatures.'

        self.a = Card()
        self.a.name = 'Odds'
        self.a.names = ['Odds', 'Ends']
        self.a.type = 'Instant'
        self.a.manacost = 'UR'
        self.a.setcode = 'DIS'
        self.a.text = 'Flip a coin. If it comes up heads, counter target instant or sorcery spell. If it comes up tails, copy that spell and you may choose new targets for the copy.'
        self.a.layout = 'split'
        self.a.rarity = 'rare'
        self.a.otherfaces = [self.b]


    def test_left_right(self):
        expected_result = '''
┌─────────────────┬────────────────┐
│Odds           UR│Ends         3RW│
│                 │                │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│                 │                │
│Instant       DIS│Instant      DIS│
│                 │                │
│ Flip a coin. If │ Target player  │
│ it comes up     │ sacrifices two │
│ heads, counter  │ attacking      │
│ target instant  │ creatures.     │
│ or sorcery      │                │
│ spell. If it    │                │
│ comes up tails, │                │
│ copy that spell │                │
│ and you may     │                │
│ choose new      │                │
│ targets for the │                │
│ copy.           │                │
│                 │                │
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        actual_result = self.a.print_card_split(w=36, pad=0, text_pad=1,
                min_text=0, image=True, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_left_right_b_higher(self):
        expected_result = '''
┌─────────────────┬────────────────┐
│Supply        XGW│Demand       1WU│
│                 │                │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│                 │                │
│Sorcery       DIS│Sorcery      DIS│
│                 │                │
│ Create X 1/1    │ Search your    │
│ green Saproling │ library for a  │
│ creature        │ multicolored   │
│ tokens.         │ card, reveal   │
│                 │ it, and put it │
│                 │ into your      │
│                 │ hand. Then     │
│                 │ shuffle your   │
│                 │ library.       │
│                 │                │
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        b = Card()
        b.name = 'Demand'
        b.type = 'Sorcery'
        b.manacost = '1WU'
        b.setcode = 'DIS'
        b.text = 'Search your library for a multicolored card, reveal it, and put it into your hand. Then shuffle your library.'
        a = Card()
        a.name = 'Supply'
        a.names = ['Supply', 'Demand']
        a.type = 'Sorcery'
        a.manacost = 'XGW'
        a.setcode = 'DIS'
        a.text = 'Create X 1/1 green Saproling creature tokens.'
        a.layout = 'split'
        a.otherfaces = [b]
        actual_result = a.print_card_split(w=36, pad=0, text_pad=1,
                min_text=0, image=True, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_up_down(self):
        expected_result = '''
┌──────────────────────────────────┐
│Odds                            UR│
│                                  │
│                                  │
│Instant                        DIS│
│                                  │
│ Flip a coin. If it comes up      │
│ heads, counter target instant or │
│ sorcery spell. If it comes up    │
│ tails, copy that spell and you   │
│ may choose new targets for the   │
│ copy.                            │
│                                  │
├──────────────────────────────────┤
│Ends                           3RW│
│                                  │
│                                  │
│Instant                        DIS│
│                                  │
│ Target player sacrifices two     │
│ attacking creatures.             │
│                                  │
└──────────────────────────────────┘
        '''.strip().splitlines()
        actual_result = self.a.print_card_split(w=36, image=False,
                ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_up_down_min_text_9(self):
        expected_result = '''
┌──────────────────────────────────┐
│Odds                            UR│
│                                  │
│                                  │
│Instant                        DIS│
│                                  │
│ Flip a coin. If it comes up      │
│ heads, counter target instant or │
│ sorcery spell. If it comes up    │
│ tails, copy that spell and you   │
│ may choose new targets for the   │
│ copy.                            │
│                                  │
├──────────────────────────────────┤
│Ends                           3RW│
│                                  │
│                                  │
│Instant                        DIS│
│                                  │
│ Target player sacrifices two     │
│ attacking creatures.             │
│                                  │
│                                  │
└──────────────────────────────────┘
        '''.strip().splitlines()
        actual_result = self.a.print_card_split(w=36, min_text=9, image=False,
                ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_wide(self):
        expected_result = '''
┌─────────────────────────────┬────────────────────────────┐
│Odds                       UR│Ends                     3RW│
│                             │                            │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│  /////////////////////////  │  ////////////////////////  │
│                             │                            │
│Instant                   DIS│Instant                  DIS│
│                             │                            │
│ Flip a coin. If it comes up │ Target player sacrifices   │
│ heads, counter target       │ two attacking creatures.   │
│ instant or sorcery spell.   │                            │
│ If it comes up tails, copy  │                            │
│ that spell and you may      │                            │
│ choose new targets for the  │                            │
│ copy.                       │                            │
│                             │                            │
└─────────────────────────────┴────────────────────────────┘
        '''.strip().splitlines()
        actual_result = self.a.print_card_split(wide=True, w=36, pad=0, text_pad=1,
                min_text=0, image=True, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_fuse(self):
        expected_result = '''
┌─────────────────┬────────────────┐
│Wear           1R│Tear           W│
│                 │                │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│                 │                │
│Instant       DGM│Instant      DGM│
│                 │                │
│ Destroy target  │ Destroy target │
│ artifact.       │ enchantment.   │
│                 │                │
│ Fuse (You may cast one or both   │
│ halves of this card from your    │
│ hand.)                           │
│                 │                │
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        b = Card()
        b.name = 'Tear'
        b.type = 'Instant'
        b.manacost = 'W'
        b.setcode = 'DGM'
        b.text = 'Destroy target enchantment.\nFuse (You may cast one or both halves of this card from your hand.)'
        a = Card()
        a.name = 'Wear'
        a.names = ['Wear', 'Tear']
        a.type = 'Instant'
        a.manacost = '1R'
        a.setcode = 'DGM'
        a.text = 'Destroy target artifact.\nFuse (You may cast one or both halves of this card from your hand.)'
        a.layout = 'split'
        a.otherfaces = [b]
        actual_result = a.print_card_split(w=36, pad=0, text_pad=1,
                min_text=0, image=True, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_fuse_a_higher(self):
        expected_result = '''
┌─────────────────┬────────────────┐
│Turn           2U│Burn          1R│
│                 │                │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│                 │                │
│Instant       DGM│Instant      DGM│
│                 │                │
│ Until end of    │ Burn deals 2   │
│ turn, target    │ damage to any  │
│ creature loses  │ target.        │
│ all abilities   │                │
│ and becomes a   │                │
│ red Weird with  │                │
│ base power and  │                │
│ toughness 0/1.  │                │
│                 │                │
│ Fuse (You may cast one or both   │
│ halves of this card from your    │
│ hand.)                           │
│                 │                │
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        b = Card()
        b.name = 'Burn'
        b.type = 'Instant'
        b.manacost = '1R'
        b.setcode = 'DGM'
        b.text = 'Burn deals 2 damage to any target.\nFuse (You may cast one or both halves of this card from your hand.)'
        a = Card()
        a.name = 'Turn'
        a.names = ['Turn', 'Burn']
        a.type = 'Instant'
        a.manacost = '2U'
        a.setcode = 'DGM'
        a.text = 'Until end of turn, target creature loses all abilities and becomes a red Weird with base power and toughness 0/1.\nFuse (You may cast one or both halves of this card from your hand.)'
        a.layout = 'split'
        a.otherfaces = [b]
        actual_result = a.print_card_split(w=36, pad=0, text_pad=1,
                min_text=0, image=True, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_fuse_b_higher(self):
        expected_result = '''
┌─────────────────┬────────────────┐
│Toil           2B│Trouble       2R│
│                 │                │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│                 │                │
│Sorcery       DGM│Sorcery      DGM│
│                 │                │
│ Target player   │ Trouble deals  │
│ draws two cards │ damage to      │
│ and loses 2     │ target player  │
│ life.           │ equal to the   │
│                 │ number of      │
│                 │ cards in that  │
│                 │ player's hand. │
│                 │                │
│ Fuse (You may cast one or both   │
│ halves of this card from your    │
│ hand.)                           │
│                 │                │
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        b = Card()
        b.name = 'Trouble'
        b.type = 'Sorcery'
        b.manacost = '2R'
        b.setcode = 'DGM'
        b.text = "Trouble deals damage to target player equal to the number of cards in that player's hand.\nFuse (You may cast one or both halves of this card from your hand.)"
        a = Card()
        a.name = 'Toil'
        a.names = ['Toil', 'Trouble']
        a.type = 'Sorcery'
        a.manacost = '2B'
        a.setcode = 'DGM'
        a.text = 'Target player draws two cards and loses 2 life.\nFuse (You may cast one or both halves of this card from your hand.)'
        a.layout = 'split'
        a.otherfaces = [b]
        actual_result = a.print_card_split(w=36, pad=0, text_pad=1,
                min_text=0, image=True, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)


    def test_fuse_b_higher_min_text(self):
        expected_result = '''
┌─────────────────┬────────────────┐
│Toil           2B│Trouble       2R│
│                 │                │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│  /////////////  │  ////////////  │
│                 │                │
│Sorcery       DGM│Sorcery      DGM│
│                 │                │
│ Target player   │ Trouble deals  │
│ draws two cards │ damage to      │
│ and loses 2     │ target player  │
│ life.           │ equal to the   │
│                 │ number of      │
│                 │ cards in that  │
│                 │ player's hand. │
│                 │                │
│ Fuse (You may cast one or both   │
│ halves of this card from your    │
│ hand.)                           │
│                 │                │
│                 │                │
│                 │                │
│                 │                │
└─────────────────┴────────────────┘
        '''.strip().splitlines()
        b = Card()
        b.name = 'Trouble'
        b.type = 'Sorcery'
        b.manacost = '2R'
        b.setcode = 'DGM'
        b.text = "Trouble deals damage to target player equal to the number of cards in that player's hand.\nFuse (You may cast one or both halves of this card from your hand.)"
        a = Card()
        a.name = 'Toil'
        a.names = ['Toil', 'Trouble']
        a.type = 'Sorcery'
        a.manacost = '2B'
        a.setcode = 'DGM'
        a.text = 'Target player draws two cards and loses 2 life.\nFuse (You may cast one or both halves of this card from your hand.)'
        a.layout = 'split'
        a.otherfaces = [b]
        actual_result = a.print_card_split(w=36, pad=0, text_pad=1,
                min_text=14, image=True, ansi=False).splitlines()
        self.assertEqual(actual_result, expected_result)
