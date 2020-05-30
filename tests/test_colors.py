import unittest
from tests import load_tests
load_tests.__module__ = __name__

from mtgcard.colors import color, mcolor, rcolor, lcolor
from mtgcard.colors import colorize_mana, colorize_rarity, colorize_text
from mtgcard.colors import colorize_format

def setUpModule():

    mcolor.W     = "\033[1;38;5;230m"
    mcolor.U     = "\033[1;38;5;15m"
    mcolor.B     = "\033[1;38;5;250m"
    mcolor.R     = "\033[1;38;5;200m"
    mcolor.G     = "\033[1;38;5;115m"
    mcolor.C     = "\033[1;38;5;170m"
    mcolor.X     = "\033[1;38;5;170m"
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
    lcolor.legal = "\033[0;38;5;1m"
    lcolor.banned = "\033[0;38;5;2m"
    lcolor.restricted = "\033[0;38;5;3m"
    lcolor.notlegal = "\033[0;38;5;4m"

class TestColorizeMana(unittest.TestCase):

    ###################
    #  return values  #
    ###################

    def test_one_red(self):
        text = 'R'
        expected_result = ['\033[1;38;5;200mR\033[0m', 13+4]
        actual_result = colorize_mana(text, 0)
        self.assertEqual(actual_result, expected_result)

    def test_two_red(self):
        text = 'RR'
        expected_result = ['\033[1;38;5;200mR\033[0m\033[1;38;5;200mR\033[0m', (13+4)*2]
        actual_result = colorize_mana(text, 0)
        self.assertEqual(actual_result, expected_result)

    def test_two_red_one_blue(self):
        text = 'RRU'
        expected_result = ['\033[1;38;5;200mR\033[0m\033[1;38;5;200mR\033[0m\033[1;38;5;15mU\033[0m', (13+4)*2+(12+4)]
        actual_result = colorize_mana(text, 0)
        self.assertEqual(actual_result, expected_result)

    def test_two_red_one_blue_one_colorless(self):
        text = '1RRU'
        expected_result = ['\033[1;38;5;170m1\033[0m\033[1;38;5;200mR\033[0m\033[1;38;5;200mR\033[0m\033[1;38;5;15mU\033[0m', (13+4)*3+(12+4)]
        actual_result = colorize_mana(text, 0)
        self.assertEqual(actual_result, expected_result)

    def test_one_colorless(self):
        text = '1'
        expected_result = ['\033[1;38;5;170m1\033[0m', (13+4)]
        actual_result = colorize_mana(text, 0)
        self.assertEqual(actual_result, expected_result)

    def test_other_text(self):
        text = 'R // G'
        expected_result = ['\033[1;38;5;200mR\033[0m // \033[1;38;5;115mG\033[0m',
                ((13+4)*2)]
        actual_result = colorize_mana(text, 0)
        self.assertEqual(actual_result, expected_result)

    def test_who_what_when_where_why(self):
        text = 'XW // 2R // 2U // 3B // 1G'
        expected_result = [
                '\033[1;38;5;170mX\033[0m\033[1;38;5;230mW\033[0m // '
                '\033[1;38;5;170m2\033[0m\033[1;38;5;200mR\033[0m // '
                '\033[1;38;5;170m2\033[0m\033[1;38;5;15mU\033[0m // '
                '\033[1;38;5;170m3\033[0m\033[1;38;5;250mB\033[0m // '
                '\033[1;38;5;170m1\033[0m\033[1;38;5;115mG\033[0m',
                ( (13+4)*9+(12+4) )]
        actual_result = colorize_mana(text, 0)
        self.assertEqual(actual_result, expected_result)


class TestColorizeRarity(unittest.TestCase):

    ###################
    #  return values  #
    ###################

    def test_common(self):
        text = 'ELD'
        expected_result = ['\033[1;38;5;231mELD\033[0m', 13+4]
        actual_result = colorize_rarity('common', 'ELD', 0)
        self.assertEqual(actual_result, expected_result)

    def test_rare(self):
        text = 'ELD'
        expected_result = ['\033[1;38;5;136mE\033[1;38;5;220mL\033[1;38;5;222mD\033[0m', 13*3+4]
        actual_result = colorize_rarity('rare', 'ELD', 0)
        self.assertEqual(actual_result, expected_result)


class TestColorizeText(unittest.TestCase):

    ###################
    #  return values  #
    ###################

    def test_one_red(self):

        text = '''
│ {R}: Shivan Dragon gets +1/+0    │
│ until end of turn.               │
        '''.strip().splitlines()

        expected_result = '''
│ \033[1;38;5;200mR\033[0m: Shivan Dragon gets +1/+0      │
│ until end of turn.               │
        '''.strip().splitlines()

        actual_result = colorize_text(text)
        self.assertEqual(actual_result, expected_result)

    def test_one_red_two_columns(self):

        text = '''
│ {R}: Shivan Dragon gets +1/+0    │Dragon gets +1/+0    │
│ until end of turn.               │ turn.               │
        '''.strip().splitlines()

        expected_result = '''
│ \033[1;38;5;200mR\033[0m: Shivan Dragon gets +1/+0      │Dragon gets +1/+0    │
│ until end of turn.               │ turn.               │
        '''.strip().splitlines()

        actual_result = colorize_text(text)
        self.assertEqual(actual_result, expected_result)

    def test_two_red_two_columns(self):

        text = '''
│ {R}: Shivan Dragon gets +1/+0    │ {R}: Dragon gets +1/+0    │
│ until end of turn.               │ turn.                     │
        '''.strip().splitlines()

        expected_result = '''
│ \033[1;38;5;200mR\033[0m: Shivan Dragon gets +1/+0      │ \033[1;38;5;200mR\033[0m: Dragon gets +1/+0      │
│ until end of turn.               │ turn.                     │
        '''.strip().splitlines()

        actual_result = colorize_text(text)
        self.assertEqual(actual_result, expected_result)

    def test_three_red_two_columns(self):

        text = '''
│ {R}{R}: Shivan Dragon gets +1/+0    │ {R}: Dragon gets +1/+0    │
│ until end of turn.                  │ turn.                     │
        '''.strip().splitlines()

        expected_result = '''
│ \033[1;38;5;200mR\033[0m\033[1;38;5;200mR\033[0m: Shivan Dragon gets +1/+0        │ \033[1;38;5;200mR\033[0m: Dragon gets +1/+0      │
│ until end of turn.                  │ turn.                     │
        '''.strip().splitlines()

        actual_result = colorize_text(text)
        self.assertEqual(actual_result, expected_result)


    def test_two_red_one_blue_two_columns(self):

        text = '''
│ {R}{U}: Shivan Dragon gets +1/+0    │ {R}: Dragon gets +1/+0    │
│ until end of turn.                  │ turn.                     │
        '''.strip().splitlines()

        expected_result = '''
│ \033[1;38;5;200mR\033[0m\033[1;38;5;15mU\033[0m: Shivan Dragon gets +1/+0        │ \033[1;38;5;200mR\033[0m: Dragon gets +1/+0      │
│ until end of turn.                  │ turn.                     │
        '''.strip().splitlines()

        actual_result = colorize_text(text)
        self.assertEqual(actual_result, expected_result)


    def test_two_red_first_column_one_blue_second_column(self):

        text = '''
│ {R}{R}: Shivan Dragon gets +1/+0    │ {U}: Dragon gets +1/+0    │
│ until end of turn.                  │ turn.                     │
        '''.strip().splitlines()

        expected_result = '''
│ \033[1;38;5;200mR\033[0m\033[1;38;5;200mR\033[0m: Shivan Dragon gets +1/+0        │ \033[1;38;5;15mU\033[0m: Dragon gets +1/+0      │
│ until end of turn.                  │ turn.                     │
        '''.strip().splitlines()

        actual_result = colorize_text(text)
        self.assertEqual(actual_result, expected_result)
class TestColorizeFormat(unittest.TestCase):

    ###################
    #  return values  #
    ###################

    def test_legal(self):
        text = 'Standard'
        status = 'Legal'
        expected_result = ['\033[0;38;5;1mStandard\033[0m', 11+4]
        actual_result = colorize_format(text, status)
        self.assertEqual(actual_result, expected_result)

    def test_banned(self):
        text = 'Standard'
        status = 'Banned'
        expected_result = ['\033[0;38;5;2mStandard\033[0m', 11+4]
        actual_result = colorize_format(text, status)
        self.assertEqual(actual_result, expected_result)

    def test_restricted(self):
        text = 'Standard'
        status = 'Restr.'
        expected_result = ['\033[0;38;5;3mStandard\033[0m', 11+4]
        actual_result = colorize_format(text, status)
        self.assertEqual(actual_result, expected_result)

    def test_notlegal(self):
        text = 'Standard'
        status = ''
        expected_result = ['\033[0;38;5;4mStandard\033[0m', 11+4]
        actual_result = colorize_format(text, status)
        self.assertEqual(actual_result, expected_result)
