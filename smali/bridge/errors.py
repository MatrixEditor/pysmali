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
Common exceptions of the Smali-Python-Bridge
"""

__all__ = [
    "NoSuchClassError",
    "NoSuchMethodError",
    "NoSuchFieldError",
    "NoSuchRegisterError",
    "NoSuchOpcodeError",
    "InvalidOpcodeError",
    "ExecutionError",
]


class NoSuchClassError(Exception):
    """The class is not defined or wasn't found"""


class NoSuchMethodError(Exception):
    """The method is not defined"""


class NoSuchFieldError(Exception):
    """The requested field is not defined"""


class NoSuchRegisterError(Exception):
    """Unknown register was requested to be read"""


class NoSuchOpcodeError(Exception):
    """The opcode does not exists or no implementation is present"""


class InvalidOpcodeError(Exception):
    """The opcode is invalid"""


class ExecutionError(Exception):
    """Wrapper class for runtime exceptions."""

    name: str
    """The exception class name"""

    def __init__(self, name: str, *args: object) -> None:
        super().__init__(*args)
        self.name = name

    def __repr__(self) -> str:
        return f"<{self.name} at {id(self)}"

    def __str__(self) -> str:
        return super().__str__().replace("ExecutionError", self.name)
