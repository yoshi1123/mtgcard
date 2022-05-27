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

"""Update database."""

import sys
import urllib.request
import json
import ssl
import shutil
import os.path
import zipfile
import subprocess
import sqlite3
import pathlib

import mtgcard.update.json2sql
import mtgcard.update.indexes


def update_database(verbose=False):
    """Retrieve, generate, and index sqlite database.

    :param int verbose: whether to print the update process

    """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    json2sql = os.path.join(this_dir, "json2sql.py")
    data_dir = os.path.abspath(os.path.join(this_dir, "../data"))
    zip_file = os.path.join(data_dir, "download.zip")
    json_filename = "AllPrintings.json"
    json_file = os.path.join(data_dir, json_filename)
    sqlite_file = os.path.join(data_dir, "mtg.sqlite")

    pzip_file = os.path.join(data_dir, "pdownload.zip")
    pjson_filename = "AllPrices.json"
    pjson_file = os.path.join(data_dir, pjson_filename)

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    def vprint(*args):
        if verbose:
            print(*args)

    ############################################
    #  get AllPrintings.zip and AllPrices.zip  #
    ############################################

    cert_filename = "Baltimore_CyberTrust_Root.crt"
    capath = ssl._ssl.get_default_verify_paths()[3]
    cert = os.path.join(capath, "Baltimore_CyberTrust_Root.pem")
    if os.path.exists(cert):
        vprint("  CA certificate:", cert)
        cxt = ssl.create_default_context(cafile=cert)
    else:
        vprint("  CA certificate: system default CA path")
        cxt = None

    # url = "https://www.mtgjson.com/files/AllPrintings.json.zip"
    url = "https://www.mtgjson.com/api/v5/AllPrintings.json.zip"
    req = urllib.request.Request(url)
    req.add_header("Accept-Language", "en-US,en;q=0.5")
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
    )
    price_url = "https://www.mtgjson.com/api/v5/AllPrices.json.zip"
    preq = urllib.request.Request(price_url)
    preq.add_header("Accept-Language", "en-US,en;q=0.5")
    preq.add_header(
        "User-Agent",
        "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11",
    )

    with urllib.request.urlopen(req, context=cxt) as contents:
        with open(zip_file, "wb") as f:
            vprint("  downloading '{}' to '{}'...".format(url, zip_file))
            shutil.copyfileobj(contents, f)
            vprint("  download complete")

    with urllib.request.urlopen(preq, context=cxt) as contents:
        with open(pzip_file, "wb") as f:
            vprint("  downloading '{}' to '{}'...".format(price_url, pzip_file))
            shutil.copyfileobj(contents, f)
            vprint("  download complete")

    ##############################################
    #  unzip AllPrintings.zip and AllPrices.zip  #
    ##############################################

    with zipfile.ZipFile(zip_file) as zf:
        vprint("  extracting '{}' to '{}'...".format(zip_file, data_dir))
        zf.extract(json_filename, path=data_dir)
        vprint("  extraction complete")

    with zipfile.ZipFile(pzip_file) as zf:
        vprint("  extracting '{}' to '{}'...".format(pzip_file, data_dir))
        zf.extract(pjson_filename, path=data_dir)
        vprint("  extraction complete")

    ########################
    #  convert to sqlite3  #
    ########################

    if os.path.exists(sqlite_file):
        os.remove(sqlite_file)
    vprint("  generating database file...")

    infile = pathlib.Path(json_file)
    outfile = {"path": pathlib.Path(sqlite_file), "handle": None}
    try:
        result = mtgcard.update.json2sql.execute(infile, outfile,
                check_extras=True)
    except Exception:
        vprint("error creating database file")
        sys.exit(1)
    else:
        vprint("  database file complete")

    with sqlite3.connect(sqlite_file) as conn:
        cursor = conn.cursor()
        cursor.executescript(mtgcard.update.indexes.indexes)

    if verbose:
        print("success -- update of '{}' complete".format(sqlite_file))
    else:
        print("success -- update complete")

    ##############
    #  clean up  #
    ##############

    os.remove(zip_file)
    os.remove(json_file)
    os.remove(pzip_file)
    os.remove(pjson_file)
