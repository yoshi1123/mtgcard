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

"""LR parsing algorithm for mtgcard search."""


from .ply import lex
from .ply import yacc
import re

from mtgcard import settings


"""*
Grammar:


option         : option OR combination
               | combination

combination    : combination term
               | term

term           : string
               | CHARS
               | EXACT string
               | EXACT CHARS
               | CHARS eq EXACT string
               | CHARS eq EXACT CHARS
               | CHARS eq string
               | CHARS eq CHARS
               | CHARS compare CHARS
               | NOT option
               | LPAREN option RPAREN

name_term      : KW_NAME eq EXACT string
               | EXACT string
               | KW_NAME eq string
               | string
set_term       : KW_SET eq CHARS
legal_term     : KW_FORMAT eq CHARS
type_term      : KW_TYPE eq CHARS
text_term      : KW_TEXT eq string
mana_term      : KW_MANA compare CHARS

cmc_term       : KW_CMC compare CHARS
power_term     : KW_POWER compare CHARS
toughness_term : KW_TOUGHNESS compare CHARS
loyalty_term   : KW_LOYALTY compare CHARS
year_term      : KW_YEAR compare CHARS

price_term     : KW_PRICE compare CHARS

color_term     : KW_COLOR compare string


string         : DQUOTE
               | SQUOTE

eq             : EQ
               | KWEQ
compare        : GT
               | LT
               | GE
               | LE
               | NE
               | EQ
               | KWEQ


*"""

###############################################################################
#                                    Lexer                                    #
###############################################################################

# Tokens

reserved = {"or": "OR"}

tokens = [
    "NOT",
    "LPAREN",
    "RPAREN",
    "EXACT",
    "SQUOTE",
    "DQUOTE",
    "CHARS",
    "KWEQ",
    "EQ",
    "GT",
    "LT",
    "GE",
    "LE",
    "NE",
] + list(set(reserved.values()))

l_keywords = list()


def _lexer():

    t_NOT = r"-"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_EXACT = r"!"
    t_KWEQ = r":"
    t_EQ = r"="
    t_GT = r">"
    t_LT = r"<"
    t_GE = r">="
    t_LE = r"<="
    t_NE = r"!="

    def t_DQUOTE(t):
        r'"[^"]*"'
        t.value = t.value[1:-1]
        return t

    def t_SQUOTE(t):
        r"'[^']*'"
        t.value = t.value[1:-1]
        return t

    def t_CHARS(t):
        r"[a-zA-Z0-9.," "{}/]+"
        t.type = reserved.get(
            t.value.lower(), "CHARS"
        )  # check for reserved words
        return t

    # Ignored characters
    t_ignore = " \t"

    def t_error(t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)

    return lex.lex()


###############################################################################
#                                Proper Parser                                #
###############################################################################


def _parser():

    ############
    #  option  #
    ############

    def p_option_or(p):
        "option          : option OR combination"
        p[0] = "{:s} OR {:s}".format(p[1], p[3])

    def p_option_combination(p):
        "option          : combination"
        p[0] = p[1]

    #################
    #  combination  #
    #################

    def p_combination_and(p):
        "combination     : combination term"
        p[0] = "{:s} AND {:s}".format(p[1], p[2])

    def p_combination_term(p):
        "combination     : term"
        p[0] = p[1]

    ##########
    #  term  #
    ##########

    #
    # term           : CHARS
    #                | string
    #                | EXACT CHARS
    #                | EXACT string
    #                | CHARS eq EXACT string
    #                | CHARS eq EXACT CHARS
    #                | CHARS eq string
    #                | CHARS eq CHARS
    #                | CHARS compare CHARS
    #                | NOT option
    #                | LPAREN option RPAREN
    #

    def p_term_not(p):
        "term            : NOT term"
        p[0] = "NOT {:s}".format(p[2])

    def p_term_group(p):
        "term            : LPAREN option RPAREN"
        p[0] = "{:s} {:s} {:s}".format(p[1], p[2], p[3])

    ##############
    #  keywords  #
    ##############

    reserved_str = {"name": "v_name", "text": "cards.text"}
    reserved_chars = {
        "set": "cards.setCode",
        "legal": "legalities.format",
        "format": "legalities.format",
        "f": "legalities.format",
        "rarity": "cards.rarity",
        "layout": "cards.layout",
    }
    reserved_int = {
        "cmc": "cards.convertedManaCost",  # check type in Card
        "power": "cards.power",
        "toughness": "cards.toughness",
        "loyalty": "cards.loyalty",
    }
    reserved_price = {"price": "prices.price"}
    reserved_year = {"year": "sets.releaseDate"}
    reserved_type = {"type": "cards.type", "t": "cards.type"}
    reserved_color = {"colors": "cards.color", "c": "cards.color"}
    reserved_mana = {"mana": "cards.mana"}

    # name condition term

    def p_term_name(p):
        """
        term           : string
                       | CHARS
        """
        p.lexer.l_keywords.append("%{:s}%".format(p[1]))
        p.lexer.l_keywords.append("%{:s}%".format(p[1]))
        sql_query = "lower({:s}) LIKE lower(?)".format("v_name")
        other_query = "lower({:s}) LIKE lower(?)".format("cards.faceName")
        p[0] = sql_where_card_or_otherids(
            card_cond=sql_query, other_cond=other_query
        )

    def p_term_exact_name(p):
        """
        term           : EXACT string
                       | EXACT CHARS
        """
        p.lexer.l_keywords.append(p[2])
        p.lexer.l_keywords.append(p[2])
        sql_query = "lower({:s}) = lower(?)".format("v_name")
        other_query = "lower({:s}) = lower(?)".format("cards.faceName")
        p[0] = sql_where_card_or_otherids(
            card_cond=sql_query, other_cond=other_query
        )

    def p_term_eq_exact_name(p):
        """
        term           : CHARS eq EXACT string
                       | CHARS eq EXACT CHARS
        """

        if p[1] != "name":
            raise ValueError("invalid search keyword '{}'".format(p[1]))
        p.lexer.l_keywords.append(p[4])
        p.lexer.l_keywords.append(p[4])
        sql_query = "lower({:s}) = lower(?)".format("v_name")
        other_query = "lower({:s}) = lower(?)".format("cards.faceName")
        p[0] = sql_where_card_or_otherids(
            card_cond=sql_query, other_cond=other_query
        )

    # name and non-name condition terms

    def p_term_eq(p):
        """
        term           : CHARS eq string
                       | CHARS eq CHARS
        """
        if p[1] in reserved_str:
            str_term(p)

        elif p[1] in reserved_chars:
            chars_term(p)

        elif p[1] in reserved_int:
            int_term(p)

        elif p[1] in reserved_price:
            price_term(p)

        elif p[1] in reserved_year:
            year_term(p)

        elif p[1] in reserved_type:
            type_term(p)

        elif p[1] in reserved_color:
            color_term(p)

        elif p[1] in reserved_mana:
            mana_term(p)

        else:
            raise ValueError("invalid search keyword '{}'".format(p[1]))

    def p_term_compare(p):
        """
        term           : CHARS compare CHARS
        """
        if p[1] in reserved_int:
            int_term(p)

        elif p[1] in reserved_price:
            price_term(p)

        elif p[1] in reserved_year:
            year_term(p)

        elif p[1] in reserved_color:
            color_term(p)

        elif p[1] in reserved_mana:
            mana_term(p)

        else:
            raise ValueError("invalid search keyword '{}'".format(p[1]))

    ####################
    #  term functions  #
    ####################

    def str_term(p):
        p.lexer.l_keywords.append("%{:s}%".format(p[3]))
        p.lexer.l_keywords.append("%{:s}%".format(p[3]))
        sql_query = "lower({:s}) LIKE lower(?)".format(reserved_str[p[1]])
        other_str = reserved_str[p[1]].replace("v_name", "cards.faceName")
        other_query = "lower({:s}) LIKE lower(?)".format(other_str)
        p[0] = sql_where_card_or_otherids(
            card_cond=sql_query, other_cond=other_query
        )

    def chars_term(p):
        p.lexer.l_keywords.append(p[3])
        sql_query = "lower({:s}) = lower(?)".format(reserved_chars[p[1]])
        p[0] = sql_where_card_or_otherids(card_cond=sql_query, other_cond=None)

    def int_term(p):
        p.lexer.l_keywords.append(int(p[3]))
        if p[2] == ":":
            p[2] = "="

        if p[1] in ("power", "toughness"):
            p.lexer.l_keywords.append(int(p[3]))
            layouts = ("'aftermath'", "'flip'", "'transform'", "'meld'")
            sql_query = "{:s} {:s} ?".format(reserved_int[p[1]], p[2])
            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query,
                other_cond=sql_query,
                other_layouts=layouts,
            )
        else:
            sql_query = "{:s} {:s} ?".format(reserved_int[p[1]], p[2])
            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query, other_cond=None
            )

    def price_term(p):
        match = re.match(r"\d+(?:\.\d+)?", p[3])
        if not match:
            raise SyntaxError
        for i in range(1):
            p.lexer.l_keywords.append(
                float(float(match.group()) / settings.US_TO_CUR_RATE)
            )
        if p[2] == ":":
            p[2] = "="
        sql_query = """
        ( {:s} {:s} round(?,2) AND prices.type = 'paper' )
        """.format(
            "prices.price", p[2]
        )
        p[0] = sql_where_card_or_otherids(card_cond=sql_query, other_cond=None)

    def year_term(p):
        p.lexer.l_keywords.append(int(p[3]))
        p.lexer.l_keywords.append(int(p[3]))
        if p[2] == ":":
            p[2] = "="
        sql_query = """
        CAST(strftime('%Y', DATE({:s})) AS INTEGER) {:s} ?
        """.strip().format(
            "sets.releaseDate", p[2]
        )
        p[0] = sql_where_card_or_otherids(card_cond=sql_query, other_cond=None)

    def type_term(p):
        for i in range(6):
            p.lexer.l_keywords.append(p[3])
        sql_query = """
        (csv_in(lower(cards.subtypes), lower(?)) OR
        csv_in(lower(cards.supertypes), lower(?)) OR
        csv_in(lower(cards.types), lower(?)))
        """
        p[0] = sql_where_card_or_otherids(
            card_cond=sql_query, other_cond=sql_query
        )

    def color_term(p):
        layouts = ("'transform'", "'meld'")
        for i in range(4):
            p.lexer.l_keywords.append(",".join(p[3]))
        if p[2] == ":":
            p[2] = ">="

        if p[2] == "=":
            for i in range(2):
                p.lexer.l_keywords.append(",".join(p[3]))

            sql_query_split = """
        ( csv_len({tbl_col}) {:s} csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower({tbl_col})) AND
        csv_set_contains(lower({tbl_col}), lower(?)) )
        """.format(
                p[2], tbl_col="colors_sp"
            )
            sql_query = """
        ( csv_len({tbl_col}) {:s} csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower({tbl_col})) AND
        csv_set_contains(lower({tbl_col}), lower(?)) )
        """.format(
                p[2], tbl_col="cards.colors"
            )

            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query_split,
                other_cond=sql_query,
                other_layouts=layouts,
            )

        elif p[2] == ">" or p[2] == ">=":
            sql_query_split = """
        ( csv_len({tbl_col}) {:s} csv_len(lower(?)) AND
        csv_set_contains(lower({tbl_col}), lower(?)) )
        """.format(
                p[2], tbl_col="colors_sp"
            )
            sql_query = """
        ( csv_len({tbl_col}) {:s} csv_len(lower(?)) AND
        csv_set_contains(lower({tbl_col}), lower(?)) )
        """.format(
                p[2], tbl_col="cards.colors"
            )
            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query_split,
                other_cond=sql_query,
                other_layouts=layouts,
            )

        elif p[2] == "<" or p[2] == "<=":
            sql_query_split = """
        ( csv_len({tbl_col}) {:s} csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower({tbl_col})) )
        """.format(
                p[2], tbl_col="colors_sp"
            )
            sql_query = """
        ( csv_len({tbl_col}) {:s} csv_len(lower(?)) AND
        csv_set_contains(lower(?), lower({tbl_col})) )
        """.format(
                p[2], tbl_col="cards.colors"
            )
            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query_split,
                other_cond=sql_query,
                other_layouts=layouts,
            )

    def mana_term(p):
        # do not combine manacosts for split card searches
        layouts = ("'adventure'", "'split'", "'aftermath'")
        for i in range(4):
            p.lexer.l_keywords.append(p[3])
        if p[2] == ":":
            p[2] = ">="

        if p[2] == ">" or p[2] == ">=":
            sql_query = """
        ( manacost_to_cmc({tbl_col}) {:s} manacost_to_cmc(lower(?)) AND
        manacost_contains(lower({tbl_col}), lower(?)) )
        """.format(
                p[2], tbl_col="cards.manaCost"
            )
            #     sql_query_split = '''
            # ( {:s} {:s} manacost_to_cmc(lower(?)) AND
            # manacost_contains(lower({:s}), lower(?)) )
            # '''.format('cards.convertedManaCost', p[2], 'manacost_sp')
            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query,
                other_cond=sql_query,
                other_layouts=layouts,
            )

        elif p[2] == "<" or p[2] == "<=":
            sql_query = """
        ( manacost_to_cmc({tbl_col}) {:s} manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(?), lower({tbl_col})) )
        """.format(
                p[2], tbl_col="cards.manaCost"
            )
            #     sql_query_split = '''
            # ( {:s} {:s} manacost_to_cmc(lower(?)) AND
            # manacost_contains(lower(?), lower({:s})) )
            # '''.format('cards.convertedManaCost', p[2], 'manacost_sp')
            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query,
                other_cond=sql_query,
                other_layouts=layouts,
            )

        elif p[2] == "=":
            for i in range(2):
                p.lexer.l_keywords.append(p[3])
            sql_query = """
        ( manacost_to_cmc({tbl_col}) {:s} manacost_to_cmc(lower(?)) AND
        manacost_contains(lower(?), lower({tbl_col})) AND
        manacost_contains(lower({tbl_col}), lower(?)) )
        """.format(
                p[2], tbl_col="cards.manaCost"
            )
            #     sql_query_split = '''
            # ( {:s} {:s} manacost_to_cmc(lower(?)) AND
            # manacost_contains(lower(?), lower({tbl_col})) AND
            # manacost_contains(lower({tbl_col}), lower(?)) )
            # '''.format(
            #   'cards.convertedManaCost', p[2], tbl_col='manacost_sp'
            # )
            p[0] = sql_where_card_or_otherids(
                card_cond=sql_query,
                other_cond=sql_query,
                other_layouts=layouts,
            )

    ############
    #  string  #
    ############

    def p_string_dquote_empty(p):
        """
        string          : DQUOTE
        string          : SQUOTE
        """
        p[0] = p[1]

    #############
    #  compare  #
    #############

    def p_eq(p):
        """
        eq               : EQ
                         | NE
                         | KWEQ
        """
        p[0] = p[1]

    def p_compare(p):
        """
        compare          : GT
                         | LT
                         | GE
                         | LE
        """
        p[0] = p[1]

    ###########
    #  error  #
    ###########

    def p_error(p):
        # raise Exception("parse error")
        if not p:
            # print("parse error: reached EOF while expecting data")
            raise SyntaxError("parse error: reached EOF while expecting data")
        else:
            # print(f"syntax error at {p.value!r}")
            raise SyntaxError(f"syntax error at {p.value!r}")

    return yacc.yacc(debug=debug)


###################
#  sql functions  #
###################


def sql_where_card_or_otherids(card_cond, other_cond=None, other_layouts=None):
    """Return SQL for WHERE code for the card and its other faces.

    :param str   card_cond:     WHERE condition for card
    :param list  other_cond:    WHERE condition for other faces (do not check
                                other faces if None)
    :param tuple other_layouts: limit layouts to which other faces are checked
                                (None means all layouts are checked)

    """
    if other_layouts is not None:
        s_other_layouts = ",".join(other_layouts)
    else:
        s_other_layouts = None

    sql = """

    (
        (
            """+card_cond+"""
        )


        """+("""
        OR
        (
            otherFaceIds NOT NULL AND

            """+("""
            layout in ("""+s_other_layouts+""") AND
            """ if other_layouts else """
            layout in
                ('adventure','aftermath','flip','split','transform','meld') AND
            """)+"""

            ( WITH split(word, str) AS (
                SELECT '', otherFaceIds||','
                UNION ALL
                SELECT
                substr(str, 1, instr(str, ',')-1),
                substr(str, instr(str, ',')+1)
                FROM split WHERE str != ''
                ) SELECT count(*) FROM split WHERE word != '' AND
                (
                    SELECT count(*) FROM cards
                    WHERE uuid = word AND
                        (
                            (layout != 'meld' AND side != 'a')
                            OR
                            (layout = 'meld' AND side != 'a' AND side != 'b')
                            OR
                            (side IS NULL AND layout = 'split'
                                AND cards.faceName != facename_element(cards.name,0))
                        ) AND (
                            """+other_cond+"""
                        )
                    ) >= 1
                ) >= 1

        )
        """ if other_cond else '')+"""


    )

    """

    return sql


###############################################################################
#                                   Parser                                    #
###############################################################################

v_debug = False
debug = False
# debug = True


class Parser(object):
    """Wrapper for lex and yacc parser."""

    def __init__(self):
        self.lexer = _lexer()
        self.lexer.l_keywords = []
        self.parser = _parser()

    def parse(self, string):
        if debug:
            self.tokens(string)

        try:
            ret = (
                self.parser.parse(string, debug=v_debug),
                tuple(self.lexer.l_keywords),
            )
        except TypeError as e:
            pass
            # # temporary:
            # raise SyntaxError("parser found `None` as a terminal")
        except ValueError as e:
            raise SyntaxError(e)
        finally:
            self.lexer.l_keywords = []
        return ret

    def tokens(self, string):
        print("tokens for '{:s}':".format(string))
        self.lexer.input(string)
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # No more input
            print("  {!s:s}".format(tok))
        print()


parser = Parser()

__all__ = parser
