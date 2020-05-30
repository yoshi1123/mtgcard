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

"""Utilities."""


from math import ceil
from math import floor
from textwrap import wrap

from mtgcard import settings
from mtgcard.colors import colorize
from mtgcard.colors import colorize_mana, colorize_format, colorize_set


def columnize(width, *columns, sep=0, rstrip=False):
    """Return a list of colomnized text.

    :param list columns: columns from left to right
    :param int  width:   width of columns
    :param int  sep:     number of spaces separating columns
    :param bool rstrip:  whether to strip right-most whitespace

    """
    text = []
    for line in range(max(map(len, columns))):
        # 0 to number of lines of longest column
        fmt_str = ""
        fmt_args = []
        for j, c in enumerate(columns):

            # add column in line to format string
            fmt_str += "{:{width!s}s}"

            # add column if available
            fmt_args.append(c[line] if line <= len(c) - 1 else "")

            # add separator in line, if not last column, to format string
            if j < len(columns) - 1 and sep > 0:
                fmt_str += "{:{sep!s}s}"
                fmt_args.append("")

        if rstrip:
            row = fmt_str.format(*fmt_args, width=width, sep=sep).rstrip()
        else:
            row = fmt_str.format(*fmt_args, width=width, sep=sep)
        text.append(row)
    return text


def multi_name(card):
    """Return all names of card sides seperated by '//'."""
    if card.names:
        faces = [card] + card.otherfaces
        if card.side:
            faces.sort(key=lambda f: f.side)
        names = [
            f.name
            for f in faces
            if card.layout != "meld"
            or (f.side == card.side or card.layout == "meld" and f.side == "c")
        ]
        name = " // ".join(names)
    else:
        name = card.name
    return name


def height(card, w=36, img_pad=2, min_text=6, image=True, single_side=False):
    """Return height of `card`."""
    return len(
        card.print_card(
            w=w,
            img_pad=img_pad,
            min_text=min_text,
            image=image,
            single_side=single_side,
            ansi=False,
        ).splitlines()
    )


def text_height(height, layout, w=36, img_pad=2, image=True, adv_side_a=True):
    """Return the number of lines of text effecting the height of a card.

    :param int  height:     line height of card
    :param str  layout:     layout of card
    :param bool adv_side_a: whether left text side is height determining side

    `layout` can be one of the following:

        'adventure', 'aftermath', 'flip', 'split', 'transform', 'meld'

    """
    if layout in ("split", "aftermath") and image is True:
        image_height = split_image_height(w, img_pad)
    else:
        image_width = w - img_pad * 2 - 2
        image_ratio = 0.3 if layout == "flip" else 0.37
        image_height = round(image_width * image_ratio)
    non_img_height = {
        "flip": 10,
        "split": 8 if image else 15,
        "aftermath": 8 if image else 15,
        "adventure": 11 if adv_side_a else 9,
    }.get(layout, 8)
    text_height = height - (image_height * int(image) + non_img_height)
    return text_height


def card_text_center(lines, fill_line, nr_lines, high=True):
    """Return a list of text vertically centered `nr_lines` lines high.

    :param list lines:     wrapped text to vertically center
    :param str  fill_line: text filler line to add to make text `nr_lines` high
    :param int  nr_lines:  number of lines in result
    :param bool high:      prioritize text being on the high end

    """
    nr_tlines = len(lines)
    if high:
        cstart = floor((nr_lines / 2 - nr_tlines / 2))
    else:
        cstart = ceil((nr_lines / 2 - nr_tlines / 2))
    cend = cstart + nr_tlines - 1

    ftext = []
    for i in range(nr_lines):
        if nr_tlines and i >= cstart and i <= cend:
            line = i - cstart
            ftext.append(lines[line])
        else:
            ftext.append(fill_line)

    return ftext


def adv_text_height(text, w=36, pad=0, text_pad=1, side_a=True):
    """Return number of lines of specified adventure side.

    :param str  text:     text of the side
    :param int  w:        width of adventure card print
    :param int  pad:      left/right card padding
    :param int  text_pad: left/right text padding
    :param bool side_a:   whether side a (left side)

    """
    w_a = floor(w / 2) + 1
    w_b = w - w_a + 1
    w = w_a if side_a else w_b
    ftext = card_inscribe(text, w=w, pad=pad, text_pad=text_pad)
    text_height = len(ftext)
    return text_height


def split_image_height(w=36, img_pad=2):
    """Return height of split card image."""
    w_a = floor(w / 2 + 1)
    w_b = w - w_a + 1
    a_iheight = round((w_a - img_pad * 2 - 2) * 0.37)
    b_iheight = round((w_b - img_pad * 2 - 2) * 0.37)
    iheight = max([a_iheight, b_iheight])
    return iheight


def card_inscribe(
    text, w=36, pad=0, text_pad=1, left_border=True, right_border=True
):
    """Return a list of left/right bordered text.

    :param str  text:         text to be inscribed
    :param int  w:            non-bordered width + 2
    :param int  pad:          padding on left and right
    :param int  text_pad:     padding on left and right side of text
    :param bool left_border:  whether to include left border
    :param bool right_border: whether to include right border


    To combine two sides:

        card_inscribe('Lorem', w=10)                     # '| Lorem  |'
        card_inscribe('ipsum', w=10, left_border=False)  # ' ipsum  │'

            19
    <----------------->
    | Lorem  | ipsum  │
    <--------><------->
        10       9

    """
    paragraphs = text.splitlines() if text else []

    if left_border and not right_border:
        text_fmt = "{:s}{:s}{:{text_width!s}s}{:s}"
        inner_width = w - 2 - pad * 1
        lpadding = " " * (text_pad + pad)
        rpadding = " " * (text_pad)
        spacer_fmt = "{:s}{:s}"
        spacer = spacer_fmt.format("│", " " * (w - 2))
    elif not left_border and right_border:
        text_fmt = "{:s}{:{text_width!s}s}{:s}{:s}"
        inner_width = w - 2 - pad * 1
        lpadding = " " * (text_pad)
        rpadding = " " * (text_pad + pad)
        spacer_fmt = "{:s}{:s}"
        spacer = spacer_fmt.format(" " * (w - 2), "│")
    elif not left_border and not right_border:
        text_fmt = "{:s}{:{text_width!s}s}{:s}"
        inner_width = w - 2
        lpadding = " " * (text_pad)
        rpadding = " " * (text_pad)
        spacer_fmt = "{:s}{:s}"
        spacer = spacer_fmt.format("│", " " * (w - 2))

    else:
        text_fmt = "{:s}{:s}{:{text_width!s}s}{:s}{:s}"
        inner_width = w - 2 - pad * 2
        lpadding = " " * (text_pad + pad)
        rpadding = " " * (text_pad + pad)
        spacer_fmt = "{:s}{:s}{:s}"
        spacer = spacer_fmt.format("│", " " * (w - 2), "│")

    ftext = []
    for p in paragraphs:
        for i in wrap(p, inner_width - text_pad * 2):
            if left_border and not right_border:
                ftext.append(
                    text_fmt.format(
                        "│",
                        lpadding,
                        i,
                        rpadding,
                        text_width=inner_width - text_pad * 2,
                    )
                )
            elif not left_border and right_border:
                ftext.append(
                    text_fmt.format(
                        lpadding,
                        i,
                        rpadding,
                        "│",
                        text_width=inner_width - text_pad * 2,
                    )
                )
            elif not left_border and not right_border:
                ftext.append(
                    text_fmt.format(
                        lpadding,
                        i,
                        rpadding,
                        text_width=inner_width - text_pad * 2,
                    )
                )
            else:
                ftext.append(
                    text_fmt.format(
                        "│",
                        lpadding,
                        i,
                        rpadding,
                        "│",
                        text_width=inner_width - text_pad * 2,
                    )
                )
        # spacer
        ftext.append(spacer)
    if len(ftext) > 0:
        ftext.pop()

    return ftext


def get_transform_meld_sideb(card):
    """Return other face of a transform or meld card."""
    faces = card.otherfaces
    faces.sort(key=lambda f: f.side)
    if card.layout == "transform":
        sideb = faces[0]
    else:
        sideb = faces[1]
    return sideb


def highest_adv_side_a(c, w=36, text_pad=1):
    """Return if side a (left) is the card height determiner."""
    atext_height = (
        adv_text_height(
            c.otherfaces[0].text, w=w, text_pad=text_pad, side_a=True
        )
        + 6
    )  # 6 non-text lines in adv side
    btext_height = (
        adv_text_height(c.text, w=w, text_pad=text_pad, side_a=False) + 4
    )  # 4 non-text lines in main side
    return atext_height >= btext_height


def text_height_of_highest(
    *cards, w=36, img_pad=2, text_pad=1, min_text=0, image=True
):
    """Return number of lines of the highest card in `cards`.

    :param list *cards:   list of Card objects
    :param int  w:        width of card prints
    :param int  img_pad:  left/right image padding
    :param int  text_pad: left/right text padding
    :param int  min_text: minimum text line count
    :param bool image:    whether to include image in height determination

    """
    # get card heights of current row
    result = [
        (height(c, w=w, img_pad=img_pad, min_text=min_text, image=image), c)
        for c in cards
    ]

    # get text height of card with max height
    max_height, c = max(result, key=lambda r: r[0])
    adv_side_a = True
    if c.layout == "adventure":
        adv_side_a = highest_adv_side_a(c, w=w, text_pad=text_pad)
    text_height_of_highest = text_height(
        max_height,
        c.layout,
        w=w,
        img_pad=img_pad,
        image=image,
        adv_side_a=adv_side_a,
    )

    return text_height_of_highest, c


def legality_print(legality, ansi=True):
    """Return formatted list of `legality`.

    :param dict legality: key value pairs of {format: legal_status, ...}
    :param bool ansi:     whether color

    formats:

        standard
        brawl
        pioneer
        pauper
        modern
        legacy
        commander
        vintage

    legal statuses:

        legal
        banned
        restr.

    Example:

        legality_print(
                {
                    'commander': 'Legal',
                    'legacy': 'Banned',
                    'vintage': 'Restricted'
                }
        )

    """
    SHOWN_FORMATS = settings.SHOWN_FORMATS

    legal_print = []

    def limit(string, n):
        if len(string) > n:
            string = string[0:n-1] + "."
        return string

    # list of statuses of corresponding `SHOWN_FORMATS`
    legalities = []
    for f in SHOWN_FORMATS:
        legalities.append(
            limit(legality[f], 6).lower() if f in legality.keys() else ""
        )

    # get maximum format string length
    max_left = max(map(len, SHOWN_FORMATS[0::2]))
    max_right = max(map(len, SHOWN_FORMATS[1::2]))

    # get non-ansi legality strings as 'format: status'
    format_pairs = []
    for i in range(len(legalities)):
        l_fmt = SHOWN_FORMATS[i].capitalize() + ":"
        r_stat = legalities[i]
        if i % 2 == 0:
            lformat = max_left + 2
        else:
            if legalities[i]:
                lformat = max_right + 2
            else:
                lformat = len(l_fmt)
        format_pairs.append(
            "{:{lformat}}{}".format(l_fmt, r_stat, lformat=lformat)
        )

    # add legality to list
    nr_fmts = len(SHOWN_FORMATS)
    for i in range(0, nr_fmts, 2):
        if ansi:
            (l, ls) = colorize_format(
                SHOWN_FORMATS[i].capitalize(), legalities[i]
            )
            (r, rs) = colorize_format(
                SHOWN_FORMATS[i + 1].capitalize(), legalities[i + 1]
            )
            shift = ls
            if i < nr_fmts - 1:
                legal_print.append(
                    "{:{length}}{}".format(l, r, length=16 + shift)
                )
            else:
                legal_print.append(
                    "{:{length}}{}".format(l, "", length=16 + shift)
                )
        else:
            if i < nr_fmts - 1:
                legal_print.append(
                    "{:19}{}".format(format_pairs[i], format_pairs[i + 1])
                )
            else:
                legal_print.append("{:19}{}".format(format_pairs[i], ""))

    return legal_print


def printings_print(prices, set_types, ansi=True):
    """Return formatted list of set codes and prices.

    :param list prices:    list of [[setcode, price], ...]
    :param dict set_types: dict of {setcode: type, ...}
    :param bool ansi:      whether color

    Example:

        printings_print(
                [['M19', 1.00], [M20, 1.00]],
                db.get_sets()
        )

    """
    # get list of [setcode, price]
    if ansi:
        ansi_prices = []
        for p in prices:
            setcode, s_shift = colorize_set(p[0], set_types)
            if p[1] is not None:
                s_price = "(${:.2f})".format(p[1] * settings.US_TO_CUR_RATE)
                s_price, p_shift = colorize(s_price, "dark")
                item = "{:{lset}} {}".format(
                    setcode, s_price, lset=4 + s_shift
                )
                ansi_prices.append(
                    "{:{litem}}".format(item, litem=18 + s_shift + p_shift)
                )
            else:
                ansi_prices.append("{:{w}}".format(setcode, w=18 + s_shift))
        prices = ansi_prices
    else:
        prices = [
            "{:4} ({:.2f})".format(
                p[0]
                + ("*" if set_types[p[0]] in ("core", "expansion") else ""),
                p[1] * settings.US_TO_CUR_RATE,
            )
            if p[1] is not None
            else "{:4}".format(
                p[0]
                + ("*" if set_types[p[0]] in ("core", "expansion") else "")
            )
            for p in prices
        ]

    nr = len(prices)

    fourth = ceil(nr / 4)
    c1 = prices[0:fourth]
    c2 = prices[fourth:fourth*2]
    c3 = prices[fourth*2:fourth*3]
    c4 = prices[fourth*3:]
    fprices = columnize(18, c1, c2, c3, c4, rstrip=True)

    fprices = ["  " + l for l in fprices]

    return fprices


def rulings_print(rulings, w=36, ansi=True):
    """Return formatted two column list of rulings.

    :param list rulings: list of {'date': YYYY-MM-DD, 'text': text}
    :param int  w:       width of columns
    :param bool ansi:    whether color

    Example:

        rulings_print(card.rulings)

    """
    nr_rulings = len(rulings) if rulings else 0
    count_col1 = ceil(nr_rulings / 2)
    col1 = rulings[0:count_col1]
    col2 = rulings[count_col1:]
    wcols = [[], []]
    for i, c in enumerate([col1, col2]):
        for r in c:
            wcols[i].extend(wrap(r["text"], w - 2))
            date = "({:s})".format(r["date"])
            if ansi:
                date, shift = colorize(date, "dark")
            else:
                shift = 0
            wcols[i].append("{:{w}}".format(date, w=shift + w))
            wcols[i].append("")
        if len(wcols[i]) > 0:
            wcols[i].pop()
    frulings = columnize(w, wcols[0], wcols[1], rstrip=False)

    frulings = ["  " + l for l in frulings]

    return frulings
