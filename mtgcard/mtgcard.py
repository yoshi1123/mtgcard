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

"""Core functionality."""


from mtgcard import settings
from mtgcard.card import Card
from mtgcard.colors import color, colorize_mana, colorize_format, hdr
from mtgcard.parser import parser
from mtgcard import util


def get_and_print_card(
    db,
    name=None,
    setcode=None,
    format=None,
    w=36,
    min_text=6,
    image=True,
    ansi=True,
    verbose=False,
    rulings=False,
    card=None,
):
    """Return print of card `name` from `setcode` and/or format else None.

    :param MTGDatabase db:       database
    :param str         name:     exact name of card (not case sensitive)
    :param str         setcode:  set code of card
    :param str         format:   format card is legal in
    :param int         w:        width of card print
    :param int         min_text: minimum height of card text
    :param bool        image:    whether to include images
    :param bool        ansi:     whether color
    :param bool        verbose:  whether to display additional card information
    :param bool        rulings:  whether to display rulings
    :param Card        card:     Card instead of name and/or setcode

    """
    if not card:
        c = db.get_card(
            name, setcode, format, verbose=verbose, rulings=rulings
        )
    else:
        c = card

    card_print = c.print_card(
        w=w, min_text=min_text, image=image, ansi=ansi, wide=verbose
    )

    if verbose or rulings:
        card_print += "\n"

    if verbose:

        # price
        section = "Price ({:s}):".format(settings.CURRENCY)
        section = hdr(section) if ansi else section
        price = (
            "${:.2f}".format(c.price * settings.US_TO_CUR_RATE)
            if c.price is not None
            else ""
        )
        sec_price = ""
        sec_price += "\n{} {:s}".format(section, price)
        sec_price += "\n"
        card_print += sec_price

        # # printings
        #
        # main_sets = [ "THB", "ELD", "M20", "WAR", "RNA", "GRN", "M19", "DOM",
        # "RIX", "XLN", "HOU", "AKH", "AER", "KLD", "EMN", "SOI", "OGW", "BFZ",
        # "ORI", "DTK", "FRF", "KTK", "M15", "JOU", "BNG", "THS", "M14", "DGM",
        # "GTC", "RTR", "M13", "AVR", "DKA", "ISD", "M12", "NPH", "MBS", "SOM",
        # "M11", "ROE", "WWK", "ZEN", "M10", "ARB", "CON", "ALA", "EVE", "SHM",
        # "MOR", "LRW", "10E", "FUT", "PLC", "TSB", "TSP", "CSP", "DIS", "GPT",
        # "RAV", "9ED", "SOK", "BOK", "CHK", "5DN", "DST", "MRD", "8ED", "SCG",
        # "LGN", "ONS", "JUD", "TOR", "ODY", "APC", "7ED", "PLS", "INV", "PCY",
        # "NEM", "MMQ", "UDS", "6ED", "ULG", "USG", "EXO", "STH", "TMP", "WTH",
        # "5ED", "VIS", "MIR", "ALL", "HML", "ICE", "4ED", "FEM", "DRK", "LEG",
        # "SUM", "3ED", "ATQ", "2ED", "ARN", "LEB", "LEA", ]
        #
        # section = 'Core/expansion printings:'
        # sets_main_new_to_old = [
        #         i for i in settings.main_sets if i in c.printings]
        # sets_main_new_to_old = wrap(' '.join(sets_main_new_to_old), w-4)
        # sets_main_new_to_old = ['  '+l for l in sets_main_new_to_old]
        # sec_onlyprintings = ''
        # sec_onlyprintings += '\n{}\n\n'.format(hdr(section) \
        #          if ansi else section)
        # sec_onlyprintings += '{:s}\n'.format('\n'.join(sets_main_new_to_old))
        # card_print += sec_onlyprintings

        # printings and prices
        sets = db.get_sets()
        sec_printings = ""
        # sec_printings += ' '*72 + '|'
        section = "Printings ({:s}):".format(settings.CURRENCY)
        sec_printings += "\n{}\n\n".format(hdr(section) if ansi else section)
        prices = db.get_price(c.name, token=c.types[0] == "Token")
        sec_printings += "\n".join(
            util.printings_print(prices, sets, ansi=ansi)
        )
        sec_printings += "\n"
        card_print += sec_printings

        # formats
        section = "Formats:"
        sec_formats = ""
        sec_formats += "\n{}\n".format(hdr(section) if ansi else section)
        sec_formats += "\n"
        formats = ["  " + l for l in util.legality_print(c.formats, ansi=ansi)]
        sec_formats += "\n".join(formats)
        card_print += sec_formats

    if rulings:

        if verbose:
            card_print += "\n"

        # rulings
        nr_rulings = len(c.rulings) if c.rulings else 0
        if nr_rulings == 0:
            card_print += "\nNo rulings."
        else:
            section = "Rulings:"
            sec_rulings = ""
            sec_rulings += "\n{}\n\n".format(hdr(section) if ansi else section)
            sec_rulings += "\n".join(
                util.rulings_print(c.rulings, w, ansi=ansi)
            )
            card_print += sec_rulings

    return card_print


def list_cards_images(
    cards,
    columns,
    w=36,
    img_pad=2,
    text_pad=1,
    min_text=6,
    image=True,
    ansi=True,
):
    """List `cards` as images.

    :param list cards:    list of Card objects
    :param int  columns:  number of columns per row
    :param int  w:        width of card prints
    :param int  img_pad:  left/right image padding
    :param int  text_pad: left/right text padding
    :param int  min_text: minimum text line count
    :param bool image:    include images
    :param bool ansi:     whether color

    """
    images = []

    # extract double faced cards (transform/meld)
    cards_expand = []
    for c in cards:
        cards_expand.append(c)
        if c.layout in ("transform", "meld"):
            cards_expand.append(util.get_transform_meld_sideb(c))

    # create list of rows
    # [ [c1, c2], [c3, c4], ... ]
    card_prints = []
    row = []
    for i, c in enumerate(cards_expand):
        if i % columns == 0:
            if row:
                card_prints.append(row)
            row = []
        row.append(c)
    if row:
        card_prints.append(row)

    # for each row of Cards, print them at same height and append to result
    for row in card_prints:

        # get text height of card with max height
        adv_side_a = True
        if c.layout == "adventure":
            adv_side_a = util.highest_adv_side_a(c, w=w, text_pad=text_pad)
        text_height_high, c = util.text_height_of_highest(
            *row, w=w, img_pad=img_pad, min_text=min_text, image=image
        )

        # normalize text height
        # - 'normalizer' is the the line count difference between a normal card
        #   and another card with the same text height
        image_width = w - img_pad * 2 - 2
        norm_iheight = round(image_width * 0.37)
        flip_iheight = round(image_width * 0.3)
        split_iheight = util.split_image_height(w, img_pad=img_pad)
        normalizers = {
            "flip": lambda: 2 - (norm_iheight - flip_iheight) * int(image),
            "split": lambda: split_iheight - norm_iheight if image else 7,
            "aftermath": lambda: split_iheight - norm_iheight if image else 7,
            "adventure": lambda: 3 if adv_side_a else 1,
        }
        layout = "normal" if c.side is None else c.layout
        add = normalizers.get(layout, lambda: 0)()
        max_theight = text_height_high + add

        # row of 'card as list' with aligned heights
        row_prints = []
        for c in row:
            if c.layout == "adventure":
                adv_side_a = util.highest_adv_side_a(c)
            layout = "normal" if c.side is None else c.layout
            add = normalizers.get(layout, lambda: 0)()
            theight = max_theight - add
            card_print = c.print_card(
                w=w, img_pad=img_pad, min_text=theight, image=image, ansi=ansi
            ).splitlines()
            if c.layout in ("transform", "meld") and c.side == "a":
                card_print[2] = card_print[2][0:-1] + ">"
            if c.layout in ("transform", "meld") and c.side != "a":
                card_print[2] = "<" + card_print[2][1:]
            row_prints.append(card_print)

        # concatenate cards as lists
        row_print_list = util.columnize(w, *row_prints, sep=2)

        # append to result
        images = images + row_print_list

    return images


def list_cards_detailed(
    cards,
    header=True,
    lname=32,
    lset=5,
    lmana=15,
    ltype=14,
    lptl=7,
    lr=3,
    ansi=True,
):
    """List `cards` as rows of details.

    :param list cards : list of Card objects
    :param bool header: whether to display header
    :param str lname  : width of name column
    :param str lset   : width of set column
    :param str lmana  : width of mana column
    :param str ltype  : width of type column
    :param str lptl   : width of power/toughness/loyalty column
    :param str lr     : width of rarity column
    :param str ansi   : width of ansi column

    """
    details = []
    fmt_details = """
{:{lname!s}s}{:{lset!s}s}{:{lmana!s}s}{:{ltype!s}s}{:{lptl!s}s}{:{lr!s}s}{:s}
""".strip()
    if header:
        details.append(
            fmt_details.format(
                "NAME",
                "SET",
                "MANA",
                "TYPE",
                "PT|L",
                "R",
                settings.CURRENCY,
                lname=lname,
                lset=lset,
                lmana=lmana,
                ltype=ltype,
                lptl=lptl,
                lr=lr,
            )
        )

    for c in cards:

        # name
        name = util.multi_name(c)

        # set
        set = c.setcode

        # mana
        if c.names:
            manacost = []
            faces = [c] + c.otherfaces
            if c.side:
                faces.sort(key=lambda f: f.side)
            manacost = [
                f.manacost
                for f in faces
                if c.layout != "meld"
                or (f.side == c.side or c.layout == "meld" and f.side == "c")
            ]
            mana = " // ".join([m for m in manacost if m is not None])
        else:
            mana = c.manacost if c.manacost is not None else ""
        if ansi:
            mana_shift = 0
            mana, mana_shift = colorize_mana(mana[:lmana], mana_shift)
            lmanas = lmana + mana_shift
        else:
            lmanas = lmana

        # type
        supertype = c.types[0]

        # pt|l
        if c.power:
            ptl = "{:s}/{:s}".format(c.power, c.toughness)
        elif c.loyalty:
            ptl = "{:s}".format(c.loyalty)
        else:
            ptl = ""

        # r
        if c.rarity:
            r = {"mythic": "M", "rare": "R", "uncommon": "U", "common": "C",
                    "special": "S"}[
                c.rarity
            ]
        else:
            r = ""

        # price
        price = (
            "${:.2f}".format(c.price * settings.US_TO_CUR_RATE)
            if c.price is not None
            else ""
        )

        # add row
        details.append(
            fmt_details.format(
                name[: lname - 2],
                set[:lset],
                mana[:lmanas],
                supertype[:ltype],
                ptl[:lptl],
                r[:lr],
                price,
                lname=lname,
                lset=lset,
                lmana=lmanas,
                ltype=ltype,
                lptl=lptl,
                lr=lr,
            )
        )

    matches = details

    return matches


def list_cards(
    db,
    query,
    image_columns=None,
    image_compact=False,
    header=True,
    onlynames=True,
    onename=True,
    sort="name",
    reverse=False,
    limit=None,
    ansi=True,
):
    """Return list of cards names matching `query` or None, and total matches.

    :param MTGDatabase db:            database
    :param str         query:         query string
    :param int         image_columns: number of images per column
    :param bool        image_compact: show compact images
    :param bool        header:        show header in detailed listing
    :param bool        onlynames:     *name listing*
    :param int         onename:       show only one name on a double faced card
    :param str         sort:          sort key (cmc, name, price, or setcode)
    :param bool        reverse:       whether sort order is reversed
    :param int         limit:         maximum amount of cards to list
    :param bool        ansi:          whether color

    There are three types of lists:

        detailed     details of cards one per line
        image        image of cards `image_columns` per line (image_columns)
        name         names of cards one per line (onlynames)

    * a true value of column in parentheses determines list type

    """
    if len(query) != 0:

        sql_query = parser.parse(query)

        # if sql_query[0] is None:
        #     # temporary:
        #     raise SyntaxError("unknown syntax error")

    else:
        # get all cards
        sql_query = ("", ())

    cards = db.get_cards(sql_query, sort=sort, reverse=reverse, limit=limit)
    if cards is None:
        return None, 0

    total = len(cards)

    if image_columns:
        # image listing

        matches = list_cards_images(
            cards, image_columns, image=not image_compact, ansi=ansi
        )

    else:

        if not onlynames:
            # line listing

            matches = list_cards_detailed(cards, header=header, ansi=ansi)

        else:
            # name listing

            matches = []
            for c in cards:
                if onename:
                    matches.append(c.name)
                else:
                    matches.append(util.multi_name(c))

    if matches and len(matches) >= 1:
        return "\n".join(matches), total
    else:
        return None, 0
