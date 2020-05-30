# mtgcard - Command-line MTG card viewer and searcher.
# Copyright (C) 2020  yoshi1@tutanota.com
#
# mtgcard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mtgcard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with mtgcard.  If not, see <https://www.gnu.org/licenses/>.

"""MTG card class."""


from math import ceil
from math import floor
from textwrap import wrap
import re

from mtgcard.colors import color, mcolor, rcolor
from mtgcard.colors import colorize
from mtgcard.colors import colorize_rarity, colorize_mana, colorize_text
from mtgcard import util


class Card(object):
    """A MTG Card."""

    def __init__(self):
        """Initialize."""
        self.name = None
        self.uuid = None
        self.cmc = None
        self.manacost = None
        self.colors = None
        self.types = None
        self.type = None
        self.setcode = None
        self.power = None
        self.toughness = None
        self.loyalty = None
        self.rarity = None
        self.text = None
        self.side = None
        self.otherfaces = None
        self.printings = None
        self.rulings = None
        self.layout = None
        self.names = None
        self.price = None
        self.price_date = None
        self.formats = None

    def __str__(self):
        """Return all Card attributes for `self`."""
        attrs = vars(self)
        ls = []
        ls.append("Card '{!s:s}'".format(self.name))
        for attr in attrs.keys():
            if attr == "text" and attrs[attr] is not None:
                v = attrs[attr].replace("\n", "//")
            else:
                v = attrs[attr]
            ls.append("  {:11s}: {!s}".format(attr, v))

        return "\n".join(ls)

    def print_card(
        self,
        w=36,
        pad=0,
        img_pad=2,
        text_pad=1,
        min_text=6,
        image=True,
        single_side=False,
        wide=False,
        ansi=False,
    ):
        """Return print of Card.

        :param int  w:           width of columns
        :param int  pad:         left/right card padding
        :param int  img_pad:     left/right image padding
        :param int  text_pad:    left/right text padding
        :param int  min_text:    minimum text line count
        :param bool image:       whether to print image
        :param bool single_side: whether to print only one card face
        :param bool wide:        whether to use extra columns for two faces*
        :param bool ansi:        whether color

        * For split cards, the print will use more than `w`. For transform and
          meld cards, the print will use double `w` to print the cards side by
          side.

                        /  : image
                        -  : text_pad
                        .. : image_pad

                        ┌──────────────────────────────────┐
                        │Bristling Boar                  3G│
                        │                                  │
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │..//////////////////////////////..│
                        │                                  │
                        │Creature — Boar                M20│
                        │                                  │
                      ^ │-Bristling Boar can't be blocked -│
                text  | │-by more than one creature.      -│
                line  | │-                                -│
               count  | │-                                -│
                 (6)  | │-                                -│
                      v │-                                -│
                        │                               4/3│
                        └──────────────────────────────────┘
                        <---------------------------------->
                                        w

        """
        ############
        #  layout  #
        ############

        if not single_side:

            if self.side == "a" and self.layout == "flip":
                return self.print_card_flip(
                    w=w,
                    pad=pad,
                    img_pad=img_pad,
                    text_pad=text_pad,
                    min_text=min_text,
                    image=image,
                    ansi=ansi,
                )

            elif self.side == "a" and self.layout in ("split", "aftermath"):
                return self.print_card_split(
                    w=w,
                    pad=pad,
                    img_pad=img_pad,
                    text_pad=text_pad,
                    min_text=min_text,
                    image=image,
                    wide=wide,
                    ansi=ansi,
                )

            elif (self.layout == "transform" and self.side == "a") or (
                self.layout == "meld" and self.side in ("a", "b")
            ):
                return self.print_card_transform(
                    w=w,
                    pad=pad,
                    img_pad=img_pad,
                    text_pad=text_pad,
                    min_text=min_text,
                    image=image,
                    wide=wide,
                    ansi=ansi,
                )

        ###############
        #  arguments  #
        ###############

        name = self.name
        manacost = self.manacost
        types = self.type
        setcode = self.setcode
        power = self.power
        toughness = self.toughness
        loyalty = self.loyalty
        rarity = self.rarity
        text = self.text
        if not single_side and self.otherfaces and self.layout == "adventure":
            adventure = self.otherfaces[0]
        else:
            adventure = None

        if manacost is None:
            manacost = ""
        if setcode is None:
            setcode = ""

        if name == "":
            raise ValueError("name empty")
        if type(manacost) != str:
            raise ValueError("invalid mana cost")

        ###########
        #  color  #
        ###########

        mcolor_shift = 0
        rcolor_shift = 0

        if ansi:

            if manacost != "":
                [manacost, mcolor_shift] = colorize_mana(
                    manacost, mcolor_shift
                )
            if rarity:
                [setcode, rcolor_shift] = colorize_rarity(
                    rarity, setcode, rcolor_shift
                )

        ##################
        #  measurements  #
        ##################

        inner_width = w - 2 - pad * 2

        if manacost != "":
            name_len = inner_width - len(self.manacost) - 2
            mana_len = len(self.manacost) + 2 + mcolor_shift
        else:
            mana_len = 0
            name_len = inner_width

        image_width = w - img_pad * 2 - 2
        image_height = round(image_width * 0.37)

        if setcode != "":
            types_len = inner_width - len(self.setcode) - 2 - pad
            setcode_len = len(self.setcode) + 2 + rcolor_shift
        else:
            setcode_len = 0
            types_len = inner_width - pad

        ptl_len = 6

        ###################
        #  create spacer  #
        ###################

        spacer_fmt = "{:s}{:s}{:s}"
        spacer = spacer_fmt.format("│", " " * (w - 2), "│")

        ######################
        #  CREATE PRINTCARD  #
        ######################

        cardprint = []

        ################
        #  top border  #
        ################

        top_fmt = "{:s}{:s}{:s}"
        cardprint.append(top_fmt.format("┌", "─" * (w - 2), "┐"))

        ##########
        #  name  #
        ##########

        # card.append( '│{:<27s}{:>7s}│'.format(name, manacost) )
        name_fmt = "{:s}{:<{name_len!s}s}{:>{mana_len!s}s}{:s}"
        cardprint.append(
            name_fmt.format(
                "│",
                name[:name_len],
                manacost,
                "│",
                name_len=name_len,
                mana_len=mana_len,
            )
        )

        ############
        #  spacer  #
        ############

        cardprint.append(spacer)

        ###########
        #  image  #
        ###########

        if image:
            image_fmt = "{:s}{:^{inner_width!s}s}{:s}"
            for i in range(image_height):
                cardprint.append(
                    image_fmt.format(
                        "│", "/" * image_width, "│", inner_width=inner_width
                    )
                )

        ############
        #  spacer  #
        ############

        cardprint.append(spacer)

        ###########
        #  types  #
        ###########

        types_fmt = "{:s}{:<{types_len!s}s}{:>{setcode_len!s}s}{:s}"
        cardprint.append(
            types_fmt.format(
                "│",
                types[:types_len],
                setcode,
                "│",
                types_len=types_len,
                setcode_len=setcode_len,
            )
        )

        ##################
        #  REGULAR CARD  #
        ##################
        if not adventure:

            ############
            #  spacer  #
            ############

            cardprint.append(spacer)

            #######################
            #  regular card text  #
            #######################

            ftext = util.card_inscribe(text, w=w, pad=pad, text_pad=text_pad)
            nr_ftext = len(ftext)
            if ansi:
                ftext = colorize_text(ftext)
            cardprint = cardprint + ftext

            #########################
            #  text minimum height  #
            #########################

            if nr_ftext < min_text:
                for i in range(0, min_text - nr_ftext):
                    cardprint.append(spacer)

            ####################################
            #  power and toughness or loyalty  #
            ####################################

            ptl_fmt = "{:s}{:s}{:s}{:>{inner_width!s}s}{:s}{:s}"
            if power is not None:
                ptl = "{!s}/{!s}".format(power, toughness)
            elif loyalty is not None:
                ptl = loyalty
            else:
                ptl = ""

            tpt = ""
            t_shift = 0
            if (self.layout == "transform" and self.side == "a") or (
                self.layout == "meld" and self.side in ("a", "b")
            ):
                b = util.get_transform_meld_sideb(self)
                if b.power is not None:
                    tpt = "({!s}/{!s})".format(b.power, b.toughness)
                    if ansi:
                        tpt, t_shift = colorize(tpt, "black")

            cardprint.append(
                ptl_fmt.format(
                    "│",
                    " " * pad,
                    tpt,
                    ptl,
                    " " * pad,
                    "│",
                    inner_width=inner_width - len(tpt) + t_shift,
                )
            )

            ################################
            #  regular card bottom border  #
            ################################

            bottom_fmt = "{:s}{:s}{:s}"
            cardprint.append(bottom_fmt.format("└", "─" * (w - 2), "┘"))

        #####################
        #  ADVENTURER CARD  #
        #####################
        else:

            #############################
            #  get height of adventure  #
            #############################

            # get adv text height
            atext_height = (
                util.adv_text_height(
                    adventure.text,
                    w=w,
                    pad=pad,
                    text_pad=text_pad,
                    side_a=True,
                )
                + 6
            )  # 6 non-text lines in adv side

            # get main text height
            mtext_height = (
                util.adv_text_height(
                    text, w=w, pad=pad, text_pad=text_pad, side_a=False
                )
                + 4
            )  # 4 non-text lines in main side

            # get the higher
            adv_height = max([atext_height, mtext_height])

            if atext_height > mtext_height:
                if atext_height - 6 < min_text:
                    adv_height += min_text - (atext_height - 6)
            else:
                if mtext_height - 4 < min_text:
                    adv_height += min_text - (mtext_height - 4)

            ########################
            #  get adventure card  #
            ########################

            a = adventure
            adv_card = a.print_card_adventurer(
                adv_height, w=w, pad=pad, text_pad=text_pad, ansi=ansi
            ).splitlines()

            ##################
            #  measurements  #
            ##################

            w_a = floor(w / 2) + 1
            w_b = w - w_a + 1
            inner_width_b = w_b - 2 - pad * 2

            ###################
            #  create spacer  #
            ###################

            spacer_fmt = "{:s}{:s}"
            bprint_spacer = spacer_fmt.format(" " * (w_b - 2), "│")

            ###############
            #  main text  #
            ###############

            mtext = util.card_inscribe(
                text, w=w_b, pad=pad, text_pad=text_pad, left_border=False
            )

            ##################
            #  side b print  #
            ##################

            bprint = []

            #######################
            #  side b top border  #
            #######################

            top_fmt = "{:s}{:s}"
            bprint.append(spacer_fmt.format("─" * (w_b - 2), "┤"))

            #################
            #  side b text  #
            #################

            alines = len(adv_card)
            btext = util.card_text_center(
                mtext, bprint_spacer, alines - 3, high=False
            )
            if ansi:
                btext = colorize_text(btext)
            bprint = bprint + btext

            ################################
            #  side b power and toughness  #
            ################################

            pt_fmt = "{:s}{:>{inner_width_b!s}s}{:s}{:s}"
            if power is not None:
                pt = "{!s}/{!s}".format(power, toughness)
            else:
                pt = ""
            bprint.append(
                pt_fmt.format(
                    " " * pad, pt, " " * pad, "│", inner_width_b=inner_width_b
                )
            )

            ##########################
            #  side b bottom border  #
            ##########################

            bottom_fmt = "{:s}{:s}"
            bprint.append(bottom_fmt.format("─" * (w_b - 2), "┘"))

            #######################
            #  adv_card │ side b  #
            #######################

            abprint = util.columnize(
                len(adv_card[0]), adv_card, bprint, rstrip=True
            )

            #######################################
            #  append sides a and b to cardprint  #
            #######################################

            cardprint = cardprint + abprint

        ############
        #  return  #
        ############

        return "\n".join(cardprint)

    def print_card_adventurer(
        self, height, w=36, pad=0, text_pad=1, ansi=False
    ):
        """Return print of adventure card.

        :param int  height:   height of left/right sides
        :param int  w:        width of columns of whole card
        :param int  pad:      left/right card padding
        :param int  text_pad: left/right text padding
        :param bool ansi:     whether color


                        - : text_pad

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

                      ^ ├─────────────────┬ ───────────────┤
                      | │Boulder Rush    R│                │
                      | │Instant — Adventu│                │
                      | │                 │                │
                      | │-Target creature-│                │
                      | │-gets +2/+0     -│                │
                      | │-until end of   -│ Rimrock Knight │
               height | │-turn. (Then    -│ can't block.   │
                      | │-exile this     -│                │
                      | │-card. You may  -│                │
                      | │-cast the       -│                │
                      | │-creature later -│                │
                      | │-from exile.)   -│                │
                      | │                 │             3/1│
                      v └─────────────────┴ ───────────────┘
                        <---------------------------------->
                                        w

        """
        ###############
        #  arguments  #
        ###############

        name = self.name
        manacost = self.manacost
        types = self.type
        text = self.text

        if name == "":
            raise ValueError("name empty")
        if type(manacost) != str:
            raise ValueError("invalid mana cost")

        ###########
        #  color  #
        ###########

        mcolor_shift = 0

        if ansi:
            [manacost, mcolor_shift] = colorize_mana(manacost, mcolor_shift)

        ##################
        #  measurements  #
        ##################

        w = floor(w / 2) + 1
        inner_width = w - 2 - pad * 2

        if manacost is None:
            manacost = ""
        if manacost != "":
            name_len = inner_width - len(self.manacost) - 2
            mana_len = len(self.manacost) + 2 + mcolor_shift
        else:
            mana_len = 0
            name_len = inner_width

        types_len = inner_width

        ###################
        #  create spacer  #
        ###################

        spacer_fmt = "{:s}{:s}{:s}"
        adv_spacer = spacer_fmt.format("│", " " * (w - 2), "│")

        ######################
        #  CREATE PRINTCARD  #
        ######################

        cardprint = []

        ################
        #  top border  #
        ################

        top_fmt = "{:s}{:s}{:s}"
        cardprint.append(top_fmt.format("├", "─" * (w - 2), "┬"))

        ##########
        #  name  #
        ##########

        # card.append( '│{:<27s}{:>7s}│'.format(name, manacost) )
        name_fmt = "{:s}{:<{name_len!s}s}{:>{mana_len!s}s}{:s}"
        cardprint.append(
            name_fmt.format(
                "│",
                name[:name_len],
                manacost,
                "│",
                name_len=name_len,
                mana_len=mana_len,
            )
        )

        ###########
        #  types  #
        ###########

        types_fmt = "{:s}{:<{types_len!s}s}{:s}"
        cardprint.append(
            types_fmt.format("│", types[:types_len], "│", types_len=types_len)
        )

        ############
        #  spacer  #
        ############

        cardprint.append(adv_spacer)

        ##########
        #  text  #
        ##########

        #    ├─────────────────┬
        #    │Stomp          1R│
        #    │Instant — Adventu│
        #    │                 │
        #  1 │                 │
        #  2 │ Damage can’t be │
        #  3 │ prevented this  │
        #  4 │ turn. Stomp     │
        #  5 │ deals 2 damage  │
        #  6 │ to any target.  │
        #  7 │                 │
        #  8 │                 │
        #  9 │                 │
        #    │                 │
        #    └─────────────────┴

        # get text lines with left-right border
        atext = util.card_inscribe(text, w=w, text_pad=text_pad)

        # add spacers to center text, to fill `height-6` lines
        alines = len(atext)
        atextlines = height - 6
        ftext = util.card_text_center(atext, adv_spacer, atextlines, high=True)

        # add text
        cardprint = cardprint + ftext

        ############
        #  spacer  #
        ############

        cardprint.append(adv_spacer)

        ###################
        #  bottom border  #
        ###################

        bottom_fmt = "{:s}{:s}{:s}"
        cardprint.append(bottom_fmt.format("└", "─" * (w - 2), "┴"))

        ############
        #  return  #
        ############

        return "\n".join(cardprint)

    def print_card_flip(
        self,
        w=36,
        pad=0,
        img_pad=2,
        text_pad=1,
        min_text=6,
        image=True,
        ansi=False,
    ):
        """Return print of card.

        :param int  w:        width of columns of whole card
        :param int  pad:      left/right card padding
        :param int  img_pad:  left/right image padding
        :param int  text_pad: left/right text padding
        :param int  min_text: minimum text line count
        :param bool image:    whether to print image
        :param bool ansi:     whether color


                        | : text line count (10)

                        ┌──────────────────────────────────┐
                        │Akki Lavarunner                 3R│
                        │                                  │
                      | │ Haste                            │
                      | │                                  │
                      | │ Whenever Akki Lavarunner deals   │
                      | │ damage to an opponent, flip it.  │
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
                      | │ Protection from red              │
                      | │                                  │
                      | │ If a red source would deal       │
                      | │ damage to a player, it deals     │
                      | │ that much damage plus 1 to that  │
                      | │ player instead.                  │
                        │                                  │
                        │Tok-Tok, Volcano Born          CHK│
                        └──────────────────────────────────┘

        """
        ###############
        #  arguments  #
        ###############

        a_name = self.name
        a_manacost = self.manacost
        a_types = self.type
        a_setcode = self.setcode
        a_power = self.power
        a_toughness = self.toughness
        a_rarity = self.rarity
        a_text = self.text

        if self.otherfaces:
            sideb = self.otherfaces[0]
        else:
            raise ValueError("card has no other faces for print")

        b_name = sideb.name
        b_types = sideb.type
        b_power = sideb.power
        b_toughness = sideb.toughness
        b_text = sideb.text

        if a_manacost is None:
            a_manacost = ""
        if a_power is None:
            a_power = ""
        if b_power is None:
            b_power = ""
        if a_toughness is None:
            a_toughness = ""

        if a_name == "":
            raise ValueError("name empty")
        if type(a_manacost) != str:
            raise ValueError("invalid mana cost")

        ###########
        #  color  #
        ###########

        mcolor_shift = 0
        rcolor_shift = 0

        if ansi:

            if a_manacost != "":
                [a_manacost, mcolor_shift] = colorize_mana(
                    a_manacost, mcolor_shift
                )
            if a_rarity:
                [a_setcode, rcolor_shift] = colorize_rarity(
                    a_rarity, a_setcode, rcolor_shift
                )

        ##################
        #  measurements  #
        ##################

        inner_width = w - 2 - pad * 2

        if a_manacost != "":
            a_name_len = inner_width - len(self.manacost) - 2
            mana_len = len(self.manacost) + 2 + mcolor_shift
        else:
            mana_len = 0
            a_name_len = inner_width

        image_width = w - img_pad * 2 - 2
        image_height = round(image_width * 0.3)

        if a_power != "":
            a_types_len = (
                inner_width - len(a_power) - len(a_toughness) - 1 - 2 - pad
            )
            a_pt_len = len(a_power) + len(a_toughness) + 1 + 2
        else:
            a_pt_len = 0
            a_types_len = inner_width - pad

        if b_power != "":
            b_types_len = (
                inner_width - len(b_power) - len(b_toughness) - 1 - 2 - pad
            )
            b_pt_len = len(b_power) + len(b_toughness) + 1 + 2
        else:
            b_pt_len = 0
            b_types_len = inner_width - pad

        if a_setcode != "":
            b_name_len = inner_width - len(self.setcode) - 2 - pad
            setcode_len = len(self.setcode) + 2 + rcolor_shift

        ###################
        #  create spacer  #
        ###################

        spacer_fmt = "{:s}{:s}{:s}"
        flip_spacer = spacer_fmt.format("│", " " * (w - 2), "│")

        ##################
        #  text heights  #
        ##################

        a_ftext = util.card_inscribe(a_text, w=w, pad=pad, text_pad=text_pad)
        b_ftext = util.card_inscribe(b_text, w=w, pad=pad, text_pad=text_pad)

        a_theight = len(a_ftext)
        b_theight = len(b_ftext)

        ceilmin = ceil(min_text / 2)
        floormin = min_text - ceilmin
        a_min_text = a_theight
        b_min_text = b_theight

        if a_theight + b_theight < min_text:
            if a_theight >= ceilmin:
                b_min_text = min_text - a_min_text
            elif b_theight >= floormin:
                a_min_text = min_text - b_theight
            else:
                a_min_text = ceilmin
                b_min_text = floormin

        ######################
        #  CREATE PRINTCARD  #
        ######################

        cardprint = []

        ################
        #  top border  #
        ################

        top_fmt = "{:s}{:s}{:s}"
        cardprint.append(top_fmt.format("┌", "─" * (w - 2), "┐"))

        ##############
        #  top name  #
        ##############

        name_fmt = "{:s}{:<{name_len!s}s}{:>{mana_len!s}s}{:s}"
        cardprint.append(
            name_fmt.format(
                "│",
                a_name[:a_name_len],
                a_manacost,
                "│",
                name_len=a_name_len,
                mana_len=mana_len,
            )
        )

        ############
        #  spacer  #
        ############

        cardprint.append(flip_spacer)

        ###################
        #  top card text  #
        ###################

        if ansi:
            a_ftext = colorize_text(a_ftext)
        cardprint = cardprint + a_ftext

        #############################
        #  top text minimum height  #
        #############################

        for i in range(0, a_min_text - a_theight):
            cardprint.append(flip_spacer)

        ############
        #  spacer  #
        ############

        cardprint.append(flip_spacer)

        ###############
        #  top types  #
        ###############

        types_fmt = "{:s}{:<{types_len!s}s}{:>{pt_len!s}s}{:s}"
        if a_power:
            pt = "{!s}/{!s}".format(a_power, a_toughness)
        else:
            pt = ""
        cardprint.append(
            types_fmt.format(
                "│",
                a_types[:a_types_len],
                pt,
                "│",
                types_len=a_types_len,
                pt_len=a_pt_len,
            )
        )

        ###########
        #  image  #
        ###########

        if image:
            image_fmt = "{:s}{:^{inner_width!s}s}{:s}"
            for i in range(image_height):
                cardprint.append(
                    image_fmt.format(
                        "│", "/" * image_width, "│", inner_width=inner_width
                    )
                )

        ##################
        #  bottom types  #
        ##################

        types_fmt = "{:s}{:<{types_len!s}s}{:>{pt_len!s}s}{:s}"
        if b_power:
            pt = "{!s}/{!s}".format(b_power, b_toughness)
        else:
            pt = ""
        cardprint.append(
            types_fmt.format(
                "│",
                b_types[:b_types_len],
                pt,
                "│",
                types_len=b_types_len,
                pt_len=b_pt_len,
            )
        )

        ############
        #  spacer  #
        ############

        cardprint.append(flip_spacer)

        ######################
        #  bottom card text  #
        ######################

        if ansi:
            b_ftext = colorize_text(b_ftext)
        cardprint = cardprint + b_ftext

        ################################
        #  bottom text minimum height  #
        ################################

        for i in range(0, b_min_text - b_theight):
            cardprint.append(flip_spacer)

        ############
        #  spacer  #
        ############

        cardprint.append(flip_spacer)

        #################
        #  bottom name  #
        #################

        name_fmt = "{:s}{:<{name_len!s}s}{:>{setcode_len!s}s}{:s}"
        cardprint.append(
            name_fmt.format(
                "│",
                b_name[:b_name_len],
                a_setcode,
                "│",
                name_len=b_name_len,
                setcode_len=setcode_len,
            )
        )

        ################################
        #  regular card bottom border  #
        ################################

        bottom_fmt = "{:s}{:s}{:s}"
        cardprint.append(bottom_fmt.format("└", "─" * (w - 2), "┘"))

        ############
        #  return  #
        ############

        return "\n".join(cardprint)

    def print_card_split(
        self,
        w=36,
        pad=0,
        img_pad=2,
        text_pad=1,
        min_text=0,
        image=True,
        wide=False,
        ansi=False,
    ):
        """Return print of card.

        :param int  w:        width of columns of whole card
        :param int  pad:      left/right card padding
        :param int  img_pad:  left/right image padding
        :param int  text_pad: left/right text padding
        :param int  min_text: minimum text line count
        :param bool image:    whether to print image
        :param bool ansi:     whether color
        :param bool wide:     whether to use extra columns for two faces


        image:

                | : text line count (12)

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
              | │ Flip a coin. If │ Target player  │
              | │ it comes up     │ sacrifices two │
              | │ heads, counter  │ attacking      │
              | │ target instant  │ creatures.     │
              | │ or sorcery      │                │
              | │ spell. If it    │                │
              | │ comes up tails, │                │
              | │ copy that spell │                │
              | │ and you may     │                │
              | │ choose new      │                │
              | │ targets for the │                │
              | │ copy.           │                │
                │                 │                │
                └─────────────────┴────────────────┘

        compact:

                | : text line count (10)

                ┌──────────────────────────────────┐
                │Odds                            UR│
                │                                  │
                │                                  │
                │Instant                        DIS│
                │                                  │
              | │ Flip a coin. If it comes up      │
              | │ heads, counter target instant or │
              | │ sorcery spell. If it comes up    │
              | │ tails, copy that spell and you   │
              | │ may choose new targets for the   │
              | │ copy.                            │
                │                                  │
                ├──────────────────────────────────┤
                │Ends                           3RW│
                │                                  │
                │                                  │
                │Instant                        DIS│
                │                                  │
              | │ Target player sacrifices two     │
              | │ attacking creatures.             │
              | │                                  │
                │                                  │
                └──────────────────────────────────┘


        wide:

                | : text line count (7)

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
              | │ Flip a coin. If it comes up │ Target player sacrifices   │
              | │ heads, counter target       │ two attacking creatures.   │
              | │ instant or sorcery spell.   │                            │
              | │ If it comes up tails, copy  │                            │
              | │ that spell and you may      │                            │
              | │ choose new targets for the  │                            │
              | │ copy.                       │                            │
                │                             │                            │
                └─────────────────────────────┴────────────────────────────┘

        """
        ###############
        #  arguments  #
        ###############

        if self.otherfaces:
            sideb = self.otherfaces[0]
        else:
            raise ValueError("card has no other faces for print")

        ##################
        #  left | right  #
        ##################
        if (image) or (not image and wide):

            if wide:
                w = round(w * 1.67)

            # widths
            w_a = floor(w / 2 + 1)
            w_b = w - w_a + 1

            # max text height of sides
            a_height = util.height(
                self,
                w=w_a,
                img_pad=img_pad,
                min_text=min_text,
                image=image,
                single_side=True,
            )
            b_height = util.height(
                sideb,
                w=w_b,
                img_pad=img_pad,
                min_text=min_text,
                image=image,
                single_side=True,
            )
            a_theight = util.text_height(
                a_height, "normal", w_a, img_pad, image
            )
            b_theight = util.text_height(
                b_height, "normal", w_b, img_pad, image
            )
            max_theight = max([a_theight, b_theight])

            # get prints
            left = self.print_card(
                w=w_a,
                pad=pad,
                img_pad=img_pad,
                text_pad=text_pad,
                image=image,
                min_text=max_theight,
                single_side=True,
                ansi=ansi,
            ).splitlines()
            right = sideb.print_card(
                w=w_b,
                pad=pad,
                img_pad=img_pad,
                text_pad=text_pad,
                min_text=max_theight,
                image=image,
                single_side=True,
                ansi=ansi,
            ).splitlines()

            # alter cards for split format
            left = [l[:-1] for l in left]
            right[0] = "┬" + right[0][1:]
            right[-1] = "┴" + right[-1][1:]

            # equalize image heights
            left_iheight = round((w_a - img_pad * 2 - 2) * 0.37)
            right_iheight = round((w_b - img_pad * 2 - 2) * 0.37)
            add = abs(left_iheight - right_iheight)
            for i in range(add):
                if right_iheight < left_iheight:
                    right.insert(3, right[3])
                else:
                    left.insert(3, left[3])

            # get card print
            cardprint = util.columnize(len(left[0]), left, right, sep=0)

            # fusion
            fuse_txt = """
            Fuse (You may cast one or both halves of this card from your hand.)
            """.strip()
            if re.search("Fuse", "\n".join(cardprint)):
                ln_col1 = None
                ln_col2 = None
                a_col = []
                b_col = []
                for i, l in enumerate(cardprint):

                    # if re.match(r'└─*┘$', l):
                    if re.match(r"└", l):
                        last = i
                        break

                    match = re.findall("│ Fuse", l)
                    if match:
                        if len(match) == 2:
                            ln_col1 = i
                            ln_col2 = i
                        else:
                            if re.match("^│ Fuse", l):
                                ln_col1 = i
                                a_col = []
                            else:
                                ln_col2 = i
                                b_col = []

                    if ln_col1:
                        cols = re.match(r"│ ([^│]*) │ ([^│]*) │", cardprint[i])
                        if cols:
                            a_col.append(cols.group(1))

                    if ln_col2:
                        cols = re.match(r"│ ([^│]*) │ ([^│]*) │", cardprint[i])
                        if cols:
                            b_col.append(cols.group(2))

                a_col_str = re.subn(" {2,}", " ", " ".join(a_col))[0].strip()
                b_col_str = re.subn(" {2,}", " ", " ".join(b_col))[0].strip()

                if a_col_str == fuse_txt and b_col_str == fuse_txt:
                    if ln_col1 == ln_col2:
                        ln_last = ln_col1

                    if ln_col1 < ln_col2:
                        ln_last = ln_col2
                        # remove first occurence of fuse text
                        for i, l in enumerate(cardprint[ln_col1:ln_col2]):
                            inner_width = w_a - 2 - pad
                            blank_col = "│{:s}│".format(" " * inner_width)
                            row = "{:s}{:s}".format(blank_col, l[w_a:])
                            cardprint[i + ln_col1] = row

                    if ln_col2 < ln_col1:
                        ln_last = ln_col1
                        # remove first occurence of fuse text
                        for i, l in enumerate(cardprint[ln_col2:ln_col1]):
                            inner_width = w_b - 2 - pad
                            blank_col = "│{:s}│".format(" " * inner_width)
                            row = "{:s}{:s}".format(l[:w_b], blank_col)
                            cardprint[i + ln_col2] = row

                    # inscribe and find height difference before and after fuse
                    ftext = util.card_inscribe(
                        fuse_txt, w=w, pad=pad, text_pad=text_pad
                    )
                    difference = len(cardprint) - ln_last - 2 - len(ftext)
                    cardprint[ln_last:-2] = ftext

                    # min_text
                    nr_text = max_theight - difference
                    if nr_text < min_text:
                        add = min_text - nr_text
                        for i in range(add):
                            cardprint.insert(-2, cardprint[-2])

        ##########
        #   up   #
        #  ----  #
        #  down  #
        ##########
        else:

            if wide:
                raise ValueError("wide print does not support compact mode")

            top_theight = util.text_height(
                util.height(self, w, img_pad, 0, image, True),
                w,
                img_pad,
                image,
            )
            bottom_theight = util.text_height(
                util.height(sideb, w, img_pad, 0, image, True),
                w,
                img_pad,
                image,
            )

            # get min_text
            ceilmin = ceil(min_text / 2)
            floormin = min_text - ceilmin
            top_min_text = top_theight
            bottom_min_text = bottom_theight

            if top_theight + bottom_theight < min_text:
                if top_theight >= ceilmin:
                    bottom_min_text = min_text - top_min_text
                elif bottom_theight >= floormin:
                    top_min_text = min_text - bottom_theight
                else:
                    top_min_text = ceilmin
                    bottom_min_text = floormin

            # get cards
            top = self.print_card(
                w=w,
                pad=pad,
                img_pad=img_pad,
                text_pad=text_pad,
                image=image,
                min_text=top_min_text,
                single_side=True,
                ansi=ansi,
            ).splitlines()
            bottom = sideb.print_card(
                w=w,
                pad=pad,
                img_pad=img_pad,
                text_pad=text_pad,
                min_text=bottom_min_text,
                image=image,
                single_side=True,
                ansi=ansi,
            ).splitlines()

            # alter cards for split format
            top.pop()
            bottom[0] = "├" + bottom[0][1:]
            bottom[0] = bottom[0][0:-1] + "┤"

            # get card print
            cardprint = top + bottom

        return "\n".join(cardprint)

    def print_card_transform(
        self,
        w=36,
        pad=0,
        img_pad=2,
        text_pad=1,
        min_text=6,
        image=True,
        wide=False,
        ansi=False,
    ):
        """Return print of card.

        :param int  w:        width of columns of whole card
        :param int  pad:      left/right card padding
        :param int  img_pad:  left/right image padding
        :param int  text_pad: left/right text padding
        :param int  min_text: minimum text line count
        :param bool image:    whether to print image
        :param bool ansi:     whether color
        :param bool wide:     whether to show both faces side by side

        """
        ###############
        #  arguments  #
        ###############

        if self.otherfaces:
            sideb = util.get_transform_meld_sideb(self)
        else:
            raise ValueError("card has no other faces for print")

        if wide:

            text_height = util.text_height_of_highest(
                self, sideb, w=w, img_pad=img_pad, min_text=0, image=image
            )[0]
            aprint = self.print_card(
                w=w,
                pad=pad,
                img_pad=img_pad,
                text_pad=text_pad,
                image=image,
                min_text=text_height,
                single_side=True,
                ansi=ansi,
            ).splitlines()
            bprint = sideb.print_card(
                w=w,
                pad=pad,
                img_pad=img_pad,
                text_pad=text_pad,
                image=image,
                min_text=text_height,
                single_side=True,
                ansi=ansi,
            ).splitlines()
            cardprint = util.columnize(w, aprint, bprint)

        else:

            aprint = self.print_card(
                w=w,
                pad=pad,
                img_pad=img_pad,
                text_pad=text_pad,
                image=image,
                min_text=min_text,
                single_side=True,
                ansi=ansi,
            ).splitlines()
            # bprint = sideb.print_card(w=w, pad=pad, img_pad=img_pad,
            #             text_pad=text_pad, image=image, min_text=min_text,
            #             single_side=True, ansi=ansi).splitlines()
            # cardprint = aprint + bprint
            cardprint = aprint

        return "\n".join(cardprint)
