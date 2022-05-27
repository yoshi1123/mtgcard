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

"""Database interface."""


import sys
from os import path
import re
import json
import sqlite3

from mtgcard.card import Card
from mtgcard import util
from mtgcard import settings

# debug
from pprint import pprint


# regex
r_facenamesep = re.compile(r" // ")
r_namesep = re.compile(r",(?=[^ ])")
r_unbraced_char = re.compile(r"(?<!{)(\d+|[WUBRGSCXwubrgscx])(?!})")


# SQLite functions


def csv_in(l, v):
    """Return if value `v` is in `l`.

    :param str v: value
    :param str l: comma separated value string

    Example:

        >>> csv_in('w', "w,u,g")
        # True

    """
    if l is None:
        return False
    return v in r_namesep.split(l)


def csv_element(l, i):
    """Return element `i` in `l`.

    :param int i: index
    :param str l: comma separted value string

    Example:

        >>> csv_element(0, "w,u,g")
        # 'w'

    """
    e = r_namesep.split(l)
    if e and i <= len(e) - 1:
        return e[i]
    else:
        return None


def csv_len(l):
    """Return number of items in `l`.

    :param str l: comma separated value string

    Example:

        >>> csv_len("w,u,g")
        # 3

    """
    if l is None or len(l) == 0:
        return 0
    return len(set(l.split(",")))


def csv_set_contains(a, b):
    """Return if set a contains set b.

    :param str a: comma separated value string
    :param str b: comma separated value string

    Example:

        >>> csv_set_contains("w,u,g", "w,u")
        # True

    """
    if not a and not b:
        return True
    if a and not b:
        return True
    if not a and b:
        return False
    if len(a) == 0:
        seta = set()
    else:
        seta = set(a.split(","))
    if len(b) == 0:
        setb = set()
    else:
        setb = set(b.split(","))
    return seta.issuperset(setb)


def facename_element(l, i):
    """Return element `i` in `l`.

    :param int i: index
    :param str l: ' // ' separated name string

    Example:

        >>> facename_element(0, 'Rimrock Knight // Boulder Rush')
        # 'Rimrock Knight'

    """
    e = r_facenamesep.split(l)
    if e and i <= len(e) - 1:
        return e[i]
    else:
        return None


def manacost_contains(a, b):
    """Return if color list a contains color list b.

    :param str a: manacost
    :param str b: manacost

    Example:

        manacost_contains("3wg", "1wg")
        # True

        manacost_contains("{3}{w}g", "1wg")
        # True

    """
    if not a and not b:
        return True
    if a and not b:
        return True
    if not a and b:
        return False
    a = r_unbraced_char.subn(r"{\1}", a)[0]
    b = r_unbraced_char.subn(r"{\1}", b)[0]

    # flatten generic mana in a
    match = re.findall(r"{(\d+)}", a)
    a = re.subn(r"{\d+}", "", a)[0]
    for g in match:
        for n in range(1, int(g) + 1):
            a += "{1}"

    # flatten generic mana in b
    match = re.findall(r"{(\d+)}", b)
    b = re.subn(r"{\d+}", "", b)[0]
    for g in match:
        for n in range(1, int(g) + 1):
            b += "{1}"

    # sort the mana string
    if len(a) == 0:
        lista = ""
    else:
        lista = "".join(sorted(a.replace("}{", "},{").split(",")))
    if len(b) == 0:
        listb = ""
    else:
        listb = "".join(sorted(b.replace("}{", "},{").split(",")))

    return listb in lista


def manacost_to_cmc(mc):
    """Return converted manacost of manacost `mc`.

    :param str mc: manacost

    Example:

        manacost_to_cmc("3wg")
        # 5

        manacost_to_cmc("{1}{w}g")
        # 3

    """
    if mc is None:
        return 0

    # surround unbraced colors with braces
    mc = r_unbraced_char.subn(r"{\1}", mc)[0]

    # remove x
    mc = re.subn("{[Xx]}", "", mc)[0]

    # count and remove {#}
    count = 0
    match = re.findall(r"{(\d+)(?:/[WUBRGSCXwubrgscx])?}", mc)
    for i in match:
        count += int(i)
    mc = re.subn(r"{\d+(?:/[WUBRGSCXwubrgscx])?}", "", mc)[0]

    # make list of mana
    if len(mc) == 0:
        listmc = ""
    else:
        listmc = sorted(mc.replace("}{", "},{").split(","))

    return len(listmc) + count


def collate_exp_core_first(settype1, settype2):
    """Return a number indicating if `settype1` is greater than `settype2`.

    :param str settype1: set type
    :param str settype2: set type

    Alphabetical comparison except set types "expansion" and "core" are
    greatest. Return codes are as follows:

        1   `settype1` is greater than `settype2`
        0   `settype1` is equal to `settype2`
        -1  `settype1` is lesser than `settype2`

    """
    if settype1 in ("expansion", "core") and settype2 not in (
        "expansion",
        "core",
    ):
        return 1
    elif settype1 not in ("expansion", "core") and settype2 in (
        "expansion",
        "core",
    ):
        return -1
    elif settype1 in ("expansion", "core") and settype2 in (
        "expansion",
        "core",
    ):
        return 0

    if settype1 == settype2:
        return 0
    elif settype1 > settype2:
        return 1
    else:
        return -1


class MTGDatabase(object):
    """MTG database interface."""

    def __init__(self):
        """Initialize."""
        pass

    def get_cards(self, query):
        """Return a list of Cards based on `query`."""
        pass

    def get_card(self, name, setcode, case_sensitive=False):
        """Return a card by name."""
        pass


class Interface(MTGDatabase):
    """MTG sqlite database interface."""

    def __init__(self):
        """Initialize database cursor and set up sqlite."""
        self.cursor = None

        # get cursor
        root_dir = path.dirname(__file__)
        filepath = path.join(root_dir, "data/mtg.sqlite")
        if not path.exists(filepath):
            raise FileNotFoundError(
                "'mtgcard [-v] --update-db' to generate database"
            )
        conn = sqlite3.connect(filepath)
        conn.row_factory = sqlite3.Row
        self.cursor = conn.cursor()

        # settings
        self.cursor.execute("PRAGMA case_sensitive_like=ON")

        # functions
        conn.create_function("csv_in", 2, csv_in)
        conn.create_function("csv_element", 2, csv_element)
        conn.create_function("csv_len", 1, csv_len)
        conn.create_function("csv_set_contains", 2, csv_set_contains)
        conn.create_function("facename_element", 2, facename_element)
        conn.create_function("manacost_to_cmc", 1, manacost_to_cmc)
        conn.create_function("manacost_contains", 2, manacost_contains)
        conn.create_collation("main_sets_first", collate_exp_core_first)

    # mtgdb functions

    def get_rulings(self, uuid):
        """Return list of rulings for `uuid`.

        Rulinglist format: [ {'date': 'YYYY-MM-DD', 'text': STR}, ... ]

        """
        self.cursor.execute(
            """
            SELECT DISTINCT rulings.date, rulings.text
            FROM cards
                LEFT JOIN rulings ON cards.uuid = rulings.uuid
            WHERE cards.uuid = ?
            ORDER BY rulings.id
            """,
            (uuid,),
        )
        result = self.cursor.fetchall()
        if len(result) == 0 or result[0][1] is None:
            return []
        rulings = []
        for ruling in result:
            rulings.append({"date": ruling[0], "text": ruling[1]})
        return rulings

    def get_formats(self, uuid):
        """Return list of formats for `uuid`.

        Formats list format: [ {'format': STR, 'status': STR}, ... ]

        """
        self.cursor.execute(
            """
            SELECT DISTINCT format, status
            FROM cards
                LEFT JOIN legalities ON cards.uuid = legalities.uuid
            WHERE cards.uuid = ?
            ORDER BY format
            """,
            (uuid,),
        )
        result = self.cursor.fetchall()
        if len(result) == 0 or result[0][1] is None:
            return {}
        formats = {f["format"]: f["status"] for f in result}
        return formats

    def get_sets(self):
        """Return a dict of all sets and their type in the database.

        Sets format: {SETCODE: TYPE}
        """
        self.cursor.execute(
            """
            SELECT DISTINCT code, type
            FROM sets
            ORDER BY
                sets.type collate main_sets_first DESC,
                sets.releaseDate DESC
            """
        )
        result = self.cursor.fetchall()
        if len(result) == 0:
            return []
        sets = {}
        for s in result:
            sets[s[0]] = s[1]
        return sets

    def get_price(self, name, setcode=None, token=False):
        """Return prices, or price if `setcode` is specified, for `name`.

        Price format: FLOAT

        Prices format: [[SETCODE, FLOAT], ...]

        """
        if setcode is not None:
            self.cursor.execute(
                """
                SELECT DISTINCT
                prices.price, --, prices.date
                CASE WHEN cards.faceName IS NULL
                THEN cards.name
                ELSE cards.faceName
                END AS v_name
                FROM cards
                    LEFT JOIN prices ON cards.uuid = prices.uuid
                        AND prices.type = 'paper'
                WHERE lower(v_name) = lower(?) AND lower(setCode) = lower(?)
                ORDER BY prices.price
                LIMIT 1
                """,
                (name, setcode),
            )
            # result = self.cursor.fetchall()
            result = self.cursor.fetchone()
            price = None
            if len(result) > 0 and result[0] is not None:
                price = result[0]
            return price
        else:
            if token:

                self.cursor.execute(
                    """
                    SELECT DISTINCT setCode, min(prices.price), --, prices.date
                    CASE WHEN tokens.faceName IS NULL
                    THEN tokens.name
                    ELSE tokens.faceName
                    END AS v_name
                    FROM tokens
                        LEFT JOIN sets ON tokens.setCode = sets.code
                        LEFT JOIN prices ON tokens.uuid = prices.uuid
                            AND prices.type = 'paper'
                    WHERE lower(v_name) = lower(?)
                    GROUP BY setCode
                    ORDER BY
                        sets.type collate main_sets_first DESC,
                        sets.releaseDate DESC,
                        prices.price
                    """,
                    (name,),
                )

            else:

                self.cursor.execute(
                    """
                    SELECT DISTINCT setCode, min(prices.price), --, prices.date
                    CASE WHEN cards.faceName IS NULL
                    THEN cards.name
                    ELSE cards.faceName
                    END AS v_name
                    FROM cards
                        LEFT JOIN sets ON cards.setCode = sets.code
                        LEFT JOIN prices ON cards.uuid = prices.uuid
                            AND prices.type = 'paper'
                    WHERE lower(v_name) = lower(?)
                    GROUP BY setCode
                    ORDER BY
                        sets.type collate main_sets_first DESC,
                        sets.releaseDate DESC,
                        prices.price
                    """,
                    (name,),
                )

            result = self.cursor.fetchall()
            if len(result) == 0:
                return []
            prices = []
            for price in result:
                prices.append(list(price))
            return prices

    def get_other_faces(self, card):
        """Return list of all faces that are not `card.name`.

        :para Card card: a card

        """
        if card.names:
            otherFaces = []
            for n in card.names:
                if n != card.name:
                    otherFaces.append(
                        self.get_card(n, card.setcode, single_side=True)
                    )
            return otherFaces
        else:
            return None

    def get_token(self, name, setcode=None, verbose=False):
        """Return a token Card called `name`.

        :param str  name:    name of card to get
        :param str  setcode: setcode of card to get
        :param bool verbose: whether to get price

        """
        t = [name]
        if setcode:
            t.append(setcode)
        t = tuple(t)

        sql = '''
            SELECT
                CASE WHEN tokens.faceName IS NULL
                THEN tokens.name
                ELSE tokens.faceName
                END AS v_name,
                tokens.name, tokens.uuid, setCode, power, toughness, types,
                tokens.type, text, layout,
                replace(tokens.name, " // ", ",") as v_names, side,
                colors as colors_sp

                '''+(''',
                prices.price,prices.date
                ''' if verbose else '')+'''

            FROM tokens

                '''+('''
                JOIN sets ON tokens.setCode = sets.code
                ''' if not setcode else '')+'''

                '''+('''
                LEFT JOIN prices ON tokens.uuid = prices.uuid
                    AND prices.type = 'paper'
                ''' if verbose else '')+'''

            WHERE

                lower(v_name) = lower(?)

                '''+('''
                AND lower(setCode) = lower(?)
                ''' if setcode else '')+'''

            '''+('''
            ORDER BY sets.type collate main_sets_first DESC,
                     sets.releaseDate DESC
            ''' if not setcode else '')+'''
            LIMIT 1
            '''

        self.cursor.execute(sql, t)

        result = self.cursor.fetchone()

        if result:

            card = self.card_from_result(
                result, single_side=True, verbose=verbose, rulings=False
            )
            return card

        else:

            location = ""
            if setcode:
                location += " in '{:s}'".format(setcode)
            raise ValueError(
                "token card not found{:s}: '{:s}'".format(location, name)
            )

        return card

    def card_from_result(
        self, result, single_side=False, verbose=False, rulings=False
    ):
        """Return a Card created from a database fetch dict `result`.

        :param sqlite3.Row result:      query card results
        :param bool        single_side: whether to not fetch other sides
        :param bool        verbose:     whether to assign formats to Card
        :param bool        rulings:     whether to assign rulings to Card

        """
        card = Card()

        card.names = (
            r_facenamesep.split(result["name"]) if result["name"] else None
        )

        # for flip, adventure, etc., get side a instead of side b
        # always fetch otherfaces unless 'single_side' is True
        if result["layout"] in ("flip", "adventure", "split", "aftermath"):
            if result["side"] == "b" and not single_side:
                return self.get_card(card.names[0], result["setcode"])

        card.name = result["v_name"]
        card.uuid = result["uuid"]
        card.setcode = result["setCode"]
        card.power = result["power"]
        card.toughness = result["toughness"]
        card.types = result["types"].split(",")
        card.type = result["type"]
        card.text = result["text"]
        card.layout = result["layout"]
        card.colors = (
            result["colors_sp"].split(",") if result["colors_sp"] else None
        )
        if verbose:
            card.formats = self.get_formats(card.uuid)

        if card.types[0] != "Token":

            card.printings = result["printings"]
            card.cmc = result["convertedManaCost"]
            card.manacost = (
                result["manaCost"].replace("{", "").replace("}", "")
                if result["manaCost"]
                else None
            )
            card.loyalty = result["loyalty"]
            card.rarity = result["rarity"]
            card.side = result["side"]

            if not single_side and card.names is not None:
                card.otherfaces = (
                    self.get_other_faces(card) if result["v_names"] else None
                )

            if rulings:
                card.rulings = self.get_rulings(card.uuid)

        try:
            card.price = result["price"] if result["price"] else None
            card.price_date = result["date"] if result["date"] else None
        except IndexError as e:
            pass

        return card

    def get_cards(self, query, sort="name", reverse=False, limit=None):
        """Return a list of cards from database.

        :param str  query:   search query
        :param str  sort:    sort key (cmc, name, price, or setcode)
        :param bool reverse: whether to reverse result order
        :param bool limit:   maximum number of cards to return

        """
        sortkey = {
            "cmc": "convertedManaCost",
            "name": "v_name",
            "price": "price",
            "setcode": "setCode",
        }

        sql = '''
        WITH main_first AS (


            SELECT
                CASE WHEN cards.faceName IS NULL
                THEN cards.name
                ELSE cards.faceName
                END AS v_name,
                cards.name,cards.uuid,printings,setCode,convertedManaCost,
                manaCost,power,toughness,loyalty,types,cards.type,rarity,
                cards.text,layout,
                replace(cards.name, " // ", ",") as v_names,side,
                max(setcode) OVER
                (ORDER BY sets.type collate main_sets_first DESC,
                          releaseDate DESC
                ) latest_main,
                CASE WHEN (layout) IN ('split','aftermath') THEN

                        (WITH split(word, str) AS (
                                SELECT '', otherFaceIds||','
                                UNION ALL
                                SELECT
                                substr(str, 1, instr(str, ',')-1),
                                substr(str, instr(str, ',')+1)
                                FROM split WHERE str != ''
                            ) SELECT
                                group_concat(
                                    (SELECT colors FROM cards c1
                                     WHERE c1.uuid = word)
                                )
                            FROM split WHERE word != ''
                        )||','||colors

                ELSE colors
                END AS colors_sp,
                prices.price,prices.date

            FROM cards
                JOIN sets ON cards.setCode = sets.code
                LEFT JOIN legalities ON cards.uuid = legalities.uuid
                LEFT JOIN prices ON cards.uuid = prices.uuid
                    AND prices.type = 'paper'

            WHERE

                csv_in(availability, 'paper')

                AND (
                    -- exclude set 'Mystery Booster Playtest Cards (CMB1)'
                    -- exclude set 'Happy Holidays (HHO)'
                    -- exclude set 'Ponies: The Galloping (PTG)'
                    -- exclude set '2016 Heroes of the Realm (HTR)'
                    -- exclude set '2017 Heroes of the Realm (HTR17)'
                    -- exclude set '2018 Heroes of the Realm (HTR18)'
                    -- exclude set 'HasCon (H17)'
                    setCode not in ('CMB1', 'HHO', 'PTG', 'HTR', 'HTR17',
                                    'HTR18', 'H17')
                )

                AND (
                    (side IS NULL AND layout != 'split') OR
                    side = 'a' OR (layout = 'meld' AND side = 'b') OR
                    (side IS NULL AND layout = 'split'
                        AND v_name = facename_element(cards.name,0))
                )

                '''+(' AND ('+query[0]+')' if len(query[0]) > 0 else '')+'''


        ) SELECT * FROM main_first
        GROUP BY v_name
        '''+('ORDER BY {} {}'.format(sortkey[sort],
                                     ("DESC" if reverse else "ASC")))+'''
        '''+(f'LIMIT {limit}' if limit else '')+'''

        '''

        # pprint( query )
        # print( sql )

        sqlite3.enable_callback_tracebacks(True)
        self.cursor.execute(sql, query[1])

        results = self.cursor.fetchall()
        cards = {}
        for result in results:

            # get card
            cards[result["v_name"]] = self.card_from_result(
                result, verbose=False, rulings=False
            )

        if len(cards) == 0:
            pass
        else:
            cards = list(cards.values())
            return cards

    def get_card(
        self,
        name,
        setcode=None,
        format=None,
        single_side=False,
        verbose=False,
        rulings=False,
    ):
        """Return a Card, `name` from database.

        :param str  name:        name of card to get
        :param str  setcode:     setcode of card to get
        :param str  format:      format of card to get
        :param bool single_side: whether to fetch only a single side
        :param bool verbose:     whether to get price
        :param bool rulings:     whether to get rulings

        """
        if name.lower().endswith(" token"):
            name = name[0:-6]
            return self.get_token(name, setcode=setcode, verbose=verbose)

        else:

            t = [name]
            if setcode:
                t.append(setcode)
            if format:
                t.append(format)
            t = tuple(t)

            self.cursor.execute("""
                SELECT
                    CASE WHEN cards.faceName IS NULL
                    THEN cards.name
                    ELSE cards.faceName
                    END AS v_name,
                    cards.name,cards.uuid,printings,setCode,convertedManaCost,
                    manaCost,power,toughness,loyalty,types,cards.type,rarity,
                    cards.text,layout,
                    replace(cards.name, " // ", ",") as v_names,side,
                    CASE WHEN (layout) IN ('split','aftermath') THEN

                            (WITH split(word, str) AS (
                                    SELECT '', otherFaceIds||','
                                    UNION ALL
                                    SELECT
                                    substr(str, 1, instr(str, ',')-1),
                                    substr(str, instr(str, ',')+1)
                                    FROM split WHERE str != ''
                                ) SELECT
                                    group_concat(
                                        (SELECT colors FROM cards c1
                                         WHERE c1.uuid = word)
                                    )
                                FROM split WHERE word != ''
                            )||','||colors

                    ELSE colors
                    END AS colors_sp

                    """+(""",
                    prices.price,prices.date
                    """ if verbose else '')+"""

                FROM cards

                    """+("""
                    JOIN sets ON cards.setCode = sets.code
                    """ if not setcode else '')+"""

                    """+("""
                    LEFT JOIN legalities ON cards.uuid = legalities.uuid
                    """ if format else '')+"""

                    """+("""
                    LEFT JOIN prices ON cards.uuid = prices.uuid
                        AND prices.type = 'paper'
                    """ if verbose else '')+"""

                WHERE

                    lower(v_name) = lower(?)

                    AND csv_in(availability, 'paper')

                    """+("""
                    AND lower(setCode) = lower(?)
                    """ if setcode else '')+"""

                    """+("""
                    AND lower(legalities.format) = lower(?) AND
                    legalities.status = 'Legal'
                    """ if format else '')+"""

                """+("""
                ORDER BY sets.type collate main_sets_first DESC,
                         sets.releaseDate DESC
                """ if not setcode else '')+"""
                LIMIT 1
                """, t)

            result = self.cursor.fetchone()

            if result:

                card = self.card_from_result(
                    result,
                    single_side=single_side,
                    verbose=verbose,
                    rulings=rulings,
                )
                return card

            else:

                location = ""
                if setcode:
                    location += " in '{:s}'".format(setcode)
                if format:
                    location += " in '{:s}'".format(format)
                raise ValueError(
                    "card not found{:s}: '{:s}'".format(location, name)
                )
