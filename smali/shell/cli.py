# This file is part of pysmali's Smali API
# Copyright (C) 2023-2024 MatrixEditor

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import sys

from argparse import ArgumentParser

from smali import VERSION
from smali.shell import ISmaliShell


def start_cli():
    """Starts the Smali interpreter."""

    parser = ArgumentParser(
        description=(
            "ISmali (Interactive Smali interpreter) can execute Smali-Code snippets"
            "on the fly as well as import *.smali files and use them later on."
        )
    )
    parser.add_argument(
        "file",
        nargs="*",
        help=(
            "The Smali-Script files ('.ssf') to be interpreted. Note that"
            " files as input won't result in interactive mode. Use the '-i'"
            " flag to run the interactive mode afterwards."
        ),
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help=("Runs the interactive mode after executing/ importing input files."),
    )
    parser.add_argument(
        "--version", action="store_true", help="Stores the current interpreter version"
    )

    args = parser.parse_args().__dict__
    if args["version"]:
        print(VERSION)
        sys.exit(0)

    shell = ISmaliShell()
    files = args["file"]

    if len(files) > 0:
        for path in args["file"]:
            shell.do_import(path)

    if len(files) == 0 or args["interactive"]:
        shell.cmdloop(
            (
                f"ISmali {VERSION} on {sys.platform}\nType"
                " 'help' or 'copyright' for more information."
            )
        )
