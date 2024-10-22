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
Execution frame objects are used within method calls the Smali
emulator. They store the current opcode position, label and values
of all registers in the current context.

On top of that, ``Frame`` objects store method return values (sub-
calls) as well as the final return value. If any errors occur, they
will be stored in a separate variable.
"""

from smali.bridge.errors import ExecutionError, NoSuchRegisterError


class Frame:
    """Class to represent execution frames.

    There are different special functions implemented to simplify
    the process of getting and setting register values:

    >>> value = frame["v0"]
    0
    >>> "v0" in frame
    True
    >>> frame["v0"] = 1
    >>> for register_name in frame:
    ...     value = frame[register_name]
    """

    labels: dict = {}
    """A mapping with labels to their execution position."""

    return_value: object = None
    """Stores a return value of the current method."""

    method_return: object = None
    """Stores the latest method return value"""

    opcodes: list = []
    """Stores all parsed opcodes with their arguments"""

    finished: bool = False
    """Stores whether te current frame has been executed."""

    pos: int = 0
    """The current position in opcode list"""

    label: str
    """The current label context"""

    error: ExecutionError
    """Defines the current execution error"""

    registers: dict
    """Stores values for the current registers."""

    catch: dict
    """Stores all try-catch handlers.

    Note that teh stored handlers will be tuples with
    the exception type and the handler block"""

    array_data: dict
    """Stores all array-data objecs mapped to their label."""

    vm = None
    """VM reference"""

    switch_data: dict
    """Stores packed and sparse-switch data"""

    parent: "Frame" = None
    """Parent execution context (mainly used for backtracking)"""

    def __init__(self):
        self.registers = {}
        self.opcodes = []
        self.labels = {}
        self.catch = {}
        self.array_data = {}
        self.switch_data = {}
        self.reset()

    def reset(self) -> None:
        """Resets this frame and removes execution information."""
        self.label = None
        self.error = None
        self.finished = False
        self.pos = 0
        self.return_value = None
        self.parent = None
        self.registers.clear()

    def __getitem__(self, key: str):
        if key not in self.registers:
            raise NoSuchRegisterError(f"Register with name {key} not found!")

        return self.registers[key]

    def __setitem__(self, key: str, value):
        self.registers[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.registers

    def __iter__(self):
        return iter(self.registers)

    def __len__(self) -> int:
        return len(self.opcodes)
