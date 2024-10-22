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
import os
import sys
import traceback
import pprint

from cmd import Cmd

from smali import (
    AccessType,
    opcode,
    SmaliValue,
    MethodVisitor,
    ClassVisitor,
    FieldVisitor,
    SmaliReader,
)
from smali.bridge import (
    Frame,
    executor,
    SmaliObject,
    SmaliClass,
    SmaliField,
    SmaliMethod,
)
from smali.bridge.vm import (
    SmaliVMClassReader,
    SmaliVMMethodReader,
    SmaliVMFieldReader,
    SmaliVM,
)

SMALI_SCRIPT_SUFFIX = "ssf"
"""File suffix for Smali-Script files"""


class DefaultVisitor(MethodVisitor, ClassVisitor):
    """Visitor implementation that handles both class and method definitions"""

    frame: Frame
    """The root method context"""

    cls: SmaliVMClassReader
    """The root class"""

    shell: "ISmaliShell"
    """The shell reference"""

    last_label: str
    """Stores the last label that has been typed"""

    importing: bool = False

    def __init__(self, shell: "ISmaliShell") -> None:
        super().__init__(None)
        self.shell = shell
        self.frame = Frame()
        self.last_label = None
        self.pos = 0

        self.frame.vm = shell.emulator
        self.reset_var("p0", shell.root)

    def visit_restart(self, register: str) -> None:
        if register != "p0":
            self.reset_var(register)
        else:
            self.reset_var(register, self.shell.root)

    def reset_var(self, register: str, val=None):
        """Applies a new value to the given register name"""
        self.frame.registers[register] = val

    def visit_block(self, name: str) -> None:
        self.frame.labels[name] = self.pos
        self.pos += 1
        self.last_label = name
        self.frame.label = name

    def visit_registers(self, registers: int) -> None:
        for i in range(registers):
            self.reset_var(f"v{i}")

    def visit_locals(self, local_count: int) -> None:
        self.visit_registers(local_count)

    def visit_catch(self, exc_name: str, blocks: tuple) -> None:
        start, _, handler = blocks
        self.frame.catch[start] = (exc_name, handler)

    def visit_catchall(self, exc_name: str, blocks: tuple) -> None:
        self.visit_catch(exc_name, blocks)

    def visit_instruction(self, ins_name: str, args: list) -> None:
        for _, value in opcode.__dict__.items():
            if value == ins_name:
                exc = executor.get_executor(ins_name)
                exc.args = args
                exc(self.frame)
                self.pos += 1

                if "return" in value:
                    print(self.frame.return_value)
                return

        if self.importing:
            self.shell.onecmd(f"{ins_name} {' '.join(args)}")
        else:
            raise SyntaxError(f"Invalid OpCode: {ins_name}")

    def visit_field(
        self, name: str, access_flags: int, field_type: str, value=None
    ) -> FieldVisitor:
        field = SmaliField(
            field_type,
            self.shell.root.smali_class,
            f"{name}:{field_type}",
            access_flags,
            name,
            value=SmaliValue(value) if value else None,
        )
        self.shell.root.smali_class[name] = field
        if access_flags not in AccessType.STATIC and value is not None:
            self.shell.root[name] = value

        return SmaliVMFieldReader(field)

    def visit_return(self, ret_type: str, args: list) -> None:
        if ret_type:
            self.visit_instruction(f"return-{ret_type}", args)
        else:
            self.visit_instruction("return", args)

    def visit_invoke(self, inv_type: str, args: list, owner: str, method: str) -> None:
        if inv_type:
            self.visit_instruction(
                f"invoke-{inv_type}", [inv_type, args, owner, method]
            )
        else:
            self.visit_instruction("invoke", [inv_type, args, owner, method])

    def visit_method(
        self, name: str, access_flags: int, parameters: list, return_type: str
    ) -> MethodVisitor:
        signature = f"{name}({''.join(parameters)}){return_type}"
        smali_class = self.shell.root.smali_class

        method = SmaliMethod(self.shell.emulator, smali_class, signature, access_flags)
        visitor = SmaliVMMethodReader(method)
        self.shell.emulator.new_frame(method, visitor.frame)
        smali_class[name] = method
        return visitor

    def visit_inner_class(self, name: str, access_flags: int) -> "ClassVisitor":
        if self.importing:
            smali_class = self.shell.root.smali_class
            inner = SmaliClass(smali_class, name, access_flags)

            smali_class[name] = inner
            return SmaliVMClassReader(self.shell.emulator, inner)


class ISmaliShell(Cmd):
    """Implementation of an interactive Smali-Interpreter."""

    DEFAULT_PROMPT = ">>> "
    """The default prompt"""

    INLINE_PROMPT = "... "
    """Prompt used for field and method definitions"""

    visitor: DefaultVisitor
    """The default visitor instance"""

    reader: SmaliReader
    """The reader used to parse code snippets."""

    emulator: SmaliVM
    """The actual VM reference that will execute each method"""

    root: SmaliObject
    """The base context used to define fields and methods."""

    prompt: str = ">>> "
    """The prompt used by ``cmd.Cmd``"""

    check_import: bool = True
    """Used to indicate whether this shell should verify each import"""

    __imported_files: list = []
    """Internal file list"""

    def __init__(self) -> None:
        super().__init__()
        self.stack = []
        self.reader = SmaliReader(comments=False, snippet=True)
        self.emulator = SmaliVM()

        cls = SmaliClass(None, "L<Root>;", AccessType.PUBLIC + AccessType.FINAL)
        self.emulator.new_class(cls)
        self.root = SmaliObject(cls)
        self.visitor = DefaultVisitor(self)

    def do_import(self, path: str) -> None:
        """usage: import <file>

        This command will try to import the given smali file or
        Smali-Script file (.ssf). Note that files with wrong suffixes
        will be ignored.
        """
        if not os.path.exists(path):
            print(f'! Could not find file at "{path}"')
            return

        if path in self.__imported_files and self.check_import:
            return

        if not path.endswith((".smali", f".{SMALI_SCRIPT_SUFFIX}")):
            print(f"! Unknown file format (unknown suffix) at '{path}'")
            return

        cls = None
        with open(path, "r", encoding="utf-8") as source:
            self.__imported_files.append(path)
            if path.endswith(f".{SMALI_SCRIPT_SUFFIX}"):
                self.visitor.importing = True
                self.reader.visit(source, self.visitor)
                self.visitor.importing = False
            else:
                cls = self.emulator.classloader.load_class(source, init=False)

        try:
            if cls is not None:
                cls.clinit()
        except Exception:  # :noqa
            print(traceback.format_exc())

    def do_vars(self, _):
        """usage: vars

        Prints all variables with the help of ``pprint``.
        """
        pprint.pprint(self.visitor.frame.registers)

    def do_fields(self, _):
        """usage: fields

        Prints all fields that have been defined in the root context.
        """
        pprint.pprint(list(self.root.smali_class.fields()))

    def do_label(self, _):
        """:usage label

        Prints the name of the active label.
        """
        print(self.visitor.frame.label)

    def do_del(self, register):
        """usage: del <register>

        Deletes the variable at the specified register. The root
        context at 'p0' can't be deleted.
        """
        if register == "p0":
            print("! Attempted to delete root-context - skipping...\n")
            return

        if register in self.visitor.frame.registers:
            val = self.visitor.frame.registers.pop(register)
            del val

    def precmd(self, line: str):
        if len(line) == 0:
            self.change_prompt(ISmaliShell.DEFAULT_PROMPT)
            return "EOF"

        return line

    def default(self, line: str) -> None:
        """Handles the instruction or register name

        :param line: the input line
        :type line: str
        """
        if line == "EOF":
            return

        if isinstance(self.visitor, DefaultVisitor):
            if line in self.visitor.frame.registers:
                print(self.visitor.frame.registers[line])
                return

        try:
            self.reader.visit(line, self.visitor)
        except Exception:
            print(traceback.format_exc())

    def do_exit(self, _):
        """Exits the interpreter"""
        sys.exit(0)

    def do_copyright(self, _):
        """Prints copyright information"""
        print("Copyright (C) 2023-2024 MatrixEditor")

    def change_prompt(self, new_prompt: str):
        """Changes the prompt (for later usage)"""
        self.prompt = new_prompt
