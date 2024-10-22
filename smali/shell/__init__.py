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
__doc__ = """
Implementation of a "shell"-like interpreter that can be run interactively
or can execute smali files.

The options the ``smali.shell`` module accept are the following:

file [file ...]
    The Smali-Script files (``.ssf``) to be interpreted. Note that files
    as input won't result in interactive mode. Use the ``-i`` flag to run
    the interactive mode afterwards.

-i / --interactive
    Runs the interactive mode after executing/importing input files.

"""

from smali.shell.model import ISmaliShell, SMALI_SCRIPT_SUFFIX
from smali.shell.cli import start_cli

