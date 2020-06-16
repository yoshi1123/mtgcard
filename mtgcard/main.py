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

"""mtgcard entry point."""


# for debugging
from pprint import pprint

import sys
import argparse
import signal

from mtgcard import mtgdb
from mtgcard import settings
from mtgcard.mtgcard import get_and_print_card
from mtgcard.mtgcard import list_cards


def get_args():
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        prog="mtgcard",
        description="""
        Either (1) print a MTG card by name or (2) list cards by query.
        """.strip(),
    )

    parser.add_argument(
        "-l",
        dest="full_list",
        action="store_true",
        help="list card summaries by 'query'",
    )
    parser.add_argument(
        "-i", dest="nr_columns", type=int, help="list card images by 'query'"
    )
    parser.add_argument(
        "-n",
        dest="name_list",
        action="store_true",
        help="list card names by 'query'",
    )
    parser.add_argument(
        "-N",
        dest="name_list_multi",
        action="store_true",
        help="list card names, of all sides, by 'query'",
    )
    parser.add_argument(
        "-g",
        dest="ansi",
        action="store_const",
        const=False,
        default=settings.ANSI_COLOR,
        help="disable color",
    )
    parser.add_argument(
        "-G",
        dest="ansi",
        action="store_const",
        const=True,
        help="enable color (default)",
    )
    parser.add_argument(
        "-q",
        dest="header",
        action="store_false",
        help="disable header row in listing",
    )
    parser.add_argument(
        "-c",
        dest="compact",
        action="store_true",
        help="disable image in card prints",
    )
    parser.add_argument(
        "--sort",
        dest="sort",
        type=str,
        default="name",
        choices=("name", "cmc", "price"),
        help="sort listings (default: %(default)s)",
    )
    parser.add_argument(
        "-r", dest="reverse", action="store_true", help="reverse sort order"
    )
    parser.add_argument(
        "-L", dest="limit", type=int, help="set a listing limit"
    )
    parser.add_argument(
        "-R", dest="rulings", action="store_true", help="show rulings"
    )
    parser.add_argument(
        "-v",
        dest="verbose",
        action="store_true",
        help="card: extra info; listing: show matches count",
    )

    parser.add_argument(
        "--set",
        "-s",
        dest="setcode",
        type=str,
        help="set code of card (default: %(default)s)",
    )
    parser.add_argument(
        "--format",
        "-f",
        dest="format",
        type=str,
        default=settings.DEFAULT_FORMAT,
        help="format of card (default: %(default)s)",
    )

    parser.add_argument("query", type=str, nargs="*", help="card search terms")

    parser.add_argument(
        "--update-db",
        dest="update_db",
        action="store_true",
        help="update the local MTG database",
    )

    return parser.parse_args()


def interrupt_handler(a, b):
    """Exit quietly on CTRL-C."""
    print()
    sys.exit(130)


def main():
    """Entry point."""
    # exit quietly on KeyboardInterrupt
    signal.signal(signal.SIGINT, interrupt_handler)

    args = get_args()

    full_list = args.full_list
    image_list = args.nr_columns  # number of columns
    name_list = args.name_list
    name_list_multi = args.name_list_multi
    header = args.header
    sort = args.sort
    reverse = args.reverse
    limit = args.limit
    rulings = args.rulings

    query = " ".join(args.query)
    ansi = args.ansi
    verbose = args.verbose
    compact = args.compact

    setcode = args.setcode
    format = args.format

    update_db = args.update_db

    # setup database
    try:
        db = mtgdb.Interface()
    except FileNotFoundError as e:
        if update_db:
            import mtgcard.update

            print("updating database... (this could take a while [~45MB])")
            mtgcard.update.update_database(verbose=verbose)
            print("update complete")
            sys.exit(0)
        else:
            print(e)
            sys.exit(1)
    if update_db:
        import mtgcard.update

        print("updating database")
        mtgcard.update.update_database(verbose=verbose)
        sys.exit(0)

    def option_warn(arg, type):
        """Print warning message for incompatabile command line arguments."""
        message = """
            error: command line argument '{:s}' is not compatible with {:s}
            """.strip().format(
            arg, type
        )
        print(message, file=sys.stderr)
        sys.exit(1)

    # retrieve cards
    if full_list or name_list or name_list_multi or image_list:

        if full_list:
            if name_list:
                option_warn("-n", "line listings (-l)")
            if image_list:
                option_warn("-i", "line listings (-l)")
        elif name_list or name_list_multi:
            if full_list:
                option_warn("-l", "name listings (-n)")
            if image_list:
                option_warn("-i", "name listings (-n)")
            if name_list and name_list_multi:
                option_warn("-N", "-n")
        elif image_list:
            if full_list:
                option_warn("-l", "image listings (-i)")
            if name_list:
                option_warn("-n", "image listings (-i)")
        if setcode:
            option_warn("-s", "listings")

        if name_list_multi:
            name_list = True

        cardlist, total = list_cards(
            db,
            query,
            image_columns=image_list,
            image_compact=compact,
            onlynames=name_list,
            onename=not name_list_multi,
            header=header,
            sort=sort,
            reverse=reverse,
            limit=limit,
            ansi=ansi,
        )
        if cardlist:
            print(cardlist)
        if verbose:
            print("{:d} matches".format(total))

    else:

        if not header:
            option_warn("-q", "card printings")

        try:
            cardprint = get_and_print_card(
                db,
                query,
                setcode,
                format,
                image=not compact,
                ansi=ansi,
                rulings=rulings,
                verbose=verbose,
            )
        except ValueError as e:
            print("error:", e, file=sys.stderr)
            sys.exit(1)
        else:
            print(cardprint)


if __name__ == "__main__":
    main()
