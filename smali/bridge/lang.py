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
The module ``lang`` of the provided Smali bridge defines classes that
can be used to mimic Java's reflection at runtime of the :class:`SmaliVM`.

All members of a Smali class inherit functionalities of ``__eq__``,
``__ne__``, as well as hash value calculation and string representation
of objects.

.. hint::

    Some properties are modifiable like ``SmaliField.value`` or the name
    of a :class:`SmaliClass` object. It is recommended to leave them how they
    are and let the VM make chenges to them.

"""

import re

from io import UnsupportedOperation

from smali.base import AccessType, SVMType
from smali.bridge.errors import NoSuchMethodError, NoSuchFieldError, NoSuchClassError

__all__ = [
    "SmaliMember",
    "SmaliAnnotation",
    "SmaliField",
    "SmaliMethod",
    "SmaliMethodBroker",
    "SmaliClass",
    "SmaliObject",
]


class SmaliMember:
    """Base class for Python classes of the Smali language.

    All members must provide a signature to be identified with.
    """

    __parent: "SmaliMember"
    """The parent of this member."""

    __signature: str
    """The qualified signature of this member"""

    __type: SVMType

    __modifiers: int
    """The member's visibility modifiers."""

    __annotations: dict
    """All annotations of this member. The will be stored in
    a type-2-object mapping.

    >>> member.annotations
    { 'Ljava/lang/Deprecated;': [<SmaliAnnotation at 0x...>, ...] }
    """

    def __init__(
        self,
        type_: str,
        parent: "SmaliMember",
        signature: str,
        modifiers: int,
        base_class: type,
        annotations: list = None,
    ) -> None:
        self.__type = SVMType(str(type_))
        self.__signature = signature
        self.__modifiers = modifiers
        self.__annotations = annotations or []
        if self.__class__ != base_class:
            raise TypeError(f"{base_class.__name__} cannot be sub-classed!")

        self.__parent = parent
        if not isinstance(self.parent, SmaliMember) and parent:
            raise TypeError("Parent of this memeber must be an instance of SmaliMember")

    def is_annotation_present(self, a_type: str) -> bool:
        """Returns whether the given annotation is present.

        :param a_type: the annotation's type descriptor
        :type a_type: str
        :return: True, if present; False otherwise
        :rtype: bool
        """
        if isinstance(a_type, SVMType):
            a_type = str(a_type)

        return isinstance(a_type, str) and a_type in self.__annotations

    def get_annotations(self, a_type: str) -> list:
        """Returns all declared annnotations of the given type.

        :param a_type: the annotation's type descriptor
        :type a_type: str | SVMType
        :return: a list of declared annotations
        :rtype: list
        """
        if isinstance(a_type, SVMType):
            a_type = str(a_type)

        if not isinstance(a_type, str):
            # to prevent errors, the output is non-null
            return []

        return self.__annotations.get(a_type, [])

    @property
    def parent(self) -> "SmaliMember":
        """Returns the declaring class or annotation member.

        :return: the parent of this member
        :rtype: SmaliMember
        """
        return self.__parent

    @property
    def signature(self) -> str:
        """The signature of this member

        :return: the id for this member
        :rtype: str
        """
        return self.__signature

    @property
    def modifiers(self) -> int:
        """The modifiers for this member

        :return: the modifiers
        :rtype: int
        """
        return self.__modifiers

    @property
    def annotations(self) -> list:
        """The declared annotations of this member

        :return: all declared annotations
        :rtype: list
        """
        return self.__annotations

    @property
    def type(self) -> SVMType:
        """Returns the type of this member

        :return: the type instance
        :rtype: :class:`SVMType`
        """
        return self.__type

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, self.__class__):
            return __o.signature == self.__signature
        return super().__eq__(__o)

    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)

    def __hash__(self) -> int:
        return hash(str(self.type))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.signature!r} at {id(self):#x}>"

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} {self.signature!r}>"


class SmaliAnnotation(SmaliMember):
    """Class that represents Smali annotations (and subannotations).

    This class mimics the behaviour of a ``dict`` object, so it can be
    used as follows:

    >>> annotation = SmaliAnnotation(...)
    >>> annotation['age'] = 30
    >>> age = annotation['age']
    30
    >>> 'age' in annotation
    True

    :param signature: the annotation's type descriptor
    :type signature: str
    :param modifiers: the annotation's visibility
    :type modifiers: int
    :param annotations: a list of declared annotations, defaults to None
    :type annotations: list, optional
    :param attr: the annotation's attributes, defaults to None
    :type attr: dict, optional
    """

    attr: dict
    """The attributes of this annotation (key-value map)."""

    def __init__(
        self,
        parent: SmaliMember,
        signature: str,
        modifiers: int,
        annotations: list = None,
        attr=None,
    ) -> None:
        super().__init__(
            signature, parent, signature, modifiers, SmaliAnnotation, annotations
        )
        self.attr = attr or {}

    def __getitem__(self, key: str) -> object:
        return self.attr.get(key, None)

    def __setitem__(self, key: str, value):
        self.attr[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.attr


class SmaliField(SmaliMember):
    """Python class that represents fields in Smali.

    :param signature: the field's signature (``name:type``)
    :type signature: str
    :param modifiers: the field's access modifiers
    :type modifiers: int
    :param annotations: the field's annotations, defaults to None
    :type annotations: list, optional
    :param value: the field's value, defaults to None
    :type value: int | float | str | SVMType | bool, optional
    """

    __name: str
    """The field's name"""

    __value: int | float | str | SVMType | bool
    """Stores the actual value of this field"""

    def __init__(
        self,
        _type: str,
        parent,
        signature: str,
        modifiers: int,
        name: str,
        annotations: list = None,
        value=None,
    ) -> None:
        super().__init__(_type, parent, signature, modifiers, SmaliField, annotations)
        self.__value = value
        self.__name = name

    @property
    def value(self) -> int | float | str | SVMType | bool:
        """Returns the value of this field.

        :return: the value as a :class:`SmaliValue`
        :rtype: int | float | str | SVMType | bool
        """
        return self.__value

    @value.setter
    def value(self, new_value: int | float | str | SVMType | bool):
        """Setter for ``self.value``.

        :param new_value: the new value to apply
        :type new_value: int | float | str | SVMType | bool
        :raises UnsupportedOperation: if this field can not be modified
        """
        self.__value = new_value

    @property
    def name(self) -> str:
        """Returns the name of this field

        :return: the name
        :rtype: str
        """
        return self.__name


class SmaliMethod(SmaliMember):
    """Implementation of a Smali method

    Instances of this class are callable with pre-defined
    arguments. For example, a method with the signature ``"add(II)I"``
    has two integet arguments and an integer as return value. A
    ``SmaliMethod`` can be executed as follows:

    .. code-block:: python

        # Our example method with signature := "add(II)I"
        method = SmaliMethod(...)
        instance = SmaliObject(...)
        result = method(instance, 1, 2)

    The instance of the object that defines the method is always
    needed except for static method. They can bbe called with
    ``None`` as the instance parameter.
    """

    __smali_params: list = []
    """The smali parameter types (:class:`SVMType`)"""

    __smali_return: SVMType
    """The return type"""

    __name: str
    """The method's name"""

    __vm = None
    """The VM that delegates the execution of this method."""

    __locals: int
    """Stores the amount of locals"""

    def __init__(
        self,
        vm,
        parent: "SmaliMember",
        signature: str,
        modifiers: int,
        annotations: list = None,
    ) -> None:
        super().__init__(
            f"{parent.type}->{signature}",
            parent,
            signature,
            modifiers,
            SmaliMethod,
            annotations,
        )
        self.__vm = vm
        sig_type = self.type.signature
        if not sig_type:
            raise ValueError(f"Expected a method signature - got {self.type}")
        self.name = sig_type.name
        self.smali_params = sig_type.parameter_types
        self.smali_return = sig_type.return_type

    def __call__(self, instance, *args, **kwds) -> object:
        if not self.__vm:
            raise UnsupportedOperation("VM not activated!")

        if self.modifiers in AccessType.ABSTRACT:
            raise UnsupportedOperation("Abstract methods cannot e executed!")

        # Argument validation will be done within the VM
        return self.__vm.call(self, instance, *args, **kwds)

    @property
    def name(self) -> str:
        """Returns the name of this method

        :return: the method's name
        :rtype: str
        """
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def parameters(self) -> list[SVMType]:
        """Returns the parameters of this method as type descriptor strings

        :return: the parameters of this method
        :rtype: list
        """
        return self.__smali_params

    @property
    def return_type(self) -> SVMType:
        """Returns the method's return type

        :return: the return type
        :rtype: SVMType
        """
        return self.__smali_return

    @property
    def locals(self) -> int:
        """Returns the amount of local variables."""
        return self.__locals

    @locals.setter
    def locals(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Invalid locals argument type")
        self.__locals = value


RE_REGISTER = re.compile(r"p\d+")


class _MethodBroker:
    """Custom implementation of an additional layer between class and method.

    This class is used to delegate method execution when multiple
    methods with the same name are present. It supports ``__call__`` to
    execute defined methods and ``__iadd__`` to add new methods. In order to
    iterate over defined methods, ``__iter__`` is implemented as well:

    >>> broker = SmaliMethodBroker(methods)
    >>> broker += SmaliMethod(...)
    >>> broker(object_instance, p0=1, p1=2)
    <result> # in case we defined a method with two parameters
    >>> for method in broker:
    ...     print(str(method))

    There is a pre-defined alias for this class named :class:`SmaliMethodBroker` in the .
    same module.
    """

    __name: str
    """The method's name"""

    __methods: list[SmaliMethod]
    """The methods that can be called."""

    def __init__(self, name: str, methods: list) -> None:
        self.__methods = methods or []
        self.__name = name

    def __iadd__(self, method: SmaliMethod) -> "_MethodBroker":
        self.__methods.append(method)
        return self

    def __call__(self, instance, *args, **kwds) -> object:
        if len(self.__methods) == 1:
            method = self.__methods[0]
            return method(instance, *args, **kwds)

        returns = kwds.get("returns", None)
        reg_count = 0
        for key in kwds:
            if RE_REGISTER.match(key):
                reg_count += 1

        # 1: If no register arguments are present via
        # **kwds, try to resolve with amount of parameters
        if len(kwds) == 0 or reg_count == 0:
            count = len(args)
            targets = list(filter(lambda x: len(x.parameters) == count, self.__methods))

            # We find the right method if only one result is present
            if len(targets) == 1:
                method = targets[0]
                return method(instance, *args, **kwds)

            else:
                if returns is None:
                    raise NoSuchMethodError(
                        f"Attempted to call {self.__name}() with invalid arguments"
                    )
                # Filter by return type
                if not returns:
                    targets = list(
                        filter(lambda x: (str(x.return_type) != "V"), targets)
                    )
                else:
                    targets = list(
                        filter(lambda x: (str(x.return_type) == "V"), targets)
                    )

                # We found one method, call it!
                if len(targets) == 1:
                    method = targets[0]
                    return method(instance, *args, **kwds)

        # 2. If registers are present, filter by amount
        # of defined parameters
        elif reg_count > 0:
            targets = list(
                filter(lambda x: len(x.parameters) == reg_count, self.__methods)
            )
            # Again, we find the right method if only one result is present
            if len(targets) == 1:
                method = targets[0]
                return method(instance, *args, **kwds)

        raise NoSuchMethodError(
            f"Attempted to call {self.__name}() - multiple variants present"
        )

    def __str__(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return f"<MethodBroker of {self.__name!r} at {id(self):#x}"

    def __iter__(self):
        return iter(self.__methods)

    def __getitem__(self, idx):
        return self.__methods[idx]


SmaliMethodBroker = _MethodBroker
"""Public alias for method broker objects"""


class SmaliClass(SmaliMember):
    """Internal class for storing imported class data.

    Annotations of a class
    ----------------------

    **All** declared annotations are stored within the ``annotations`` field
    and can be edited via the list type. it is also possible to check, wheter
    an anntation with a specific type descriptor is present. The present
    annotations can be retirievend via another method:

    >>> smali_class: SmaliClass = ...
    >>> smali_class.is_annotation_present("Lcom/dalvik/Signature;")
    True
    >>> for annotation in smali_class.get_annotations("Lcom/dalvik/Signature;")
    ...     # Dict behaviour is implemented here
    ...     annotation: SmaliAnnotation

    Fields of a class
    -----------------

    Field definitions are stored in a dict to enable quick access to all of
    them. Static fields contain values at class level and the values of normal
    fields will be stored in separate :class:`SmaliObject` instances. A field that
    belongs to a class should be retrieved via the following method:

    >>> field = smali_class.field("foo")
    <SmaliField 'foo:Ljava/lang/String;'>

    It is also possible to retrieve the :class:`SmaliField` via a dict-like access:

    >>> field = smali_class["foo"]

    .. important::

        Only fields are accessable via subcription, annotations, methods and
        implemented interfaces must e queried with other methods.

    Fields can be added via a dict-set operation:

    >>> smali_class["foo"] = SmaliField(...)

    Methods of a class
    ------------------

    Smali methods are mapped to their name and can be retrieved by either providing
    their name or signature directly:

    >>> method = smali_class.method("<init>")
    <SmaliMethod '<init> at ...>

    In this example we queried the method named ``<init>``, which is the constructor
    method of this class. If there is more than one definition, a so-called
    :class:`SmaliMethodBroker` is returned:

    >>> method = smali_class.method("getString")
    <_MethodBroker of 'getString' at ...>

    These objects store all methods with the same name and will choose the
    best method according to the given arguments when trying to execute one
    method.

    Like :class:`SmaliField` objects, methods can be added via dic-set as well:

    >>> smali_class["getString"] = SmaliMethod(...)

    Interfaces of a class
    ---------------------

    The implemented interfaces and super class will be stored as simple string
    objects. As the option ``lookup_missing`` can be set to false, these values
    won't be initialized with :class:`SmaliClass` instances to enable import of
    whole class files wihtout having all classes defined.

    Inner classes defined inside a SmaliClass
    -----------------------------------------

    Inner classes are stored like fields or methods - in a dict. They can't be
    queried directly, but the dictionary storing all classes is accessable:

    >>> smali_class["LMyInnerClass;"] = SmaliClass(...)
    """

    __simple_name: str
    """The simple name of this class"""

    __name: str
    """The full name of this class with dots (``.``)"""

    __methods: dict[str, _MethodBroker]
    """All methods that can be executed are stored in a separate dict.

    The values are instances of ``_Methodbroker``.
    """

    __fields: dict[str, SmaliField]
    """All fields if this class"""

    __classes: dict[str, SmaliClass]
    """All inner classes of this class"""

    __super: SVMType
    """The class descriptor of the super class"""

    __implements: list[SVMType]
    """The list of implemented interfaces."""

    def __init__(
        self,
        parent: "SmaliMember",
        signature: str,
        modifiers: int,
        annotations: list = None,
    ) -> None:
        super().__init__(
            signature, parent, signature, modifiers, SmaliClass, annotations
        )
        self.__name = self.type.pretty_name
        self.__simple_name = self.type.simple_name
        self.__fields = {}
        self.__methods = {}
        self.__super = None
        self.__implements = []
        self.__classes = {}

    @property
    def simple_name(self) -> str:
        """Returns the name of this class.

        :return: the class name
        :rtype: str
        """
        return self.__simple_name

    @property
    def name(self) -> str:
        """Returns the name of this class with the package (with dots)"""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Setter for the name property.

        :param value: the name of this class
        :type value: str
        """
        self.__name = value

    @property
    def inner_classes(self) -> dict[str, SmaliClass]:
        """Returns all inner classes

        :return: all defined inner classes
        :rtype: dict
        """
        return self.__classes

    @property
    def super_cls(self) -> SVMType:
        """Returns the super class of this class

        :return: the super class name
        :rtype: SVMType | SmaliClass
        """
        return self.__super

    @super_cls.setter
    def super_cls(self, value):
        """Setter for the super-class name

        :param value: the new name
        :type value: str
        """
        self.__super = value

    @property
    def interfaces(self) -> list[SVMType]:
        """Returns all implemented interfaces (type descriptors)

        :return: all implemented interfacea in a list
        :rtype: list
        """
        return self.__implements

    def get_declared_methods(self, access_type: AccessType = None) -> list[SmaliMethod]:
        """Returns all declared methods in this class,

        :param access_type: an extra filter, defaults to None
        :type access_type: AccessType, optional
        :return: the list of defined smali methods
        :rtype: list[SmaliMethod]
        """
        result = []
        for name in self.__methods:
            for method in self.__methods[name]:
                if access_type is None or method.modifiers in access_type:
                    result.append(method)

        return result

    def method(self, signature: str) -> SmaliMethod:
        """Searches for the given method signature or name.

        :param signature: the name or signature of the method
        :type signature: str
        :raises NoSuchMethodError: if no method with a name or wignature
                                   equal to the given could be found
        :return: the method or method-broker if multiple methods with the
                 same name exist.
        :rtype: SmaliMethod | SmaliMethodBroker
        """
        for name, broker in self.__methods.items():
            if name == signature:
                return broker

            for method in broker:
                if method.signature == signature:
                    return method

        raise NoSuchMethodError(f'Method with signature {signature!r} not found')

    def field(self, name: str) -> SmaliField:
        """Returns the field with the given name.

        :param name: the field's name
        :type name: str
        :raises NoSuchFieldError: if no field with the goven name is defined
        :return: the :class:`SmaliField` instance
        :rtype: SmaliField
        """
        if name in self.__fields:
            return self.__fields[name]

        raise NoSuchFieldError(f"Field with name {name!r} not found")

    def inner_class(self, name: str) -> "SmaliClass":
        """Returns an inner class by its name.

        :param name: the name (type descrptor)
        :type name: str
        :raises NoSuchClassError: if no inner class with the given name is defined
        :return: the :class:`SmaliClass` instance of the inner class
        :rtype: SmaliClass
        """
        if name not in self.__classes:
            raise NoSuchClassError(f'Class with name "{name}" not found!')

        return self.__classes[name]

    def __setitem__(self, key: str, value) -> None:
        if not key or not isinstance(key, str):
            raise KeyError("Invalid key")

        if isinstance(value, SmaliMethod):
            if key not in self.__methods:
                self.__methods[key] = SmaliMethodBroker(key, [value])
            else:
                self.__methods[key] += value

        elif isinstance(value, SmaliField):
            self.__fields[key] = value

        elif isinstance(value, SmaliClass):
            self.__classes[key] = value

    def __getitem__(self, key: str) -> SmaliField:
        if not key or not isinstance(key, str):
            raise KeyError("Invalid Key")

        return self.field(key)

    def __contains__(self, field_name: str) -> bool:
        return field_name in self.__fields

    def fields(self, access_type: AccessType = None):
        """Returns all fields that match the given access type.

        If no access type is given, all fields will be returned.

        :param access_type: the access type to filter, defaults to None
        :type access_type: AccessType, optional
        """

        def field_filter(field: SmaliField):
            if not access_type:
                return True
            return field.modifiers in access_type

        return filter(field_filter, self.__fields)

    def clinit(self) -> None:
        """Calls the static-block initializer method (``<clinit>``)

        If no static-block is defined, this method won't have any
        further action to take.
        """
        try:
            method = self.method("<clinit>")
        except NoSuchMethodError:
            # If no static initializer block is defined,
            # we should skip the execution
            return

        # The first argument represents an instance of the
        # current class - for static context it is always null
        method(None)

    def is_assignable(self, other: "SmaliClass") -> bool:
        if not other or not other.super_cls:
            return False

        super_class = other.super_cls
        while super_class and super_class != "Ljava/lang/Object;":
            if super_class == self or super_class == self.super_cls:
                return True

        return False


class SmaliObject:
    """Python objects that store data of a Smali object.

    This class implements dict-like access to all fields' values and
    static fields will be directly references if possible.

    .. caution::

        Smali objects of interfaces or abstract classes can't be created.
    """

    __field_values: dict
    """The object's field values.

    :meta public:
    """

    __class: SmaliClass
    """The prototype class.

    :meta public:
    """

    def __init__(self, clazz: SmaliClass) -> None:
        self.__class = clazz
        if clazz.modifiers in (AccessType.ABSTRACT, AccessType.INTERFACE):
            raise UnsupportedOperation(
                "Class is abstract and cannot be instantiated directly!"
            )

        self.__field_values = {}
        for name in clazz.fields():
            field = clazz.field(name)
            if field.modifiers not in AccessType.STATIC:
                self.__field_values[field.name] = None

    def init(self, *args):
        """Calls the constructor of this object."""
        ctor = self.smali_class.method("<init>")
        ctor(self, *args)

    @property
    def smali_class(self) -> SmaliClass:
        """Returns the prototype SmaliClass object

        :return: the smali class this object is an instance of
        :rtype: SmaliClass
        """
        return self.__class

    def __getitem__(self, name: str):
        field = self.smali_class.field(name)
        if field.modifiers in AccessType.STATIC:
            return field.value

        if name not in self.__field_values:
            raise NoSuchFieldError(f"Field not found: {name}")

        return self.__field_values[name]

    def __setitem__(self, name: str, value):
        field = self.smali_class.field(name)
        if field.modifiers in AccessType.FINAL:
            raise UnsupportedOperation(
                f'Attempt to write in read-only field "{self.smali_class.name}{name}"'
            )

        if field.modifiers in AccessType.STATIC:
            field.value = value

        # Rather don't use a check whether the field is present
        # as new members could be defined at runtime
        self.__field_values[name] = value

    def __contains__(self, name: str):
        return name in self.smali_class

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        """Objects will be represented in the following form:

        >>> repr(smali_object)
        <SmaliObject@$id(smali_object)$>

        :return: _description_
        :rtype: str
        :meta public:
        """
        return f"<SmaliObject@{id(self):x}>"

    def __str__(self) -> str:
        return f"<SmaliObject@{id(self):x} fields={len(self.__field_values)} type={self.smali_class!r}"
