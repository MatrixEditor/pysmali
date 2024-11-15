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


class VisitorBase:
    """Base class for Smali-Class visitor classes.

    :param delegate: A delegate visitor, defaults to None
    :type delegate: BaseVisitor subclass, optional
    """

    def __init__(self, delegate: "VisitorBase" = None) -> None:
        self.delegate = delegate
        # does not apply to muliple inheritance
        if delegate and not isinstance(delegate, self.__class__.__base__):
            raise TypeError(
                f"Invalid Visitor type - expected subclass of {self.__class__}"
            )

    def visit_comment(self, text: str) -> None:
        """Visits a comment string.

        Important: if you want to visit inline comments (EOL comments)
        use `#visit_eol_comment()` instead.

        :param text: the comment's text without the leading '#'
        :type text: str
        """
        if self.delegate:
            self.delegate.visit_comment(text)

    def visit_eol_comment(self, text: str) -> None:
        """Visits an inlined comment (EOL comment)

        :param text: the text without the leading '#'
        :type text: str
        """
        if self.delegate:
            self.delegate.visit_eol_comment(text)

    def visit_end(self) -> None:
        """Called at then end of an annotation."""
        if self.delegate:
            self.delegate.visit_end()


class AnnotationVisitor(VisitorBase):
    """Base class for annotation visitors."""

    def visit_value(self, name: str, value) -> None:
        """Visits a simple annotation value.

        :param name: the value's name
        :type name: str
        :param value: the value
        :type value: _type_
        """
        if self.delegate:
            self.delegate.visit_value(name, value)

    def visit_array(self, name: str, values: list) -> None:
        """Visits an array of values.

        :param name: the value name
        :type name: str
        :param values: the array's values
        :type values: list
        """
        if self.delegate:
            self.delegate.visit_array(name, values)

    def visit_subannotation(
        self, name: str, access_flags: int, signature: str
    ) -> "AnnotationVisitor":
        """Prepares to visit an internal annotation.

        :param name: the annotation value name
        :type name: str
        :param access_flags: the annotations access flags (zero on most cases)
        :type access_flags: int
        :param signature: the class signature
        :type signature: str
        """
        if self.delegate:
            return self.delegate.visit_subannotation(name, access_flags, signature)

    def visit_enum(self, name: str, owner: str, const: str, value_type: str) -> None:
        """Visits an enum value

        :param owner: the declaring class
        :type owner: str
        :param name: the annotation value name
        :type name: str
        :param const: the enum constant name
        :type const: str
        :param value_type: the value type
        :type value_type: str
        """
        if self.delegate:
            self.delegate.visit_enum(name, owner, const, value_type)


class MethodVisitor(VisitorBase):
    """Base class for method visitors."""

    def __init__(self, delegate: "MethodVisitor" = None) -> None:
        super().__init__(delegate)

    def visit_catch(self, exc_name: str, blocks: tuple) -> None:
        """Called on a ``.catch`` statement.

        The blocks contain the two enclosing goto blocks and the returning
        definition:

        .. code-block:: bnf

            .catch <name> { <try_start> .. <try_end> } <catch_handler>

        :param exc_name: the exception descriptor
        :type exc_name: str
        :param blocks: the goto-blocks definition
        :type blocks: tuple
        """
        if self.delegate:
            self.delegate.visit_catch(exc_name, blocks)

    def visit_catchall(self, exc_name: str, blocks: tuple) -> None:
        """Called on a ``.catchall`` statement.

        The blocks contain the two enclosing goto blocks and the returning
        definition:

        .. code-block:: bnf

            .catchall { <try_start> .. <try_end> } <catch_handler>

        :param exc_name: the exception descriptor
        :type exc_name: str
        :param blocks: the goto-blocks definition
        :type blocks: tuple
        """
        if self.delegate:
            self.delegate.visit_catchall(exc_name, blocks)

    def visit_param(self, register: str, name: str) -> None:
        """Called on a ``.param`` statement

        :param register: the register
        :type register: str
        :param name: the parameter's name
        :type name: str
        """
        if self.delegate:
            return self.delegate.visit_param(register, name)

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        """Prepares to visit an annotation.

        :param access_flags: the annotations access flags (zero on most cases)
        :type access_flags: int
        :param signature: the class signature
        :type signature: str
        """
        if self.delegate:
            return self.delegate.visit_annotation(access_flags, signature)

    def visit_locals(self, local_count: int) -> None:
        """Called on a ``.locals`` statement.

        The execution context of this method should be the same as of
        *visit_registers*.

        :param locals: the amount of local variables
        :type locals: int
        """
        if self.delegate:
            self.delegate.visit_locals(local_count)

    def visit_registers(self, registers: int) -> None:
        """Called on a '.registers' statement.

        The execution context of this method should be the same as of
        'visit_locals'.

        :param registers: the amount of local variables
        :type registers: int
        """
        if self.delegate:
            self.delegate.visit_registers(registers)

    def visit_line(self, number: int) -> None:
        """Called when a line definition is parsed.

        :param name: the line number
        :type name: str
        """
        if self.delegate:
            self.delegate.visit_line(number)

    def visit_block(self, name: str) -> None:
        """Called when a goto-block definition is parsed.

        :param name: the block's name
        :type name: str
        """
        if self.delegate:
            self.delegate.visit_block(name)

    def visit_invoke(self, inv_type: str, args: list, owner: str, method: str) -> None:
        """Handles an 'invoke-' statement.

        This method is called whenever an 'invoke-' statement hias been
        parsed. That includes 'invoke-virtual' as well as 'invoke-direct'.

        The provided metho string contains the method signature which can
        be passed into the Type constructor.

        :param inv_type: the invocation type (direct, virtual, ...)
        :type inv_type: str
        :param args: the argument list
        :type args: list
        :param owner: the owner class of the referenced method
        :type owner: str
        :param method: the method to call
        :type method: str
        """
        if self.delegate:
            self.delegate.visit_invoke(inv_type, args, owner, method)

    def visit_return(self, ret_type: str, args: list) -> None:
        """Handles 'return-' statements.

        :param ret_type: the return type, e.g. "object" or "void", ...
        :type ret_type: str
        :param args: the argument list
        :type args: list
        """
        if self.delegate:
            self.delegate.visit_return(ret_type, args)

    def visit_instruction(self, ins_name: str, args: list) -> None:
        """Visits common instructions with one or two parameters.

        :param ins_name: the instruction name
        :type ins_name: str
        :param args: the argument list
        :type args: list
        """
        if self.delegate:
            self.delegate.visit_instruction(ins_name, args)

    def visit_goto(self, block_name: str) -> None:
        """Visits 'goto' statements.

        :param block_name: the destination block name
        :type block_name: str
        """
        if self.delegate:
            self.delegate.visit_goto(block_name)

    def visit_packed_switch(self, value: str, blocks: list) -> None:
        """Handles the packed-switch statement.

        :param value: the value which will be "switched"
        :type value: str
        :param blocks: the block ids
        :type blocks: list[str]
        """
        if self.delegate:
            self.delegate.visit_packed_switch(value, blocks)

    def visit_array_data(self, length: str, value_list: list) -> None:
        """Called on an '.array-data' statement.

        :param length: the array's length
        :type length: str
        :param value_list: the array's values
        :type value_list: list
        """
        if self.delegate:
            self.delegate.visit_array_data(length, value_list)

    def visit_local(
        self, register: str, name: str, descriptor: str, full_descriptor: str
    ) -> None:
        """Handles debug information packed into .local statements.

        :param register: the variable register
        :type register: str
        :param name: the variable name
        :type name: str
        :param descriptor: the type descriptor
        :type descriptor: str
        :param full_descriptor: the java descriptor
        :type full_descriptor: str
        """
        if self.delegate:
            self.delegate.visit_local(register, name, descriptor, full_descriptor)

    def visit_sparse_switch(self, branches: dict) -> None:
        """Visits a .sparse-switch statement.

        The branches takes the original case value as their key
        and the block_id as their value.

        :param branches: the switch branches
        :type branches: dict
        """
        if self.delegate:
            self.delegate.visit_sparse_switch(branches)

    def visit_prologue(self) -> None:
        """Visits a .prologue statement.

        Note that this call comes without any arguments.
        """
        if self.delegate:
            self.delegate.visit_prologue()

    def visit_restart(self, register: str) -> None:
        """Visits a .restart statement.

        :param register: the register
        :type register: str
        """
        if self.delegate:
            self.delegate.visit_restart(register)


class FieldVisitor(VisitorBase):
    """Base class for field visitors."""

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        """Prepares to visit an annotation.

        :param access_flags: the annotations access flags (zero on most cases)
        :type access_flags: int
        :param signature: the class signature
        :type signature: str
        """
        if self.delegate:
            return self.delegate.visit_annotation(access_flags, signature)


class ClassVisitor(VisitorBase):
    """Base class for Smali class visitors."""

    def visit_class(self, name: str, access_flags: int) -> None:
        """Called when the class definition has been parsed.

        :param name: the class name (type descriptor, e.g. "Lcom/example/A;")
        :type name: str
        :param access_flags: different access flags (PUBLIC, FINAL, ...)
        :type access_flags: int
        """
        if self.delegate:
            self.delegate.visit_class(name, access_flags)

    def visit_super(self, super_class: str) -> None:
        """Called when a .super statement has been parsed.

        :param super_class: the super class name as type descriptor
        :type super_class: str
        """
        if self.delegate:
            self.delegate.visit_super(super_class)

    def visit_implements(self, interface: str) -> None:
        """Colled upon an implements directive.

        :param interface: the class name (internal name)
        :type interface: str
        """
        if self.delegate:
            self.delegate.visit_implements(interface)

    def visit_field(
        self, name: str, access_flags: int, field_type: str, value=None
    ) -> FieldVisitor:
        """Called when a global field definition has been parsed.

        :param name: the field's name
        :type name: str
        :param access_flags: the access flags like PUBLIC, FINAL, ...
        :type access_flags: str
        :param field_type: the field's type (can be primitive)
        :type field_type: str
        :param value: the field's   value
        :type value: _type_
        """
        if self.delegate:
            return self.delegate.visit_field(name, access_flags, field_type, value)

    def visit_method(
        self, name: str, access_flags: int, parameters: list, return_type: str
    ) -> MethodVisitor:
        """Called when a method definition has been parsed.

        :param name: the method's name
        :type name: str
        :param access_flags: the access flags (PUBLIC, PRIVATE, ...)
        :type access_flags: int
        :param parameters: the parameter list (internal names)
        :type parameters: list
        :param return_type: the return type (internal name)
        :type return_type: str
        :return: a MethodVisitor that handles method parsing events
        :rtype: MethodVisitor
        """
        if self.delegate:
            return self.delegate.visit_method(
                name, access_flags, parameters, return_type
            )

    def visit_inner_class(self, name: str, access_flags: int) -> "ClassVisitor":
        """Called when the class definition has been parsed.

        :param name: the class name (type descriptor, e.g. "Lcom/example/A;")
        :type name: str
        :param access_flags: different access flags (PUBLIC, FINAL, ...)
        :type access_flags: int
        """
        if self.delegate:
            return self.delegate.visit_inner_class(name, access_flags)

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        """Prepares to visit an annotation.

        :param access_flags: the annotations access flags (zero on most cases)
        :type access_flags: int
        :param signature: the class signature
        :type signature: str
        """
        if self.delegate:
            return self.delegate.visit_annotation(access_flags, signature)

    def visit_source(self, source: str) -> None:
        """Visits the source type of the smali file.

        :param source: the source type
        :type source: str
        """
        if self.delegate:
            self.delegate.visit_source(source)

    def visit_debug(self, enabled: int) -> None:
        """Visits a ``.debug`` directive.

        :param enabled: whether debugging symbols are enabled.
        :type enabled: int
        """
        if self.delegate:
            self.delegate.visit_debug(enabled)
