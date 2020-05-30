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

"""ANSI color."""


import re

bg = False


class color:
    """General colors."""

    NC = "\033[0m"

    header = "\033[0m"

    dark = "\033[1;38;5;243m"
    coreexp = "\033[1;38;5;146m"
    black = "\033[0;38;5;0m"


class mcolor:
    """Mana colors."""

    W = "\033[1;38;5;230m"
    U = "\033[1;38;5;153m"
    B = "\033[1;38;5;247m"
    R = "\033[1;38;5;216m"
    G = "\033[1;38;5;115m"
    C = "\033[1;38;5;253m"
    X = "\033[1;38;5;253m"

    darkW = "\033[1;38;5;229m"
    darkU = "\033[1;38;5;19m"
    darkB = "\033[1;38;5;235m"
    darkR = "\033[1;38;5;160m"
    darkG = "\033[1;38;5;22m"

    WU = "\033[1;38;5;230m\033[1;38;5;19m"
    UB = "\033[1;48;5;153m\033[1;38;5;235m"
    RB = "\033[1;48;5;216m\033[1;38;5;235m"
    GR = "\033[1;48;5;115m\033[1;38;5;160m"
    WG = "\033[1;48;5;230m\033[1;38;5;22m"
    WB = "\033[1;48;5;230m\033[1;38;5;235m"
    UR = "\033[1;48;5;153m\033[1;38;5;160m"
    GB = "\033[1;48;5;115m\033[1;38;5;235m"
    WR = "\033[1;48;5;230m\033[1;38;5;160m"
    GU = "\033[1;48;5;115m\033[1;38;5;19m"


class rcolor:
    """Rarity colors."""

    C = "\033[1;38;5;231m"

    if not bg:

        U = "\033[1;38;5;152m"
        R = "\033[1;38;5;222m"
        M = "\033[1;38;5;208m"
        midU = "\033[1;38;5;110m"
        midR = "\033[1;38;5;220m"
        midM = "\033[1;38;5;166m"
        darkU = "\033[1;38;5;67m"
        darkR = "\033[1;38;5;136m"
        darkM = "\033[1;38;5;160m"

    else:

        U = "\033[1;48;5;152m\033[1;38;5;232m"
        R = "\033[1;48;5;222m\033[1;38;5;232m"
        M = "\033[1;48;5;208m\033[1;38;5;232m"
        midU = "\033[1;48;5;110m\033[1;38;5;232m"
        midR = "\033[1;48;5;220m\033[1;38;5;232m"
        midM = "\033[1;48;5;166m\033[1;38;5;232m"
        darkU = "\033[1;48;5;67m\033[1;38;5;232m"
        darkR = "\033[1;48;5;136m\033[1;38;5;232m"
        darkM = "\033[1;48;5;160m\033[1;38;5;232m"


class lcolor:
    """Legality colors."""

    legal = "\033[0;38;5;28m"
    banned = "\033[0;38;5;1m"
    restricted = "\033[0;38;5;25m"
    notlegal = "\033[0;38;5;0m"


"""*
def colorize_mana(manacost, color_shift):

    opt_mana = [{'str':'WB', 'co':'!@', 'r':re.compile('W/B|B/W')},
                {'str':'UB', 'co':'@#', 'r':re.compile('U/B|B/U')},
                {'str':'RB', 'co':'$#', 'r':re.compile('R/B|B/R')},
                {'str':'GR', 'co':'%$', 'r':re.compile('G/R|R/G')},
                {'str':'WG', 'co':'!%', 'r':re.compile('W/G|G/W')},
                {'str':'WB', 'co':'!#', 'r':re.compile('W/B|B/W')},
                {'str':'UR', 'co':'@$', 'r':re.compile('U/R|R/U')},
                {'str':'GB', 'co':'%#', 'r':re.compile('G/B|B/G')},
                {'str':'WR', 'co':'!$', 'r':re.compile('W/R|R/W')},
                {'str':'GU', 'co':'%@', 'r':re.compile('G/U|U/G')}]

    def encode(str):
        return "".join([ chr(ord(i)+100) for i in str ])

    for m in ['C']:

        r = '[0-9]' if m == 'C' else m
        c = getattr(mcolor, m)

        r_mana = re.compile(r'({:s})'.format(r))
        repl = r'{:s}\1{:s}'.format(c, color.NC)
        (manacost, count) = re.subn(r_mana, repl, manacost)
        color_shift += ( len(c) + len(color.NC) ) * count

    for m in opt_mana:
        c = getattr(mcolor, m['str'])
        cmana = '{:s}{:s}{:s}'.format(c, encode(m['str'][-1]), color.NC)
        (manacost, count) = re.subn(m['r'], cmana, manacost)
        color_shift += ( len(c) + len(color.NC) ) * count

    for m in ['W', 'U', 'B', 'R', 'G']:

        r = '[0-9]' if m == 'C' else m
        c = getattr(mcolor, m)

        r_mana = re.compile(r'({:s})'.format(r))
        repl = r'{:s}\1{:s}'.format(c, color.NC)
        (manacost, count) = re.subn(r_mana, repl, manacost)
        color_shift += ( len(c) + len(color.NC) ) * count

    for char in "WUBRG":
        (manacost,count) = re.subn('{:s}'.format(encode(char)), char, manacost)

    return [manacost, color_shift]
*"""


def colorize_mana(manacost, color_shift):
    """Return colored `manacost` and the `color_shift` as a list.

    :param str manacost:    mana cost (e.g., "1W") to colorize
    :param int color_shift: value to add the coloring byte count to

    `color_shift` is the amount of bytes not displayed in ANSI displays.

    """
    for m in ["C", "U", "B", "R", "G", "W", "X"]:

        r = "[0-9]" if m == "C" else m
        c = getattr(mcolor, m)

        r_mana = re.compile(r"({:s})".format(r))
        repl = r"{:s}\1{:s}".format(c, color.NC)
        (manacost, count) = re.subn(r_mana, repl, manacost)
        color_shift += (len(c) + len(color.NC)) * count

    return [manacost, color_shift]


def colorize_rarity(rarity, setcode, color_shift):
    """Return colored `setcode` and the `color_shift` as a list.

    :param int rarity:      the rarity to determine color
    :param int setcode:     setcode to colorize with rarity color
    :param int color_shift: value to add the coloring byte count to

    `color_shift` is the amount of bytes not displayed in ANSI displays.

    """
    colors = {
        "common": [rcolor.C],
        "uncommon": [rcolor.darkU, rcolor.midU, rcolor.U],
        "rare": [rcolor.darkR, rcolor.midR, rcolor.R],
        "mythic": [rcolor.darkM, rcolor.midM, rcolor.M],
    }[rarity]

    setcode_colored = ""
    if len(colors) == 1:
        setcode_colored = f"{colors[0]}{setcode}{color.NC}"
        color_shift += len(colors[0]) + len(color.NC)
    elif len(colors) == 3:
        color_len = 0
        for i, c in enumerate(colors):
            setcode_colored += "{:s}{:s}".format(c, setcode[i])
            color_shift += len(c)
        setcode_colored += color.NC
        color_shift += len(color.NC)
    return [setcode_colored, color_shift]


def colorize_text(text):  # type: list
    """Return `text` with colorized mana symbols.

    :param int text: text to colorize

    """
    colored_text = text
    for m in ["C", "U", "B", "R", "G", "W", "X"]:

        r = "[0-9]" if m == "C" else m
        c = getattr(mcolor, m)

        r_mana = re.compile(r"{(%s)}(.*?)│" % r)
        for i, l in enumerate(colored_text):
            repl = r"{:s}\1{:s}\2  │".format(c, color.NC)
            match = (l, 0)
            while True:
                match = re.subn(r_mana, repl, match[0])
                if match[1] <= 0:
                    break
            colored_text[i] = match[0]

    return colored_text


def colorize_format(text, status):
    """Return `text` colorized by format status `status`.

    :param int text:   the text to colorize
    :param int status: the legality status ('legal', 'banned', 'restr.', or '')

    `color_shift` is the amount of bytes not displayed in ANSI displays.

    """
    if status.lower() == "legal":
        text = "{}{}{}".format(lcolor.legal, text, color.NC)
        return [text, len(lcolor.legal) + len(color.NC)]
    elif status.lower() == "banned":
        text = "{}{}{}".format(lcolor.banned, text, color.NC)
        return [text, len(lcolor.banned) + len(color.NC)]
    elif status.lower() == "restr.":
        text = "{}{}{}".format(lcolor.restricted, text, color.NC)
        return [text, len(lcolor.restricted) + len(color.NC)]
    elif status.lower() == "":
        if lcolor.notlegal == color.NC:
            return (text, 0)
        text = "{}{}{}".format(lcolor.notlegal, text, color.NC)
        return [text, len(lcolor.notlegal) + len(color.NC)]
    return None


def colorize_set(setcode, set_types):
    """Return colorized `setcode` to indicate core and expansion sets.

    :param int setcode:   set code to colorize
    :param int set_types: type of set (e.g., core, expansion)

    """
    if set_types[setcode] in ("core", "expansion"):
        setcode = "{}{}{}".format(color.coreexp, setcode, color.NC)
        s_shift = len(color.coreexp) + len(color.NC)
    else:
        setcode = setcode
        s_shift = 0

    return (setcode, s_shift)


def colorize(text, c):
    """Return colorized `text` with color `c`."""
    c = getattr(color, c)
    ctext = r"{}{}{}".format(c, text, color.NC)
    p_shift = len(c) + len(color.NC)
    return ctext, p_shift


def hdr(text):
    """Return `text` colorized with color `color.header`."""
    return "{}{}{}".format(color.header, text, color.NC)
