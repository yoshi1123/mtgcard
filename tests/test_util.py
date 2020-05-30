import unittest
from tests import load_tests
load_tests.__module__ = __name__

from textwrap import wrap

from mtgcard.card import Card

from mtgcard.util import columnize
from mtgcard.util import multi_name
from mtgcard.util import text_height
from mtgcard.util import adv_text_height
from mtgcard.util import card_text_center
from mtgcard.util import card_inscribe
from mtgcard.util import legality_print
from mtgcard.util import text_height_of_highest


class TestColumnize(unittest.TestCase):

    def test_two_column_one_line(self):
        text_left = ['fire']
        text_right = ['water']
        expected_result = '''
fire water
        '''.strip().splitlines()
        actual_result = columnize(5, text_left, text_right)
        self.assertEqual(actual_result, expected_result)

    def test_two_column_two_lines(self):
        text_left = ['fire', 'charmander']
        text_right = ['water', 'squirtle']
        expected_result = '''
fire       water      
charmander squirtle   
'''.strip('\n').splitlines()
        actual_result = columnize(11, text_left, text_right)
        self.assertEqual(actual_result, expected_result)

    def test_two_column_two_lines_and_three_lines(self):
        text_left = ['fire', 'charmander']
        text_right = ['water', 'squirtle', 'seel']
        expected_result = '''
fire       water      
charmander squirtle   
           seel       
'''.strip('\n').splitlines()
        actual_result = columnize(11, text_left, text_right)
        self.assertEqual(actual_result, expected_result)

    def test_three_column_two_lines(self):
        text_left = ['fire', 'charmander']
        text_middle = ['water', 'squirtle']
        text_right = ['grass', 'bulbasaur']
        expected_result = '''
fire       water      grass      
charmander squirtle   bulbasaur  
'''.strip('\n').splitlines()
        actual_result = columnize(11, text_left, text_middle, text_right)
        self.assertEqual(actual_result, expected_result)

    def test_three_column_two_lines_four_lines_and_three_lines(self):
        text_left = ['fire', 'charmander']
        text_middle = ['water', 'squirtle', 'seel', 'goldeen']
        text_right = ['grass', 'bulbasaur', 'caterpie']
        expected_result = '''
fire       water      grass      
charmander squirtle   bulbasaur  
           seel       caterpie   
           goldeen               
'''.strip('\n').splitlines()
        actual_result = columnize(11, text_left, text_middle, text_right)
        self.assertEqual(actual_result, expected_result)

    def test_three_column_two_lines_four_lines_and_three_lines_spacer(self):
        text_left = ['fire', 'charmander']
        text_middle = ['water', 'squirtle', 'seel', 'goldeen']
        text_right = ['grass', 'bulbasaur', 'caterpie']
        expected_result = '''
fire        water       grass     
charmander  squirtle    bulbasaur 
            seel        caterpie  
            goldeen               
'''.strip('\n').splitlines()
        actual_result = columnize(10, text_left, text_middle, text_right, sep=2)
        self.assertEqual(actual_result, expected_result)

    def test_two_column_paragraphs(self):
        text = wrap('Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.', 40)

        text_left = text
        text_right = text
        expected_result = '''
Lorem ipsum dolor sit amet, consetetur  Lorem ipsum dolor sit amet, consetetur  
sadipscing elitr, sed diam nonumy eirmodsadipscing elitr, sed diam nonumy eirmod
tempor invidunt ut labore et dolore     tempor invidunt ut labore et dolore     
magna aliquyam erat, sed diam voluptua. magna aliquyam erat, sed diam voluptua. 
At vero eos et accusam et justo duo     At vero eos et accusam et justo duo     
dolores et ea rebum. Stet clita kasd    dolores et ea rebum. Stet clita kasd    
gubergren, no sea takimata sanctus est  gubergren, no sea takimata sanctus est  
Lorem ipsum dolor sit amet.             Lorem ipsum dolor sit amet.             
'''.strip('\n').splitlines()
        actual_result = columnize(40, text_left, text_right)
        self.assertEqual(actual_result, expected_result)



class TestMultiName(unittest.TestCase):

    def test_adventure(self):
        a = Card()
        a.name = "Boulder Rush"
        a.side = 'b'
        c = Card()
        c.name = "Rimrock Knight"
        c.names = ["Rimrock Knight", "Boulder Rush"]
        c.side = 'a'
        c.layout = "adventure"
        c.otherfaces = [a]
        expected_result = "Rimrock Knight // Boulder Rush"
        actual_result = multi_name(c)
        self.assertEqual(actual_result, expected_result)

    def test_meld(self):
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
        a.names = ['Bruna, the Fading Light', 'Brisela, Voice of Nightmares', 'Gisela, the Broken Blade']
        a.side = 'a'
        a.layout = 'meld'
        a.manacost = "5WW"
        a.type = "Legendary Creature — Angel Horror"
        a.setcode = "EMN"
        a.power = 5
        a.toughness = 7
        a.text = text
        a.otherfaces = [b, c]
        expected_result = "Bruna, the Fading Light // Brisela, Voice of Nightmares"
        actual_result = multi_name(a)
        self.assertEqual(actual_result, expected_result)

class TestTextHeight(unittest.TestCase):

    def test_normal_layout_image(self):
        cardprint = '''
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
        expected_result = 6
        actual_result = text_height(len(cardprint), 'normal', w=36, img_pad=2, image=True)
        self.assertEqual(actual_result, expected_result)


    def test_normal_layout_no_image(self):
        cardprint = '''
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
        expected_result = 6
        actual_result = text_height(len(cardprint), 'normal', w=36, img_pad=2, image=False)
        self.assertEqual(actual_result, expected_result)


    def test_flip_layout_image(self):
        cardprint = '''
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
        expected_result = 10
        actual_result = text_height(len(cardprint), 'flip', w=36, img_pad=2,
                image=True)
        self.assertEqual(actual_result, expected_result)


    def test_flip_layout_no_image(self):
        cardprint = '''
┌──────────────────────────────────┐
│Akki Lavarunner                 3R│
│                                  │
│ Haste                            │
│                                  │
│ Whenever Akki Lavarunner deals   │
│ damage to an opponent, flip it.  │
│                                  │
│Creature — Goblin Warrior      1/1│
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
        expected_result = 10
        actual_result = text_height(len(cardprint), 'flip', w=36, img_pad=2,
                image=False)
        self.assertEqual(actual_result, expected_result)


    def test_split_layout_image(self):
        cardprint = '''
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
        expected_result = 12
        actual_result = text_height(len(cardprint), 'split', w=36, img_pad=2,
                image=True)
        self.assertEqual(actual_result, expected_result)


    def test_split_layout_image_b_higher(self):
        cardprint = '''
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
        expected_result = 9
        actual_result = text_height(len(cardprint), 'split', w=36, img_pad=2,
                image=True)
        self.assertEqual(actual_result, expected_result)


    def test_split_layout_image_fuse_a_higher(self):
        cardprint = '''
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
        expected_result = 12
        actual_result = text_height(len(cardprint), 'split', w=36, img_pad=2,
                image=True)
        self.assertEqual(actual_result, expected_result)


    def test_split_layout_image_fuse_b_higher(self):
        cardprint = '''
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
        expected_result = 11
        actual_result = text_height(len(cardprint), 'split', w=36, img_pad=2,
                image=True)
        self.assertEqual(actual_result, expected_result)

    def test_split_layout_no_image(self):
        cardprint = '''
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
        expected_result = 8
        actual_result = text_height(len(cardprint), 'split', w=36, img_pad=2,
                image=False)
        self.assertEqual(actual_result, expected_result)


    def test_adventure_layout_image(self):
        cardprint = '''
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
        expected_result = 9
        actual_result = text_height(len(cardprint), 'adventure', w=36, img_pad=2,
                image=True)
        self.assertEqual(actual_result, expected_result)


    def test_adventure_layout_image_b_text_max(self):
        cardprint = '''
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
        expected_result = 10
        actual_result = text_height(len(cardprint), 'adventure', w=36,
                img_pad=2, image=True, adv_side_a=False)
        self.assertEqual(actual_result, expected_result)


class TestAdvTextHeight(unittest.TestCase):

    def test_side_a_max(self):
        cardprint = '''
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
        a_text = "Target creature gets +2/+0 until end of turn. (Then exile this card. You may cast the creature later from exile.)"
        b_text = "Rimrock Knight can't block."
        side_a = adv_text_height(a_text, w=36, pad=0, text_pad=1, side_a=True)
        side_b = adv_text_height(b_text, w=36, pad=0, text_pad=1, side_a=False)
        self.assertEqual(side_a, 9)
        self.assertEqual(side_b, 2)


class TestCardTextCenter(unittest.TestCase):

    def test_one_line(self):
        ctext = '''
| line1 |
        '''.strip().splitlines()
        expected_result = '''
| line1 |
        '''.strip().splitlines()
        actual_result = card_text_center(ctext, '|       |', 1)
        self.assertEqual(actual_result, expected_result)

    def test_two_lines_high(self):
        ctext = '''
| line1 |
        '''.strip().splitlines()
        expected_result = '''
| line1 |
|       |
        '''.strip().splitlines()
        actual_result = card_text_center(ctext, '|       |', 2,
                high=True)
        self.assertEqual(actual_result, expected_result)

    def test_two_lines_low(self):
        ctext = '''
| line1 |
        '''.strip().splitlines()
        expected_result = '''
|       |
| line1 |
        '''.strip().splitlines()
        actual_result = card_text_center(ctext, '|       |', 2,
                high=False)
        self.assertEqual(actual_result, expected_result)

    def test_three_lines(self):
        ctext = '''
| line1 |
        '''.strip().splitlines()
        expected_result = '''
|       |
| line1 |
|       |
        '''.strip().splitlines()
        actual_result = card_text_center(ctext, '|       |', 3)
        self.assertEqual(actual_result, expected_result)

    def test_three_lines_two_lines_text_high(self):
        ctext = '''
| line1 |
| line2 |
        '''.strip().splitlines()
        expected_result = '''
| line1 |
| line2 |
|       |
        '''.strip().splitlines()
        actual_result = card_text_center(ctext, '|       |', 3, high=True)
        self.assertEqual(actual_result, expected_result)

    def test_three_lines_two_lines_text_low(self):
        ctext = '''
| line1 |
| line2 |
        '''.strip().splitlines()
        expected_result = '''
|       |
| line1 |
| line2 |
        '''.strip().splitlines()
        actual_result = card_text_center(ctext, '|       |', 3, high=False)
        self.assertEqual(actual_result, expected_result)


class TestLegalityPrint(unittest.TestCase):

    def test_one_format(self):
        legality = {'standard': 'Legal'}
        expected_result = '''
Standard:  legal   Brawl:
Pioneer:           Pauper:
Modern:            Legacy:
Commander:         Vintage:
        '''.strip().splitlines()
        actual_result = legality_print(legality, ansi=False)
        self.assertEqual(actual_result, expected_result)

    def test_two_formats(self):
        legality = {'standard': 'Legal', 'commander': 'Banned'}
        expected_result = '''
Standard:  legal   Brawl:
Pioneer:           Pauper:
Modern:            Legacy:
Commander: banned  Vintage:
        '''.strip().splitlines()
        actual_result = legality_print(legality, ansi=False)
        self.assertEqual(actual_result, expected_result)

class TestCardInscribe(unittest.TestCase):

    def test_one_row(self):
        text = 'Lorem'
        expected_result = '''
│ Lorem  │
'''.strip().splitlines()
        actual_result = card_inscribe(text, w=10)
        self.assertEqual(actual_result, expected_result)

    def test_two_rows(self):
        text = 'Lorem ipsum'
        expected_result = '''
│ Lorem  │
│ ipsum  │
'''.strip().splitlines()
        actual_result = card_inscribe(text, w=10)
        self.assertEqual(actual_result, expected_result)

    def test_two_rows_no_left_border(self):
        text = 'Lorem ipsum'
        expected_result = '''
 Lorem  │
 ipsum  │
'''.strip('\n').splitlines()
        actual_result = card_inscribe(text, w=10, left_border=False)
        self.assertEqual(actual_result, expected_result)

    def test_two_rows_no_right_border(self):
        text = 'Lorem ipsum'
        expected_result = '''
│ Lorem  
│ ipsum  
'''.strip('\n').splitlines()
        actual_result = card_inscribe(text, w=10, right_border=False)
        self.assertEqual(actual_result, expected_result)

    def test_two_rows_no_border(self):
        text = 'Lorem ipsum'
        expected_result = '''
 Lorem  
 ipsum  
'''.strip('\n').splitlines()
        actual_result = card_inscribe(text, w=10, left_border=False,
                right_border=False)
        self.assertEqual(actual_result, expected_result)


class TestTextHeightOfHighest(unittest.TestCase):

    def test_two_normal(self):

        text = "Flying (This creature can't be blocked except by creatures with flying or reach.)\n{R}: Shivan Dragon gets +1/+0 until end of turn."
        c1 = Card()
        c1.name = "Shivan Dragon"
        c1.manacost = "4RR"
        c1.type = "Creature — Dragon"
        c1.setcode = "M20"
        c1.power = 5
        c1.toughness = 5
        c1.loyalty = None
        c1.text = text

        c2 = Card()
        c2.name = "Angel's Feather"
        c2.manacost = "2"
        c2.type = "Artifact"
        c2.setcode = "M12"
        c2.rarity = "uncommon"
        c2.text = "Whenever a player casts a white spell, you may gain 1 life."
        expected_result = 6
        actual_result = text_height_of_highest(*[c1,c2], min_text=0)[0]
        self.assertEqual(actual_result, expected_result)


    def test_transform(self):
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
        expected_result = 10
        actual_result = text_height_of_highest(*[a,b], min_text=0)[0]
        self.assertEqual(actual_result, expected_result)
