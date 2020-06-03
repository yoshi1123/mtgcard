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

"""The command-line 'Magic The Gathering' card search."""


def get_defaults():
    """Set default options."""
    try:
        from mtgcard import settings
    except ImportError as e:
        global settings

        class settings:
            ANSI_COLOR = True
            DEFAULT_FORMAT = ""
            CURRENCY = "USD"
            US_TO_CUR_RATE = 1
            SHOWN_FORMATS = [
                "standard",
                "brawl",
                "pioneer",
                "pauper",
                "modern",
                "legacy",
                "commander",
                "vintage",
            ]

    if "ANSI_COLOR" not in dir(settings):
        settings.ANSI_COLOR = True
    if "DEFAULT_FORMAT" not in dir(settings):
        settings.DEFAULT_FORMAT = None
    if "CURRENCY" not in dir(settings):
        settings.CURRENCY = "USD"
    if "US_TO_CUR_RATE" not in dir(settings):
        settings.US_TO_CUR_RATE = 1


get_defaults()
