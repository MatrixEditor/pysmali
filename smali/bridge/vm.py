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
from __future__ import annotations

__doc__ = """
Implementation of a simple Smali emulator named *SmaliVM*. It supports
execution of small code snippets as well as the execution of whole
class files.

Debugging can be done by providing a :class:`DebugHandler` and enabling the
debug-option wihtin the VM object. It is also possible to use a custom
``ClassLoader`` to load or define new classes.
"""

from io import IOBase
from abc import ABCMeta, abstractmethod

from smali import SmaliValue, opcode
from smali.base import AccessType, SVMType
from smali.reader import SmaliReader
from smali.visitor import ClassVisitor, MethodVisitor, FieldVisitor, AnnotationVisitor
from smali.bridge.lang import (
    SmaliClass,
    SmaliMethod,
    SmaliField,
    SmaliAnnotation,
    RE_REGISTER,
)
from smali.bridge.frame import Frame
from smali.bridge.errors import (
    ExecutionError,
    NoSuchMethodError,
    InvalidOpcodeError,
    NoSuchClassError,
)
from smali.bridge import executor

__all__ = [
    "ClassLoader",
    "DebugHandler",
    "SmaliVM",
    "SmaliVMAnnotationReader",
    "SmaliVMFieldReader",
    "SmaliVMMethodReader",
    "SmaliVMClassReader",
    "SmaliClassLoader",
]


class ClassLoader(metaclass=ABCMeta):
    """Abstract base class for SmaliClassLoader"""

    @abstractmethod
    def define_class(self, source: bytes | str | IOBase) -> SmaliClass:
        """Defines a new SmaliClass by parsing the given source file.

        :param source: the source code
        :type source: bytes | str
        :return: the parsed class definition
        :rtype: SmaliClass
        """

    @abstractmethod
    def load_class(self, source: str | bytes | IOBase, init=True, lookup_missing=False) -> SmaliClass:
        """Parses the given source code and initializes the given class if enabled.

        :param source: the source code
        :type source: str | bytes | IOBase
        :param init: whether ``<clinit>`` should be executed, defaults to True
        :type init: bool, optional
        :param lookup_missing: whether missing classes should be searched before parsing
                               can continue, defaults to False
        :type lookup_missing: bool, optional
        :raises NoSuchClassError: if the given class is not defined and ``lookup_missing`` is true
        :raises InvalidOpcodeError: if the parsed opcode is invalid
        :return: the parsed class definition
        :rtype: SmaliClass
        """


class DebugHandler:
    """Basic adapter class used for debugging purposes"""

    def precall(
        self, vm: "SmaliVM", method: SmaliMethod, opc: executor.Executor
    ) -> None:
        """Called before an opcode executor is processed"""

    def postcall(
        self, vm: "SmaliVM", method: SmaliMethod, opc: executor.Executor
    ) -> None:
        """Called after the opcode has been executed"""


class SmaliVM:
    """Basic implementation of a Smali emulator in Python."""

    classloader: ClassLoader
    """The class loader used to define classes."""

    debug_handler: DebugHandler
    """The debug handler to use."""

    executors: dict[str, executor.Executor]
    """External executors used to operate on a single opcode."""

    use_strict: bool = False
    """Tells the VM to throw exceptions on unkown opcodes."""

    __classes: dict[str, SmaliClass] = {}
    """All classes are stored in a dict

    :meta public:
    """

    __frames: dict[int, Frame] = {}
    """Stores all execution frames mapped to their method object

    :meta public:
    """

    # This map is used to determine which parameters are applied to the right
    # values.
    __type_map: dict = {
        int: (
            "B",
            "S",
            "I",
            "J",
            "Ljava/lang/Byte;",
            "Ljava/lang/Short;",
            "Ljava/lang/Integer;",
            "Ljava/lang/Long;",
        ),
        float: ("F", "D", "Ljava/lang/Double;", "Ljava/lang/Float;"),
        str: ("Ljava/lang/String;", "C", "Ljava/lang/Character;"),
        bool: ("Z", "Ljava/lang/Boolean;"),
    }

    def __init__(
        self,
        class_loader: ClassLoader = None,
        executors: dict = None,
        use_strict: bool = False,
    ) -> None:
        self.classloader = _SmaliClassLoader(self) or class_loader
        self.executors = executors or executor.cache
        self.use_strict = use_strict
        self.debug_handler = None

    def new_class(self, __class: SmaliClass):
        """Defines a new class that can be accessed globally.

        :param cls: the class to be defined
        :type cls: SmaliClass
        """
        if not __class:
            raise ValueError("SmaliClass object is null!")

        self.__classes[__class.signature] = __class

    def new_frame(self, method: SmaliMethod, frame: Frame):
        """Creates a new method frame that will be mapped to the method's signature-

        :param method: the target method
        :type method: SmaliMethod
        :param frame: the execution frame
        :type frame: Frame
        """
        mhash = hash(method)
        if mhash not in self.__frames:
            self.__frames[mhash] = frame
            frame.vm = self


    def get_class(self, name: str) -> SmaliClass:
        """Searches for a class with the given name.

        :param name: the class name
        :type name: str
        :raises NoSuchClassError: if no class with the given name is defined
        :return: the defined Smali class
        :rtype: SmaliClass
        """
        if name not in self.__classes:
            raise NoSuchClassError(f'Class "{name}" not defined!')

        return self.__classes[name]

    def call(self, method: SmaliMethod, instance, *args, **kwargs) -> object:
        """Executes the given method in the given object instance.

        Before the method will be executed, there is an input parameter
        check to validate all passed arguments. The required registers
        will be filled automatically.

        Debugging is done via the :class:`DebugHandler` that must be set globally
        in this object.

        :param method: the method to execute
        :type method: :class:`SmaliMethod`
        :param instance: the smali object
        :type instance: :class:`SmaliObject`
        :raises NoSuchMethodError: if no frame is registered to the given method
        :raises ExecutionError: if an error occurs while execution
        :return: the return value of the executed method
        :rtype: object
        """
        mhash = hash(method)
        if mhash not in self.__frames:
            raise NoSuchMethodError(f"Method not registered! {method}")

        frame: Frame = self.__frames[mhash]
        frame.reset()
        for i in range(method.locals):
            frame.registers[f"v{i}"] = None

        if method.modifiers not in AccessType.STATIC:
            if not instance:
                raise ExecutionError(
                    "NullPtrError",
                    f"Expected instance of '{instance.smali_class.name}'",
                )
            frame.registers["p0"] = instance

        prev_frame = kwargs.pop("vm__frame", None)
        if prev_frame:
            frame.parent = prev_frame

        # validate method and set parameter values
        self._validate_call(method, frame, args, kwargs)
        while not frame.finished:
            opcode_exec, args = frame.opcodes[frame.pos]
            opcode_exec.args = args
            if self.debug_handler:
                self.debug_handler.precall(self, method, opcode_exec)

            opcode_exec(frame)
            opcode_exec.args = None
            frame.pos += 1
            if self.debug_handler:
                self.debug_handler.postcall(self, method, opcode_exec)

        if frame.error:
            if isinstance(frame.error, ExecutionError):
                raise frame.error

            raise ExecutionError(frame.error)

        value = frame.return_value
        frame.reset()
        return value

    def _validate_call(self, method: SmaliMethod, frame: Frame, args: tuple, kwargs: dict):
        parameters = method.parameters

        registers = {}
        for key, value in kwargs.items():
            if RE_REGISTER.match(key):
                registers[key] = value

        start = 1 if method.modifiers not in AccessType.STATIC else 0
        for i, value in enumerate(args, start=start):
            registers[f"p{i}"] = value

        if len(parameters) != len(registers):
            raise ValueError(
                "Invalid argument count! - expected %s, got %d"
                % (len(parameters), len(registers))
            )

        for param, register in zip(parameters, registers):
            param_type: SVMType = param
            # Lookup primitive types
            for primitive, ptypes in self.__type_map.items():
                if param_type.full_name in ptypes:
                    if not isinstance(registers[register], primitive):
                        raise TypeError(
                            "Invalid type for parameter, expected %s - got %s"
                            % (param, type(registers[register]))
                        )

            if param_type.full_name not in self.__classes:
                raise NoSuchClassError(f'Class "{param_type}" not defined!')

        frame.registers.update(registers)


####################################################################################################
# INTERNAL
####################################################################################################


class _SourceAnnotationVisitor(AnnotationVisitor):
    annotation: SmaliAnnotation
    """The final annotation"""

    def __init__(self, annotation: SmaliAnnotation) -> None:
        super().__init__(None)
        self.annotation = annotation

    def visit_value(self, name: str, value) -> None:
        self.annotation[name] = SmaliValue(value)

    def visit_array(self, name: str, values: list) -> None:
        self.annotation[name] = [SmaliValue(x) for x in values]

    def visit_enum(self, name: str, owner: str, const: str, value_type: str) -> None:
        # TODO: handle enum values
        return super().visit_enum(name, owner, const, value_type)

    def visit_subannotation(
        self, name: str, access_flags: int, signature: str
    ) -> "AnnotationVisitor":
        sub = SmaliAnnotation(self.annotation, signature, access_flags)
        self.annotation[name] = sub
        return SmaliVMAnnotationReader(sub)


class _SourceFieldVisitor(FieldVisitor):
    field: SmaliField

    def __init__(self, field: SmaliField) -> None:
        super().__init__()
        self.field = field

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        annotation = SmaliAnnotation(self.field, signature, access_flags)
        self.field.annotations.append(annotation)
        return SmaliVMAnnotationReader(annotation)


class _SourceMethodVisitor(MethodVisitor):
    method: SmaliMethod
    frame: Frame

    def __init__(self, method: SmaliMethod) -> None:
        super().__init__()
        self.method = method
        self.frame = Frame()
        self.pos = 0
        self._last_label = None

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        annotation = SmaliAnnotation(self.method, signature, access_flags)
        self.method.annotations.append(annotation)
        return SmaliVMAnnotationReader(annotation)

    def visit_block(self, name: str) -> None:
        self.frame.labels[name] = self.pos
        self.pos += 1
        self._last_label = name

    def visit_locals(self, local_count: int) -> None:
        self.method.locals = local_count

    def visit_registers(self, registers: int) -> None:
        self.method.locals = registers - len(self.method.parameters)

    def visit_catch(self, exc_name: str, blocks: tuple) -> None:
        start, _, handler = blocks
        self.frame.catch[start] = (exc_name, handler)

    def visit_catchall(self, exc_name: str, blocks: tuple) -> None:
        self.visit_catch(exc_name, blocks)

    def visit_goto(self, block_name: str) -> None:
        self.frame.opcodes.append((executor.goto, block_name))
        self.pos += 1

    def visit_array_data(self, length: str, value_list: list) -> None:
        self.frame.array_data[self._last_label] = value_list

    def visit_invoke(self, inv_type: str, args: list, owner: str, method: str) -> None:
        self.frame.opcodes.append((executor.invoke, (inv_type, args, owner, method)))
        self.pos += 1

    def visit_return(self, ret_type: str, args: list) -> None:
        if ret_type:
            self.visit_instruction(f"return-{ret_type}", args)
        else:
            self.visit_instruction("return", args)

    def visit_instruction(self, ins_name: str, args: list) -> None:
        cache: dict = self.frame.vm.executors
        for _, value in opcode.__dict__.items():
            # If the value of an attribute is equal to the given instruction
            # name,
            if value == ins_name:
                # Check if the instruction name is not in the list of executors
                # in the current frame's virtual machine
                if ins_name not in cache and not self.frame.vm.use_strict:
                    if "*" in cache:
                        func = cache["*"]
                    else:
                        # If not, add a tuple of the "nop" opcode function and the
                        # instruction arguments to the frame's opcodes list.
                        func = cache["nop"] if "nop" in cache else executor.nop
                    self.frame.opcodes.append((func, args))
                else:
                    # If yes, add a tuple of the executor function for the instruction
                    # name and the instruction arguments to the frame's opcodes list.
                    self.frame.opcodes.append((self.frame.vm.executors[ins_name], args))
                self.pos += 1
                return

        raise InvalidOpcodeError(f"Invalid OpCode: {ins_name}")

    def visit_packed_switch(self, value: str, blocks: list) -> None:
        self.frame.switch_data[self._last_label] = (value, blocks)

    def visit_sparse_switch(self, branches: dict) -> None:
        self.frame.switch_data[self._last_label] = branches


class _SourceClassVisitor(ClassVisitor):
    smali_class: SmaliClass
    """The result class object"""

    vm: SmaliVM
    """The vm used wihtin method visitor objects"""

    def __init__(self, vm: SmaliVM, smali_class: SmaliClass = None) -> None:
        super().__init__()
        self.vm = vm
        self.smali_class = smali_class

    def visit_annotation(self, access_flags: int, signature: str) -> AnnotationVisitor:
        annotation = SmaliAnnotation(self.smali_class, signature, access_flags)
        self.smali_class.annotations.append(annotation)
        return SmaliVMAnnotationReader(annotation)

    def visit_class(self, name: str, access_flags: int) -> None:
        self.smali_class = SmaliClass(None, name, access_flags)

    def visit_inner_class(self, name: str, access_flags: int) -> "ClassVisitor":
        inner = SmaliClass(self.smali_class, name, access_flags)
        self.smali_class[name] = inner
        return SmaliVMClassReader(self.vm, inner)

    def visit_field(
        self, name: str, access_flags: int, field_type: str, value=None
    ) -> FieldVisitor:
        field = SmaliField(
            field_type,
            self.smali_class,
            f"{name}:{field_type}",
            access_flags,
            name,
            value=SmaliValue(value) if value else None,
        )
        self.smali_class[name] = field
        return SmaliVMFieldReader(field)

    def visit_method(
        self, name: str, access_flags: int, parameters: list, return_type: str
    ) -> MethodVisitor:
        signature = f"{name}({''.join(parameters)}){return_type}"
        method = SmaliMethod(self.vm, self.smali_class, signature, access_flags)
        visitor = SmaliVMMethodReader(method)
        self.vm.new_frame(method, visitor.frame)
        self.smali_class[name] = method
        return visitor

    def visit_implements(self, interface: str) -> None:
        self.smali_class.interfaces.append(SVMType(interface))

    def visit_super(self, super_class: str) -> None:
        self.smali_class.super_cls = SVMType(super_class)


class _SmaliClassLoader(ClassLoader):
    vm: SmaliVM
    """The vm storing all defined classes."""

    def __init__(self, vm: SmaliVM) -> None:
        self.vm = vm

    def define_class(self, source: bytes) -> SmaliClass:
        reader = SmaliReader(validate=True, comments=False)

        visitor = SmaliVMClassReader(self.vm)
        reader.visit(source, visitor)
        smali_class = visitor.smali_class
        if not smali_class:
            raise ValueError("Could not parse class!")

        self.vm.new_class(smali_class)
        return smali_class

    def load_class(self, source: str, init=True, lookup_missing=False) -> SmaliClass:
        smali_class = self.define_class(source)
        if init:
            smali_class.clinit()
        return smali_class


####################################################################################################
# EXTERNAL
####################################################################################################
SmaliVMAnnotationReader = _SourceAnnotationVisitor
SmaliVMFieldReader = _SourceFieldVisitor
SmaliVMMethodReader = _SourceMethodVisitor
SmaliVMClassReader = _SourceClassVisitor
SmaliClassLoader = _SmaliClassLoader
