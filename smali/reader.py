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
This module contains an implementation of a line-based Smali source code
parser. It can be used to parse Smali files as an output of a decompiling
routine.
"""

import io

from smali.visitor import (
    VisitorBase,
    ClassVisitor,
    FieldVisitor,
    AnnotationVisitor,
    MethodVisitor,
)
from smali.base import AccessType, Line, Token, SVMType, smali_value, is_type_descriptor
from smali.opcode import RETURN, GOTO


class SupportsCopy:
    """Interface for classes that can react as a copy handler for a SmaliReader.

    Note that the context is used to distinguish the current visitor.
    """

    def copy(self, line: str, context: type = ClassVisitor) -> None:
        """Copies the given line.

        :param line: the line to copy
        :type line: str
        """


EMPTY_ANNOV = AnnotationVisitor()
EMPTY_METHV = MethodVisitor()
EMPTY_FIELDV = FieldVisitor()
EMPTY_CLASSV = ClassVisitor()

class SmaliReader:
    """Basic implementation of a line-base Smali-SourceCode parser.

    :param validate: Indicates the reader should validate the input code, defaults to True
    :type validate: bool, optional
    :param comments: With this option enabled, the parser will also notify about
                        comments in the source file, defaults to False
    :type comments: bool, optional
    :param snippet: With this option enabled, the initial class definition will be
                    skipped, defaults to False
    :type snippet: bool, optional
    :param errors: Indicates whether this reader should throw errors (values: ``strict``, ``ignore``),
                    defaults to 'strict'
    :type errors: str, optional
    """

    validate: bool = False
    """Indicates the reader should validate the input code."""

    comments: bool = True
    """With this option enabled, the parser will also notify about
    comments in the source file."""

    snippet: bool = False
    """With this option enabled, the initial class definition will be skipped."""

    line: Line = Line(None)
    """The current line. (Mainly used for debugging purposes)"""

    source: io.IOBase
    """The source to read from."""

    stack: list = []
    """Stores the current visitors (index 0 stores the initial visitor)

    A null value indicates that no visitors are registered for the current parsing
    context.
    """

    errors: str = "strict"
    """Indicates whether this reader should throw errors (values: 'strict', 'ignore')"""

    copy_handler: SupportsCopy

    def __init__(
        self,
        validate: bool = True,
        comments: bool = False,
        snippet: bool = False,
        errors: str = "strict",
    ) -> None:
        self.validate = validate
        self.comments = comments
        self.snippet = snippet
        self.errors = errors
        self.copy_handler = None
        # check valid values
        if self.errors not in ("ignore", "strict"):
            raise ValueError(f"Invalid error handler: {errors}")

    def visit(self, source: io.IOBase, visitor: ClassVisitor) -> None:
        """Parses the given input which can be any readable source.

        :param source: the Smali source code
        :type source: io.IOBase | str | bytes
        :param visitor: the visitor to use, defaults to None
        :type visitor: ClassVisitor, optional
        :raises ValueError: If the provided values are null
        :raises TypeError: if the source type is not accepted
        :raises ValueError: if the source is not readable
        """
        if not visitor or not source:
            raise ValueError("Invalid source or visitor (nullptr)")

        # Wrap string and bytes instances automatically.
        if isinstance(source, str):
            source = io.StringIO(source)

        elif isinstance(source, bytes):
            source = io.BytesIO(source)

        # The TypeError is needed to provide information about
        # types we don't accept
        elif not isinstance(source, io.IOBase):
            raise TypeError(f"Invalid source type: {source.__class__}")

        if not source.readable():
            raise ValueError("Source object is not readable!")

        if self.errors not in ("ignore", "strict"):
            raise ValueError(f"Invalid error handling type: {self.errors}")

        self.source = source
        self.stack.append(visitor)

        # We need to parse the class definition first if needed
        if not self.snippet:
            self._class_def()
        self._do_visit()

    @property
    def _visitor(self) -> VisitorBase:
        """Returns the active visitor instance.

        :return: the active visitor.
        :rtype: ClassVisitor
        :meta public:
        """
        return self.stack[-1]

    def _next_line(self):
        """Reads until the next code statement.

        Comments will be returned to the visitory immediately.

        :param source: the source to read from
        :type source: io.IOBase
        :param visitor: the visitor to notify
        :type visitor: ClassVisitor
        :raises EOFError: if the end of file has beeen reached
        :meta public:
        """
        raw_line = None
        while True:
            raw_line = self.source.readline()
            # We need this check as the reader would loop forever,
            # because the IOBase implementations don't throw this error.
            if len(raw_line) == 0:
                raise EOFError()

            if isinstance(raw_line, bytes):
                raw_line = raw_line.decode()

            # Sort out blank lines without anything
            if not raw_line:
                continue

            self.line.reset(raw_line)
            # Comments will be returned immediately
            if raw_line.strip().startswith("#"):
                if self._visitor and self.comments:
                    self._visitor.visit_comment(self.line.eol_comment)
                elif not self._visitor and self.comments:
                    self._copy_line()
                continue

            # return nothing as the line object is defined globally
            break

    def _copy_line(self) -> None:
        if self.copy_handler:
            self.copy_handler.copy(self.line.raw, self._visitor.__class__)

    def _validate_token(self, token: str, expected: Token) -> None:
        """Validates the given token if validation is enabled.

        :param token: the token to verify
        :type token: str
        :param expected: the expected token value
        :type expected: str
        :raises SyntaxError: if validation failed
        :meta public:
        """
        if not self.validate:
            return

        if token[0] != ".":
            raise SyntaxError(f"Expected '.' before token - got '{token[0]}'")

        if token[1:] != expected:
            raise SyntaxError(f"Expected '{expected}' - got '{token[1:]}'")

    def _validate_descriptor(self, name: str) -> None:
        """Validates the given name if validation is enabled.

        :param name: the type descriptor, e.g. 'Lcom/example/ABC;'
        :type name: str
        :raises SyntaxError: if the provided string is not a valid descriptor
        :meta public:
        """
        if not self.validate:
            return

        if not is_type_descriptor(name):
            raise SyntaxError(f"Expected type descriptor - got '{name}'")

    def _publish_comment(self) -> None:
        """Publishes the EOL comment and notifies the given visitor

        :param visitor: the visitor to notify
        :type visitor: ClassVisitor | MethodVisitor | FieldVisitor | AnnotationVisitor
        """
        if self.line.has_eol() and self._visitor:
            self._visitor.visit_eol_comment(self.line.eol_comment)

    def _read_access_flags(self) -> list:
        """Tries to resolve all access flags of the current line

        :return: the list of access flags
        :rtype: list
        :meta public:
        """
        flags = []
        while True:
            # With find() we are looking for access type key-words
            # defined in the AccessType enum. If we don't find a
            # matching one, close this loop and assume we got a class
            # name left.
            if not AccessType.find(self.line.peek()):
                break

            flags.append(self.line.peek())
            next(self.line)
        return flags

    def _throw_eol(self, err):
        if self.errors == "strict":
            raise SyntaxError("Unexpected EOL (end of line)") from err

    def _collect_values(self, strip_chars=None) -> list:
        """Collects all values stored in the rest of the current line.

        Note that values will be splitted if ',' is in a value, for instance:
        >>> line = "const/16 b,0xB"
        >>> _collect_values(',')
        ['const/16', 'b', '0xB']

        :param strip_chars: the chars to strip first, defaults to None
        :type strip_chars: str, optional
        :return: the collected values
        :rtype: list
        :meta public:
        """
        i_values = []
        while self.line.has_next():
            value = next(self.line).rstrip(strip_chars)
            # As the Line object splits all values by ' ', strings can
            # be marked by their '"' at the start or end.
            if (
                value[0] not in ('"', "'")
                and value[-1] not in ('"', "'")
                and "," in value
            ):
                i_values.extend(value.split(","))
            else:
                i_values.append(value)
        return i_values

    def _do_visit(self) -> None:
        """Performs the source code visit.

        :param source: the source to read from
        :type source: io.IOBase
        :param visitor: the visitor to notify
        :type visitor: ClassVisitor
        :meta public:
        """
        try:
            # Maybe use a loop that only executed one method at time
            # so we don't have recursion
            while True:
                self._next_line()
                if len(self.line) == 0:
                    # These are just blank lines used in the original
                    # source file.
                    self._copy_line()
                    continue

                statement = self.line.peek()
                # Tokens start with a leading dot
                if statement[0] == ".":
                    self._handle_token()
                # The same with blocks and a ':'
                elif statement[0] == ":":
                    self._handle_block()

                elif isinstance(self._visitor, AnnotationVisitor):
                    self._handle_value()

                elif isinstance(self._visitor, MethodVisitor):
                    self._handle_instruction()

                else:
                    raise SyntaxError(f'Invalid statement: "{statement}"')

        except (EOFError, ValueError):
            # The error is needed to indicate the visitation should end
            while not isinstance(self._visitor, ClassVisitor):
                self.stack.pop()
            self._visitor.visit_end()

        except StopIteration as err:
            raise SyntaxError("Unexpected EOL (end of line)") from err

    def _handle_token(self):
        # Remove the leading dot first bevore comparison
        statement = self.line.peek()[1:]

        # If the current visitor is a FieldVisitor, it should
        # be removed if the statement is not of type .annnotation
        # or .end
        visitor = self._visitor
        if isinstance(visitor, FieldVisitor):
            if statement not in (Token.ANNOTATION, Token.END):
                self.stack.pop()

        if statement == Token.IMPLEMENTS:
            # The name validation is done by checking if the name
            # contains the type descriptor: 'Lcom/example/Class;'
            next(self.line)
            if self._visitor:
                name = self.line.peek()
                self._validate_descriptor(name)
                self._visitor.visit_implements(name)
                self._publish_comment()
            else:
                self._copy_line()

        elif statement == Token.CLASS:
            c_visitor = self._class_def(next_line=False, inner_class=True)
            self.stack.append(c_visitor)

        else:
            # Dynamic method calling, we just need to implement specific
            # token handling.
            method = f'_handle_{statement.replace("-", "_")}'
            callback = getattr(self, method, None)
            if callback is None:
                raise SyntaxError(f"Invalid token: {method!r} - not implemented!")

            callback()

    def _class_def(self, next_line=True, inner_class=False):
        """Parses (and verifies) the class definition.

        :param visitor: the visitor instance
        :type visitor: ClassVisitor
        :param next_line: whether the next line should be used, defaults to True
        :type next_line: bool, optional
        :param inner_class: whether the class is an inner class, defaults to False
        :type inner_class: bool, optional
        :raises SyntaxError: if EOF is reached
        :raises SyntaxError: if EOL is reached
        :return: an inner class ClassVisitor instance if inner_class it True
        :rtype: ClassVisitor | None
        :meta public:
        """
        if next_line:
            # Only parse the next line if we have to
            try:
                self._next_line()
            except EOFError as eof:
                # It should be possible to parse small code snippets.
                if not self.validate:
                    return
                raise SyntaxError("Expected a class defintion - got EOF") from eof

        try:
            # If validation is enabled, the '.class' token is verified
            token = next(self.line)
            self._validate_token(token, Token.CLASS)

            flags = self._read_access_flags()

            # The name validation is done by checking if the name
            # contains the type descriptor: 'Lcom/example/Class;'
            name = self.line.peek()
            self._validate_descriptor(name)

            access_flags = AccessType.get_flags(flags)
            if not inner_class:
                c_visitor = self._visitor
                self._visitor.visit_class(name, access_flags)
            else:
                c_visitor = self._visitor.visit_inner_class(name, access_flags)

            # Don't forget the comment
            self._publish_comment()
            return c_visitor or EMPTY_CLASSV
        except StopIteration as err:
            self._throw_eol(err)

    ###########################################################################################
    # TOKEN IMPLEMENTATION
    ###########################################################################################

    def _handle_super(self) -> None:
        try:
            # If validation is enabled, the '.super' token is verified
            token = next(self.line)
            self._validate_token(token, Token.SUPER)

            super_class = self.line.peek()
            if not is_type_descriptor(super_class):
                raise SyntaxError(
                    f"Expected super-class type descriptor - got '{super_class}'"
                )

            if self._visitor:
                # Visit the class afterwards
                self._visitor.visit_super(super_class)
            else:
                self._copy_line()
            self._publish_comment()
        except StopIteration as err:
            self._throw_eol(err)

    def _handle_source(self) -> None:
        """Handles .source definitions and their comments.

        :param visitor: the visitor to notify
        :type visitor: ClassVisitor
        :meta public:
        """
        try:
            token = next(self.line)
            self._validate_token(token, Token.SOURCE)

            source = self.line.peek().replace('"', "")
            if self._visitor:
                self._visitor.visit_source(source)
            else:
                self._copy_line()
            self._publish_comment()
        except StopIteration as err:
            self._throw_eol(err)

    def _handle_field(self) -> None:
        try:
            # If validation is enabled, the '.class' token is verified
            token = next(self.line)
            self._validate_token(token, Token.FIELD)

            flags = self._read_access_flags()
            access_flags = AccessType.get_flags(flags)

            # The structure of a field's name is the following:
            #   - <name>:<descriptor>
            name, descriptor = next(self.line).split(":")
            self._validate_descriptor(descriptor)

            # Handle bracket names
            name = name.rstrip(">").lstrip("<")

            # If we have a direct assignment, we should parse the value
            value = None
            if self.line.has_next():
                value = self.line.last()

            if self._visitor:
                f_visitor = self._visitor.visit_field(
                    name, access_flags, descriptor, value
                )
                self._publish_comment()
            else:
                f_visitor = EMPTY_FIELDV

            self.stack.append(f_visitor if f_visitor else EMPTY_FIELDV)
            if not f_visitor or f_visitor == EMPTY_FIELDV:
                self._copy_line()

        except StopIteration as err:
            self._throw_eol(err)

    def _handle_end(self) -> None:
        """Removes the active visitor from the stack.

        :meta public:
        """
        # NOTE: As posted in issue #2, the reader would throw a SyntaxError upon
        # end-statements that store more than two elements (e.g. '.end local v2').
        # Here, we first skip the '.end' statement and then resolve the next line
        # element.
        next(self.line)
        directive = self.line.peek()
        if directive in (Token.LOCAL, Token.PARAM):
            self._copy_line()
            return

        visitor = self.stack.pop()
        if visitor and visitor not in (EMPTY_ANNOV, EMPTY_FIELDV, EMPTY_METHV):
            visitor.visit_end()
        else:
            self._copy_line()

    def _handle_method(self) -> None:
        try:
            token = next(self.line)
            self._validate_token(token, Token.METHOD)

            flags = self._read_access_flags()
            access_flags = AccessType.get_flags(flags)

            # We don't need to verify the signature as this is done
            # in the SVMType class
            signature = SVMType(self.line.peek()).signature
            if not signature:
                raise SyntaxError(f"Expected a method signature - got {signature}")

            m_visitor = EMPTY_METHV
            if self._visitor:
                m_visitor = self._visitor.visit_method(
                    signature.name,
                    access_flags,
                    [str(x) for x in signature.parameter_types],
                    str(signature.return_type),
                )

            # Add the visitor first before publishing the comment
            self.stack.append(m_visitor if m_visitor else EMPTY_METHV)
            self._publish_comment()
            # The line will be copied if no visitor has been set
            if not m_visitor or m_visitor == EMPTY_METHV:
                self._copy_line()
        except StopIteration as err:
            self._throw_eol(err)

    def _handle_annotation(self) -> None:
        """Annotations are special as they can contain .enum or .subannotation

        Note that the annotation will only be visited if the annotation visitor
        is not null.
        :meta public:
        """
        try:
            token = next(self.line)
            self._validate_token(token, Token.ANNOTATION)

            flags = self._read_access_flags()
            access_flags = AccessType.get_flags(flags)

            descriptor = self.line.peek()
            self._validate_descriptor(descriptor)

            a_visitor = EMPTY_ANNOV
            if self._visitor:
                a_visitor = self._visitor.visit_annotation(access_flags, descriptor)

            self.stack.append(a_visitor if a_visitor else EMPTY_ANNOV)
            self._publish_comment()
            if not a_visitor or a_visitor == EMPTY_ANNOV:
                self._copy_line()
        except StopIteration as err:
            self._throw_eol(err)

    def _handle_subannotation(self) -> None:
        """Handles .subannotation definitions."""
        try:
            token = next(self.line)
            self._validate_token(token, Token.SUBANNOTATION)

            # As we need the annotation value's name, we have to
            # use the cleaned line buffer in the current line object.
            name = self.line.cleaned[:self.line.cleaned.find("=")].strip()
            flags = self._read_access_flags()
            access_flags = AccessType.get_flags(flags)

            descriptor = self.line.peek()
            self._validate_descriptor(descriptor)

            a_visitor = EMPTY_ANNOV
            if self._visitor and self._visitor != EMPTY_ANNOV:
                a_visitor = self._visitor.visit_subannotation(
                    name, access_flags, descriptor
                )

            self.stack.append(a_visitor)
            self._publish_comment()
            if not a_visitor or a_visitor == EMPTY_ANNOV:
                self._copy_line()
        except StopIteration as err:
            self._throw_eol(err)

    def _handle_enum(self) -> None:
        """Handles .enum definitions in Annotations or SubAnnotations."""
        try:
            # As we need the annotation value's name, we have to
            # use the cleaned line buffer in the current line object.
            name = self.line.cleaned[:self.line.cleaned.find("=")].strip()

            token = next(self.line)
            self._validate_token(token, Token.ENUM)

            # UNSAFE
            descriptor, value = self.line.peek().split("->")
            self._validate_descriptor(descriptor)

            val_name, val_descriptor = value.split(":")
            self._validate_descriptor(val_descriptor)

            val_name = val_name.rstrip(">").lstrip("<")
            if self._visitor and self._visitor != EMPTY_ANNOV:
                self._visitor.visit_enum(name, descriptor, val_name, val_descriptor)
            else:
                self._copy_line()

        except StopIteration as err:
            self._throw_eol(err)

    def _handle_debug(self) -> None:
        # If validation is enabled, the '.super' token is verified
        token = next(self.line)
        self._validate_token(token, Token.DEBUG)

        enbaled = self.line.peek()
        if self._visitor:
            # Visit the class afterwards
            self._visitor.visit_super(int(enbaled))
        else:
            self._copy_line()
        self._publish_comment()

    ###########################################################################################
    # ANNOTATION VALUE IMPLEMENTATION
    ###########################################################################################

    def _handle_value(self) -> None:
        val_name = next(self.line)
        # Skip the assignment operator ('=')
        next(self.line)

        statement = self.line.peek()

        if statement[0] == ".":
            self._handle_token()

        # We either have a normal value or an array of values
        else:
            do_copy = not self._visitor or self._visitor == EMPTY_ANNOV
            cleaned = self.line.cleaned
            if do_copy:
                self._copy_line()

            if "{" in cleaned:
                if "}" in cleaned:
                    a_values = [
                        x.strip()
                        for x in cleaned[
                            cleaned.find("{") + 1 : cleaned.find("}")
                        ].split(",")
                    ]
                else:
                    # Read lines until '}' is at line's end, but publish
                    # an EOL comment before
                    self._publish_comment()
                    a_values = []
                    self._next_line()
                    while self.line.cleaned[-1] != "}" and self.line.cleaned[0] != "}":
                        value = self.line.peek().rstrip(",")

                        # Don't forget to publish a line comment
                        self._publish_comment()
                        a_values.append(value)
                        if do_copy:
                            self._copy_line()
                        self._next_line()

                # publish collected values
                if self._visitor and self._visitor != EMPTY_ANNOV:
                    self._visitor.visit_array(val_name, a_values)

            # Parse a simple value
            elif self._visitor and self._visitor != EMPTY_ANNOV:
                self._visitor.visit_value(val_name, self.line.peek())

    ###########################################################################################
    # METHOD SPECIFIC IMPLEMENTATION
    ###########################################################################################
    def _handle_parameter(self) -> None:
        # Simple workaround to handle #1
        self._handle_param()

    def _handle_param(self) -> None:
        if not self._visitor or self._visitor == EMPTY_METHV:
            self._copy_line()
            return

        # Skip '.param' or '.parameter' instruction
        next(self.line)

        register = next(self.line)
        if self.line.cleaned.find('"') != -1:
            name = self.line.peek().strip('"')
        else:
            name = ""
        self._visitor.visit_param(register, name)
        self._publish_comment()

    def _handle_method_int(self, token: Token, func) -> None:
        tk_val = next(self.line)
        self._validate_token(tk_val, token)

        number = self.line.peek()
        if func:
            func(int(number))
            self._publish_comment()
        else:
            self._copy_line()

    def _handle_line(self) -> None:
        self._handle_method_int(
            Token.LINE,
            self._visitor.visit_line
            if self._visitor not in (None, EMPTY_METHV)
            else None,
        )

    def _handle_registers(self) -> None:
        self._handle_method_int(
            Token.REGISTERS,
            self._visitor.visit_registers
            if self._visitor not in (None, EMPTY_METHV)
            else None,
        )

    def _handle_locals(self) -> None:
        self._handle_method_int(
            Token.LOCALS,
            self._visitor.visit_locals
            if self._visitor not in (None, EMPTY_METHV)
            else None,
        )

    def _handle_block(self) -> None:
        block_id = self.line.peek().lstrip(":")
        if self._visitor and self._visitor not in (None, EMPTY_METHV):
            self._visitor.visit_block(block_id)
            self._publish_comment()
        else:
            self._copy_line()

    def _handle_catch(self, is_catchall=False) -> None:
        """Handles simple .catch statements."""
        if not self._visitor or self._visitor == EMPTY_METHV:
            self._copy_line()
            return

        # 1. Handle the exception descriptor
        if not is_catchall:
            next(self.line)
            descriptor = self.line.peek()
        else:
            descriptor = "Ljava/lang/Exception;"
        self._validate_descriptor(descriptor)

        # 2. Collect try_start and try_end blocks
        cleaned = self.line.cleaned
        try_start, _, try_end = (
            cleaned[cleaned.find("{") + 1 : cleaned.find("}")].strip().split(" ")
        )
        catch_block = self.line.last()

        values = (try_start.lstrip(":"), try_end.lstrip(":"), catch_block.lstrip(":"))
        if is_catchall:
            self._visitor.visit_catchall(descriptor, values)
        else:
            self._visitor.visit_catch(descriptor, values)
        self._publish_comment()

    def _handle_instruction(self) -> None:
        """Dynamic method that handles instructions in methods.

        Most of Smali instructions are handled via 'visit_instruction' but there are
        a few exceptions:
            - Instructions starting with 'invoke',
            - Instructions starting with 'return' and
            - GOTO-Instructions
        :meta public:
        """
        if not self._visitor or self._visitor == EMPTY_METHV:
            self._copy_line()
            return

        instruction = next(self.line)
        sub_ins = (
            "" if "-" not in instruction else instruction[instruction.find("-") + 1 :]
        )
        if instruction.startswith("invoke"):
            # Invoke instructions will be handles separately as they have
            # as special structure
            cleaned = self.line.cleaned
            args = [
                x.strip()
                for x in cleaned[cleaned.find("{") + 1 : cleaned.find("}")].split(",")
            ]

            # Maybe replace this with a method call in Line
            method_sig = self.line.last()

            descriptor, signature = method_sig.split("->")
            self._validate_descriptor(descriptor)

            self._visitor.visit_invoke(sub_ins, args, descriptor, signature)
        elif instruction.startswith(RETURN):
            # Return statements are handled separately to make building
            # Smali files easier
            i_values = self._collect_values(",")
            self._visitor.visit_return(sub_ins, i_values)

        elif instruction == GOTO:
            # Goto instructions are handled directly
            block = self.line.peek().lstrip(":")
            self._visitor.visit_goto(block)
        else:
            i_values = self._collect_values(",")
            if self._visitor and self._visitor != EMPTY_METHV:
                self._visitor.visit_instruction(instruction, i_values)
        # Don't forget the EOL comment
        self._publish_comment()

    def _handle_packed_switch(self) -> None:
        do_copy = not self._visitor or self._visitor == EMPTY_METHV
        next(self.line)

        value = self.line.peek()
        if do_copy:
            self._copy_line()
        self._publish_comment()
        self._next_line()

        blocks = []
        while True:
            next_value = next(self.line)
            self._publish_comment()
            if do_copy:
                self._copy_line()
            if next_value[0] == ":":
                blocks.append(next_value.lstrip(":"))
            elif Token.END.value in next_value:
                # Use this method to prevent looping forever
                break
            self._next_line()

        if self._visitor and self._visitor != EMPTY_METHV:
            self._visitor.visit_packed_switch(value, blocks)

    def _handle_catchall(self) -> None:
        # same as .catch
        self._handle_catch(is_catchall=True)

    def _handle_array_data(self) -> None:
        do_copy = not self._visitor or self._visitor == EMPTY_METHV
        # We can't skip parsing because this operation takes more one
        # one line in the SourceCode
        next(self.line)

        # The number shouldn't be de-serialized as it could be a hexadezimal
        # number -> use SmaliValue(...) instead
        length = self.line.peek()
        values = []

        if do_copy:
            self._copy_line()
        self._publish_comment()
        while True:
            self._next_line()
            value = self.line.peek()
            self._publish_comment()
            if do_copy:
                self._copy_line()
            if value[0] == "." and value[1:] == Token.END.value:
                break
            values.append(smali_value(value))

        if self._visitor and self._visitor != EMPTY_METHV:
            self._visitor.visit_array_data(length, values)

    def _handle_local(self) -> None:
        """Handle debug information."""
        if not self._visitor or self._visitor == EMPTY_METHV:
            self._copy_line()
            return

        # Skip the instruction
        next(self.line)

        values = self._collect_values()
        if len(values) != 3 and self.validate:
            raise SyntaxError(
                f'Expected 3 values in ".local" statement - got {len(values)}'
            )

        register = values[0]
        name, descriptor = values[1].split(":")
        full_desc = values[2]
        self._validate_descriptor(descriptor)
        self._validate_descriptor(full_desc)

        self._visitor.visit_local(register, name.strip('"'), descriptor, full_desc)
        self._publish_comment()

    def _handle_sparse_switch(self) -> None:
        """Handles a more complicated switch statement."""
        do_copy = not self._visitor or self._visitor == EMPTY_METHV
        # We can't skip parsing because this operation takes more one
        # one line in the SourceCode
        next(self.line)

        values = {}
        if do_copy:
            self._copy_line()
        self._publish_comment()
        while True:
            self._next_line()
            key = self.line.peek()
            self._publish_comment()
            if do_copy:
                self._copy_line()
            if key[0] == "." and key[1:] == Token.END.value:
                break
            # Add the block id without leading ':'
            values[key] = self.line.last().lstrip(":")

        if self._visitor and self._visitor != EMPTY_METHV:
            self._visitor.visit_sparse_switch(values)
            self._publish_comment()

    def _handle_prologue(self) -> None:
        if self._visitor and self._visitor != EMPTY_METHV:
            self._visitor.visit_prologue()
            self._publish_comment()
        else:
            self._copy_line()

    def _handle_restart(self) -> None:
        if not self._visitor or self._visitor == EMPTY_METHV:
            self._copy_line()
            return

        register = self.line.last()
        self._visitor.visit_restart(register)
        self._publish_comment()
