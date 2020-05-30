import sys
import os
import subprocess

this_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.abspath(os.path.join(this_dir, 'mtgcard/data'))
sqlite_file = os.path.join(data_dir, 'mtg.sqlite')
if not os.path.exists(sqlite_file):
    import mtgcard.update
    print( "DOWNLOAD MTGCARD DATA BEGIN" )
    print("generating database")
    mtgcard.update.update_database(verbose=True)
    print( "DOWNLOAD MTGCARD DATA END" )

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtgcard",
    version="0.1a1",
    description="The command-line 'Magic The Gathering' card search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoshi1123/mtgcard",
    # packages=setuptools.find_packages(include=['mtgcard']),
    packages=setuptools.find_packages(exclude=['tests']),
    package_data={
        'mtgcard': ['data/mtg.sqlite'],
        },
    entry_points={
        'console_scripts': [
            'mtgcard = mtgcard.main:main',
        ],
    },
    data_files=[('man/man1', ['doc/mtgcard.1'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
