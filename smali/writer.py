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
Contains standard implementations for Smali writers that are able
to procude classes, method, fields and annotations.
"""

from smali.visitor import ClassVisitor, MethodVisitor, FieldVisitor, AnnotationVisitor
from smali.base import AccessType, Token
from smali.reader import SupportsCopy, SmaliReader
from smali import opcode

__all__ = ["SmaliWriter", "FieldWriter", "MethodWriter", "AnnotationWriter"]


class _ContainsCodeCache(SupportsCopy):
    """Interface to make sure the code cache is returned via a method."""

    def get_cache(self) -> "_CodeCache":
        """Returns the current code cache.

        :return: the code cache
        :rtype: _CodeCache
        """

    def copy(self, line: str, context: type = ClassVisitor) -> None:
        if isinstance(self, context):
            self.get_cache().add(line)

        else:
            last_writer = self.get_cache().peek()
            if not last_writer:
                self.get_cache().add(line)

            elif isinstance(last_writer, SupportsCopy):
                last_writer.copy(line, context)

            elif isinstance(last_writer, context):
                last_writer.get_cache().add(line)


class _CodeCache:
    """Simple container class for a code cache.

    :param indent: the indentation level of this code, defaults to 0
    :type indent: int, optional
    """

    default_indent = "    "

    def __init__(self, indent=0) -> None:
        self.__indent = indent
        self.__code = []
        self.__cache = []
        self.__comment_cache = []

    @property
    def indent(self) -> int:
        """Returns the indentation level

        :return: the indent amount
        :rtype: int
        """
        return self.__indent

    def add(
        self, line: str, start: str = "", end: str = "", custom_indent: int = -1
    ) -> None:
        """Appends the given line of code at the end of this cache.

        :param line: the line to add
        :type line: str
        :param start: additional prefix, defaults to ""
        :type start: str, optional
        :param end: additional suffix, defaults to ""
        :type end: str, optional
        """
        indent = self.default_indent * (
            self.indent if custom_indent == -1 else custom_indent
        )
        self.__code.append(start + indent + line + end)

    def add_to_cache(self, cache: "_ContainsCodeCache") -> None:
        """Appends the given code cache to the end of this cache.

        :param cache: the cache to append
        :type cache: _CodeCache
        """
        if cache:
            self.__cache.append(cache)

    def add_comment(self, comment: str) -> None:
        """Adds the given comment to the last line

        :param comment: the comment to add
        :type comment: str
        """
        line = self.__code[-1]
        new_line = line[:-1] if line[-1] == "\n" else str(line)
        new_line += f" # {comment}"
        if line[-1] == "\n":
            new_line += "\n"
        self.__code[-1] = new_line

    def pop_comments(self) -> list:
        """Clears the comment cache and returns all elements.

        :return: the comments that have been stored.
        :rtype: list
        """
        values = self.__comment_cache.copy()
        self.__comment_cache.clear()
        return values

    def apply_code_cache(self, clear_caches=False) -> None:
        """Applies stored caches to this one.

        The stored caches will be cleared and removed afterwards.

        :param clear_caches: whether sub-caches should be applied, defaults to False
        :type clear_caches: bool, optional
        """
        for element in self.__cache:
            cache = element.get_cache()
            end = (
                "\n"
                if isinstance(element, (_SmaliFieldWriter, _SmaliMethodWriter))
                else ""
            )
            if cache:
                self.add(cache.get_code(clear_cache=clear_caches), end=end)
                cache.clear()
        self.__cache.clear()

    def get_code(self, clear_cache=False) -> str:
        """Returns the Smali-Code

        :param clear_cache: whether cached objects should be applied first, defaults to False
        :type clear_cache: bool, optional
        :return: the source code as utf-8 string
        :rtype: str
        """
        if clear_cache:
            self.apply_code_cache(True)
        return "\n".join(self.__code)

    def clear(self) -> None:
        """Clears this cache."""
        self.__cache.clear()
        self.__comment_cache.clear()
        self.__code.clear()

    def peek(self) -> _ContainsCodeCache:
        """Returns the last element of this cache

        :return: the last element that contains itself a ``_CodeCache``
        :rtype: _ContainsCodeCache
        """
        if len(self.__cache) > 0:
            return self.__cache[-1]


##########################################################################################
# ANNOTATION IMPLEMENTATION
##########################################################################################
class _SmaliAnnotationWriter(AnnotationVisitor, _ContainsCodeCache):
    cache: _CodeCache

    def __init__(
        self, delegate: "AnnotationVisitor" = None, indent=0, name=Token.ANNOTATION
    ) -> None:
        super().__init__(delegate)
        self.cache = _CodeCache(indent)
        self._name = name

    def get_cache(self) -> "_CodeCache":
        return self.cache

    def visit_value(self, name: str, value) -> None:
        super().visit_value(name, value)
        indent = self.cache.indent + 1
        self.cache.add(f"{name} = {value}", custom_indent=indent)

    def visit_enum(self, name: str, owner: str, const: str, value_type: str) -> None:
        super().visit_enum(name, owner, const, value_type)
        indent = self.cache.indent + 1
        self.cache.add(
            f"{name} = .{Token.ENUM} {owner}->{const}:{value_type}",
            custom_indent=indent,
        )

    def visit_subannotation(
        self, name: str, access_flags: int, signature: str
    ) -> "AnnotationVisitor":
        delegate = super().visit_subannotation(name, access_flags, signature)
        desc = f"{name} = .{Token.SUBANNOTATION} {signature}"
        a_visitor = _SmaliAnnotationWriter(
            delegate, self.cache.indent + 1, Token.SUBANNOTATION
        )

        a_visitor.cache.add(desc)
        self.cache.add_to_cache(a_visitor)
        return a_visitor

    def visit_array(self, name: str, values: list) -> None:
        indent_value = self.cache.default_indent
        indent = self.cache.indent

        if len(values) == 0:
            self.cache.add("%s = {}" % name, custom_indent=indent + 1)  # noqa
        else:
            sep_value = ",\n" + indent_value * (indent + 2)
            self.cache.add(
                "%s = {\n%s%s\n%s}"
                % (
                    name,
                    indent_value * (indent + 2),
                    sep_value.join(values),
                    indent_value * (indent + 1),
                ),
                custom_indent=indent + 1,
            )
        return super().visit_array(name, values)

    def visit_comment(self, text: str) -> None:
        super().visit_comment(text)
        self.cache.add(f"# {text}")

    def visit_eol_comment(self, text: str) -> None:
        super().visit_eol_comment(text)
        self.cache.add_comment(text)

    def visit_end(self) -> None:
        super().visit_end()
        self.cache.apply_code_cache(clear_caches=True)
        self.cache.add(f".{Token.END} {self._name}\n")


##########################################################################################
# FIELD IMPLEMENTATION
##########################################################################################
class _SmaliFieldWriter(FieldVisitor, _ContainsCodeCache):
    cache: _CodeCache

    def __init__(self, delegate: "FieldVisitor" = None, indent=0) -> None:
        super().__init__(delegate)
        self.cache = _CodeCache(indent)

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        delegate = super().visit_annotation(access_flags, signature)
        desc = f".{Token.ANNOTATION} {' '.join(AccessType.get_names(access_flags))} {signature}"
        a_visitor = _SmaliAnnotationWriter(delegate, self.cache.indent + 1)

        a_visitor.cache.add(desc)
        self.cache.add_to_cache(a_visitor)
        return a_visitor

    def get_cache(self) -> "_CodeCache":
        return self.cache

    def visit_comment(self, text: str) -> None:
        super().visit_comment(text)
        self.cache.add(f"# {text}")

    def visit_eol_comment(self, text: str) -> None:
        super().visit_eol_comment(text)
        self.cache.add_comment(text)

    def visit_end(self) -> None:
        super().visit_end()
        self.cache.apply_code_cache(True)
        self.cache.add(f".{Token.END} {Token.FIELD}")


##########################################################################################
# METHOD IMPLEMENTATION
##########################################################################################
class _SmaliMethodWriter(MethodVisitor, _ContainsCodeCache):
    cache: _CodeCache

    def __init__(self, delegate: "MethodVisitor" = None, indent=0) -> None:
        super().__init__(delegate)
        self.cache = _CodeCache(indent)

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        delegate = super().visit_annotation(access_flags, signature)
        desc = f".{Token.ANNOTATION} {' '.join(AccessType.get_names(access_flags))} {signature}"
        a_visitor = _SmaliAnnotationWriter(delegate, self.cache.indent + 1)

        a_visitor.cache.add(desc)
        self.cache.add_to_cache(a_visitor)
        return a_visitor

    def visit_block(self, name: str) -> None:
        self.cache.apply_code_cache(True)
        super().visit_block(name)
        self.cache.add(f":{name}", custom_indent=self.cache.indent + 1)

    def visit_line(self, number: int) -> None:
        self.cache.apply_code_cache(True)
        super().visit_line(number)
        self.cache.add(f".{Token.LINE} {number}", custom_indent=self.cache.indent + 1)

    def visit_goto(self, block_name: str) -> None:
        self.cache.apply_code_cache(True)
        super().visit_goto(block_name)
        self.cache.add(
            f"{opcode.GOTO} :{block_name}", custom_indent=self.cache.indent + 1
        )

    def visit_instruction(self, ins_name: str, args: list) -> None:
        self.cache.apply_code_cache(True)
        super().visit_instruction(ins_name, args)
        self.cache.add(
            f"{ins_name} {', '.join(args)}",
            custom_indent=self.cache.indent + 1,
            end="\n",
        )

    def visit_param(self, register: str, name: str) -> None:
        self.cache.apply_code_cache(True)
        super().visit_param(register, name)
        self.cache.add(
            f'.{Token.PARAM} {register} "{name}"', custom_indent=self.cache.indent + 1
        )

    def visit_comment(self, text: str) -> None:
        super().visit_comment(text)
        self.cache.add(f"# {text}", custom_indent=self.cache.indent + 1)

    def visit_restart(self, register: str) -> None:
        self.cache.apply_code_cache(True)
        super().visit_restart(register)
        self.cache.add(
            f".{Token.RESTART} {register}", custom_indent=self.cache.indent + 1
        )

    def visit_locals(self, local_count: int) -> None:
        self.cache.apply_code_cache(True)
        super().visit_locals(local_count)
        self.cache.add(
            f".{Token.LOCALS} {local_count}", custom_indent=self.cache.indent + 1
        )

    def visit_local(
        self, register: str, name: str, descriptor: str, full_descriptor: str
    ) -> None:
        self.cache.apply_code_cache(True)
        super().visit_local(register, name, descriptor, full_descriptor)
        self.cache.add(
            f'.{Token.LOCAL} {register}, "{name}":{descriptor}, "{full_descriptor}"',
            custom_indent=self.cache.indent + 1,
        )

    def visit_prologue(self) -> None:
        self.cache.apply_code_cache(True)
        super().visit_prologue()
        self.cache.add(f".{Token.PROLOGUE}", custom_indent=self.cache.indent + 1)

    def visit_catch(self, exc_name: str, blocks: tuple) -> None:
        self.cache.apply_code_cache(True)
        super().visit_catch(exc_name, blocks)
        start, end, catch = blocks
        self.cache.add(
            ".%s %s { :%s .. :%s } :%s" % (Token.CATCH, exc_name, start, end, catch),
            custom_indent=self.cache.indent + 1,
        )

    def visit_catchall(self, exc_name: str, blocks: tuple) -> None:
        self.cache.apply_code_cache(True)
        super().visit_catchall(exc_name, blocks)
        start, end, catch = blocks
        self.cache.add(
            ".%s { :%s .. :%s } :%s" % (Token.CATCHALL, start, end, catch),
            custom_indent=self.cache.indent + 1,
            end="\n",
        )

    def visit_registers(self, registers: int) -> None:
        self.cache.apply_code_cache(True)
        super().visit_registers(registers)
        self.cache.add(
            f".{Token.REGISTERS} {registers}",
            custom_indent=self.cache.indent + 1,
            end="\n",
        )

    def visit_return(self, ret_type: str, args: list) -> None:
        self.cache.apply_code_cache(True)
        super().visit_return(ret_type, args)
        if ret_type:
            ret_type = f"-{ret_type}"

        self.cache.add(
            f"return{ret_type} {' '.join(args)}", custom_indent=self.cache.indent + 1
        )

    def visit_invoke(self, inv_type: str, args: list, owner: str, method: str) -> None:
        self.cache.apply_code_cache(True)
        super().visit_invoke(inv_type, args, owner, method)
        self.cache.add(
            "invoke-%s { %s }, %s->%s" % (inv_type, ", ".join(args), owner, method),
            custom_indent=self.cache.indent + 1,
            end="\n",
        )

    def visit_array_data(self, length: str, value_list: list) -> None:
        self.cache.apply_code_cache(True)
        super().visit_array_data(length, value_list)
        indent_value = self.cache.default_indent * (self.cache.indent + 2)
        sep_value = "\n" + indent_value
        value_list = map(hex, value_list)
        self.cache.add(
            f".{Token.ARRAYDATA} {length}\n{indent_value}{sep_value.join(value_list)}\n.{Token.END} {Token.ARRAYDATA}",
            end="\n",
        )

    def visit_packed_switch(self, value: str, blocks: list) -> None:
        self.cache.apply_code_cache(True)
        super().visit_packed_switch(value, blocks)
        indent_value = self.cache.default_indent * (self.cache.indent + 2)
        sep_value = "\n" + indent_value + ":"
        self.cache.add(
            f".{Token.PACKEDSWITCH} {value}\n{indent_value}:{sep_value.join(blocks)}\n.{Token.END} {Token.PACKEDSWITCH}",
            end="\n",
        )

    def visit_sparse_switch(self, branches: dict) -> None:
        self.cache.apply_code_cache(True)
        super().visit_sparse_switch(branches)
        indent_value = self.cache.default_indent * (self.cache.indent + 2)
        values = [f"{x} -> :{y}" for x, y in branches.items()]
        sep_value = "\n" + indent_value
        self.cache.add(f".{Token.SPARSESWITCH}\n{indent_value}{sep_value.join(values)}\n.{Token.END} {Token.SPARSESWITCH}")

    def visit_eol_comment(self, text: str) -> None:
        super().visit_eol_comment(text)
        self.cache.add_comment(text)

    def visit_end(self) -> None:
        self.cache.apply_code_cache(True)
        super().visit_end()
        self.cache.add(f".{Token.END} {Token.METHOD}")

    def get_cache(self) -> "_CodeCache":
        return self.cache


##########################################################################################
# CLASS IMPLEMENTATION
##########################################################################################
class _SmaliClassWriter(ClassVisitor, _ContainsCodeCache):
    """Public standard implementation of a Smali Source-Code writer."""

    cache: _CodeCache
    """The code cache to use."""

    def __init__(self, reader: SmaliReader = None, indent=0) -> None:
        super().__init__()
        self.cache = _CodeCache(indent)
        if reader:
            reader.copy_handler = self

    def __str__(self) -> str:
        return self.code

    @property
    def code(self) -> str:
        """Returns the source code as an utf-8 string

        :return: the complete source code
        :rtype: str
        """
        return self.cache.get_code(clear_cache=True)

    def reset(self) -> None:
        """Resets the writer.

        Use this method before calling #visit() to ensure the internal
        buffer is cleared.
        """
        self.cache.clear()

    def get_cache(self) -> "_CodeCache":
        return self.cache

    ######################################################################################
    # INTERNAL
    ######################################################################################
    def visit_class(self, name: str, access_flags: int) -> None:
        super().visit_class(name, access_flags)
        flags = " ".join(AccessType.get_names(access_flags))
        self.cache.add(f".{Token.CLASS} {flags} {name}")

    def visit_super(self, super_class: str) -> None:
        super().visit_super(super_class)
        self.cache.add(f".{Token.SUPER} {super_class}\n")

    def visit_implements(self, interface: str) -> None:
        super().visit_implements(interface)
        self.cache.add(f".{Token.IMPLEMENTS} {interface}")

    def visit_source(self, source: str) -> None:
        super().visit_source(source)
        self.cache.add(f'.{Token.SOURCE} "{source}"\n')

    def visit_field(
        self, name: str, access_flags: int, field_type: str, value=None
    ) -> FieldVisitor:
        delegate = super().visit_field(name, access_flags, field_type, value)
        flags = " ".join(AccessType.get_names(access_flags))
        desc = f".{Token.FIELD} {flags} {name}:{field_type}"
        if value:
            # String values come with their '"' characters
            desc = f"{desc} = {value}"

        f_visitor = _SmaliFieldWriter(delegate, self.cache.indent)
        f_visitor.cache.add(desc)
        self.cache.add_to_cache(f_visitor)
        return f_visitor

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        delegate = super().visit_annotation(access_flags, signature)
        flags = " ".join(AccessType.get_names(access_flags))
        desc = f".{Token.ANNOTATION} {flags} {signature}"
        a_visitor = _SmaliAnnotationWriter(delegate, self.cache.indent)

        a_visitor.cache.add(desc)
        self.cache.add_to_cache(a_visitor)
        return a_visitor

    def visit_inner_class(self, name: str, access_flags: int) -> ClassVisitor:
        delegate = super().visit_inner_class(name, access_flags)
        flags = " ".join(AccessType.get_names(access_flags))
        desc = f".{Token.CLASS} {flags} {name}"

        c_visitor = _SmaliClassWriter(delegate)
        c_visitor.cache.add(desc)
        self.cache.add_to_cache(c_visitor)
        return c_visitor

    def visit_method(
        self, name: str, access_flags: int, parameters: list, return_type: str
    ) -> MethodVisitor:
        delegate = super().visit_method(name, access_flags, parameters, return_type)
        flags = " ".join(AccessType.get_names(access_flags))
        params = "".join(parameters)
        desc = f".{Token.METHOD} {flags} {name}({params}){return_type}"

        m_visitor = _SmaliMethodWriter(delegate, self.cache.indent)
        m_visitor.cache.add(desc)
        self.cache.add_to_cache(m_visitor)
        return m_visitor

    def visit_comment(self, text: str) -> None:
        self.cache.apply_code_cache(True)
        super().visit_comment(text)
        self.cache.add(f"# {text}")

    def visit_eol_comment(self, text: str) -> None:
        super().visit_eol_comment(text)
        self.cache.add_comment(text)

    def visit_debug(self, enabled: int) -> None:
        super().visit_debug(enabled)
        self.cache.add(f".{Token.DEBUG} {enabled}")

    def visit_end(self) -> None:
        self.cache.apply_code_cache(True)
        super().visit_end()

    def copy(self, line: str, context: type = ClassVisitor) -> None:
        if context == ClassVisitor:
            self.cache.add(line)

        else:
            last_writer = self.cache.peek()
            if not last_writer:
                self.cache.add(line)

            elif isinstance(last_writer, SupportsCopy):
                last_writer.copy(line, context)

            elif isinstance(last_writer, (context, _ContainsCodeCache)):
                last_writer.get_cache().add(line)

            else:
                print("Line excluded:", line, "<context> =", context)


##########################################################################################
# EXPORTS
##########################################################################################
SmaliWriter = _SmaliClassWriter
FieldWriter = _SmaliFieldWriter
MethodWriter = _SmaliMethodWriter
AnnotationWriter = _SmaliAnnotationWriter
