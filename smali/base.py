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
Basic component classes when working with the Smali language.
"""

import re

from enum import Enum, IntFlag

__all__ = [
    "AccessType",
    "Token",
    "Line",
    "smali_value",
    "is_type_descriptor",
    "Signature",
    "SVMType",
]


class AccessType(IntFlag):
    """Contains all access modifiers for classes, fields, methods and annotations.

    There is also a possibility to use values of this class with an ``in``
    statement:

    >>> flags = AccessType.PUBLIC + AccessType.FINAL
    >>> flags in AccessType.PUBLIC
    True
    >>> flags in AccessType.PRIVATE
    False
    """

    # !! IMPORTANT: Although, all access types from here (https://source.android.com/docs/core/runtime/dex-format#access-flags)
    # are covered, their values differ as there are multiple access flags with the same value.
    # REVISIT: Maybe convert this class into a dictionary
    PUBLIC = 0x1
    PRIVATE = 0x2
    PROTECTED = 0x4
    STATIC = 0x8
    FINAL = 0x10
    SYNCHRONIZED = 0x20
    VOLATILE = 0x40
    BRIDGE = 0x80
    TRANSIENT = 0x100
    VARARGS = 0x200
    NATIVE = 0x400
    INTERFACE = 0x800
    ABSTRACT = 0x1000
    STRICTFP = 0x2000
    SYNTHETIC = 0x4000
    ANNOTATION = 0x8000
    ENUM = 0x10000
    CONSTRUCTOR = 0x20000
    DECLARED_SYNCHRONIZED = 0x40000
    SYSTEM = 0x80000
    RUNTIME = 0x100000
    BUILD = 0x200000

    @staticmethod
    def get_flags(values: list) -> int:
        """Converts the given readable access modifiers into an integer.

        :param values: the keyword list
        :type values: list
        :return: an integer storing all modifiers
        :rtype: int
        """
        result = 0
        for element in values:
            if not element:
                continue

            element = str(element).lower()
            for val in AccessType:
                if val.name.lower().replace("_", "-") == element:
                    result |= val.value
        return result

    @staticmethod
    def get_names(flags: int) -> list:
        """Converts the given access modifiers to a human readable representation.

        :param flags: the access modifiers
        :type flags: int
        :return: a list of keywords
        :rtype: list
        """
        result = []
        for val in AccessType:
            if flags in val:
                result.append(val.name.lower().replace("_", "-"))
        return result

    @staticmethod
    def find(value: str) -> bool:
        """Returns whether the given keyword is a valid modifier.

        :param value: the value to check
        :type value: str
        :return: True, if the given value represents an access modifier
        :rtype: bool
        """
        for val in AccessType:
            name = val.name.lower().replace("_", "-")
            if name == value:
                return True
        return False

    def __contains__(self, other: int) -> bool:
        if isinstance(other, self.__class__):
            return super().__contains__(other)
        if isinstance(other, int):
            return self.value & other != 0
        raise TypeError(f"Unsupported type: {type(other)}")


class Token(Enum):
    """Defines all common token in a Smali file.

    There are some special methods implemented to use constants of this
    class in the following situations:

    >>> "annotation" == Token.ANNOTATION
    True
    >>> "local" != Token.LOCALS
    True
    >>> len(Token.ENUM)
    4
    >>> str(Token.ARRAYDATA)
    'array-data'
    """

    ANNOTATION = "annotation"
    ARRAYDATA = "array-data"
    CATCH = "catch"
    CATCHALL = "catchall"
    CLASS = "class"
    END = "end"
    ENUM = "enum"
    FIELD = "field"
    IMPLEMENTS = "implements"
    LINE = "line"
    LOCAL = "local"
    LOCALS = "locals"
    METHOD = "method"
    PACKEDSWITCH = "packed-switch"
    PARAM = "param"
    PROLOGUE = "prologue"
    REGISTERS = "registers"
    RESTART = "restart"
    SOURCE = "source"
    SPARSESWITCH = "sparse-switch"
    SUBANNOTATION = "subannotation"
    SUPER = "super"
    DEBUG = "debug"

    def __eq__(self, other: str) -> bool:
        if isinstance(other, self.__class__):
            return super().__eq__(other)
        return self.value == other

    def __ne__(self, other: str) -> bool:
        if isinstance(other, self.__class__):
            return super().__ne__(other)
        return self.value != other

    def __len__(self) -> int:
        return len(str(self.value))

    def __str__(self) -> str:
        return self.value


class Line:
    """Simple peekable Iterator implementation."""

    RE_EOL_COMMENT = re.compile(r"\s*#.*$")
    """Pattern for EOL (end of line) comments"""

    _default = object()
    """The default object which is returned to indicate the
    end of the current line has been reached."""

    raw: str
    """The raw line as it was passed through the constructor."""

    cleaned: str
    """The cleaned line without any leading and trailing whitespace"""

    eol_comment: str
    """The removed trailing EOL comment (if present)"""

    def __init__(self, line: str) -> None:
        if isinstance(line, (bytearray, bytes)):
            line = line.decode()

        self._it = None
        self._head = self._default
        self._elements = []
        self.reset(line)

    def _get_next(self) -> str:
        try:
            return next(self._it)
        except StopIteration:
            return self._default

    def __next__(self) -> str:
        value = self._head
        if value == self._default:
            raise StopIteration()

        self._head = self._get_next()
        return value

    def reset(self, line: str = None) -> None:
        """Resets this line and/or initialized it with the new value.

        :param line: the next line, defaults to None
        :type line: str, optional
        """
        if not line:
            self._head = self._default
            self._it = None
            return

        self.eol_comment = None
        self.raw = line.rstrip()
        self.cleaned = self.raw.lstrip()
        eol_match = Line.RE_EOL_COMMENT.search(self.cleaned)
        if eol_match is not None:
            start, end = eol_match.span()
            if self.cleaned.count('"', 0, start) % 2 == 0:
                # Remove the EOL comment and save it in a variable. Note
                # that the visitor will be notified when StopIteration is
                # raised.
                self.eol_comment = eol_match.group(0).lstrip("# ")
                self.cleaned = self.cleaned[:start] + self.cleaned[end:]

        self._elements = Line.split_line(self.cleaned)
        self._it = iter(self._elements)
        self._head = self._get_next()

    def peek(self, default: str = _default) -> str:
        """Returns the current element if this line.

        This method won't move forwards.

        :param default: the default value to return, defaults to _default
        :type default: str, optional
        :raises StopIteration: if the end of this line has been reached
        :return: the current value
        :rtype: str
        """
        if self._head == self._default:
            if default != self._default:
                return default
            raise StopIteration()
        return self._head

    def last(self) -> str:
        """Returns the last element of this line without modifying the iterator.

        :return: the last element
        :rtype: str
        """
        return self._elements[-1]

    def has_eol(self) -> bool:
        """Returns whether this line contains an EOL comment

        :return: True, if the line contains an EOL comment
        :rtype: bool
        """
        return self.eol_comment is not None

    def __bool__(self) -> bool:
        return self._head != self._default

    def has_next(self) -> bool:
        """Returns whether there as a following element.

        :return: True if next() can be called safely
        :rtype: bool
        """
        return self.__bool__()

    def __len__(self) -> int:
        return len(self.cleaned)

    @staticmethod
    def split_line(cleaned: str, sep: str = " ") -> list:
        """Splits the line by the given delimiter and ignores values in strings

        :param cleaned: the input string
        :type cleaned: str
        :param sep: the delimiter, defaults to ' '
        :type sep: str, optional
        :return: the splitted values
        :rtype: list
        """
        end = cleaned.find(sep)
        start = 0
        in_literal = False
        elements = []

        while end != -1:
            if end - 1 > 0 and cleaned[end - 1] == '"' and in_literal:
                in_literal = False
                elements.append(cleaned[start:end])
                start = end + 1

            elif cleaned[start] == '"':
                in_literal = True

            elif not in_literal:
                elements.append(cleaned[start:end])
                start = end + 1

            end = cleaned.find(sep, end + 1)
        elements.append(cleaned[start:])
        return elements


class Signature:
    """Internal class to encapsulate method signatures."""

    CLINIT = "<clinit>"
    """Static block initializer"""

    INIT = "<init>"
    """Constructor method"""

    def __init__(self, __signature: str | SVMType) -> None:
        self.__signature = str(__signature)
        self.__params = None
        self.__return_type = None
        self.__name = None

    @property
    def sig(self) -> str:
        """Returns the fully qualified signature string.

        >>> s = Signature("<init>(II)V")
        >>> s.sig
        '<init>(II)V'

        :return: the input string
        :rtype: str
        """
        return self.__signature

    @property
    def name(self) -> str:
        """Returns the method name

        >>> s = Signature("Lcom/example/Class;->getLength(Ljava/lang/String;)I")
        >>> s.name
        'getLength'

        :return: the absolute method name
        :rtype: str
        """
        if self.__name:
            return self.__name

        idx = self.__signature.find("(")
        if idx == -1:
            raise TypeError(
                f"Invalid method signature: could not find name ({self.__signature})"
            )

        name = self.__signature[:idx]
        if "->" in name:
            name = name[name.find("->") + 2 :]
        # Handle bracket names if not <clinit> or <init>
        if name in (Signature.INIT, Signature.CLINIT):
            return name

        return name.rstrip(">").lstrip("<")

    @property
    def declaring_class(self) -> SVMType | None:
        """Returns the :class:`SVMType` of the method's declaring class.

        >>> s1 = Signature("Lcom/example/Class;-><init>(II)V")
        >>> str(s1.declaring_class)
        'Lcom/example/Class;'
        >>> s2 = Signature("<init>(II)V")
        >>> str(s2.declaring_class)
        'None'

        :return: the method's declaring class
        :rtype: SVMType | None
        """
        if "->" not in self.sig:
            return None  # no class defined

        return SVMType(self.sig.split("->")[0])

    @property
    def parameter_types(self) -> list[SVMType]:
        """Returns the method parameter types.

        >>> s = Signature("<init>(II)V")
        >>> params: list[SVMType] = s.parameter_types
        >>> [str(x) for x in params]
        ["I", "I"]

        :return: the method parameters
        :rtype: list
        """
        if self.__params:
            return self.__params

        start = self.__signature.find("(")
        end = self.__signature.find(")")  # we don't want the closing brace
        if start == -1 or end == -1:
            raise TypeError("Invalid method signature")

        params = self.__signature[start + 1 : end]
        if not params:
            return []

        param_list = []
        current_param = ""
        is_type_def = False
        for char in params:
            current_param = f"{current_param}{char}"

            if char == "L":
                is_type_def = True
                continue

            if char == ";":
                # This check has to be made before validating whether
                # the current param is a custom type, otherwise the
                # whole string would be returned. See issue #3
                is_type_def = False

            if char == "[" or is_type_def:
                continue

            param_list.append(SVMType(current_param))
            current_param = ""

        if current_param:
            param_list.append(SVMType(current_param))

        self.__params = param_list
        return self.__params

    @property  # lazy
    def return_type(self) -> SVMType:
        """Retrieves the method's return type

        >>> s = Signature("<init>(II)V")
        >>> str(s.return_type) # returns a SVMType instance
        'V'

        :raises TypeError: if there is no valid return type
        :return: the return type's descriptor
        :rtype: str
        """
        if not self.__return_type:
            end = self.__signature.find(")")
            if end == -1:
                raise TypeError("Invalid method signature")
            self.__return_type = SVMType(self.__signature[end + 1 :])

        return self.__return_type

    @property
    def descriptor(self) -> str:
        """Returns the method descriptor of this signature

        >>> s = Signature("<init>(II)V")
        >>> s.descriptor
        '(II)V'

        :raises ValueError: if there is no descriptor
        :return: the method's descriptor string
        :rtype: str
        """
        idx = self.sig.find("(")
        if idx == -1:
            raise ValueError("Invalid method signature - expected '('")

        return self.sig[idx:]

    def __str__(self) -> str:
        return self.sig

    def __repr__(self) -> str:
        return f'Signature("{self.__signature}")'


class SVMType:
    class TYPES(Enum):
        """Represents the classification of a type descriptor."""

        ARRAY = 1
        PRIMITIVE = 2
        CLASS = 3
        METHOD = 4
        UNKNOWN = 5

    def __init__(self, __type: str) -> None:
        self.__class = SVMType.TYPES.UNKNOWN
        self.__dim = __type.count("[")
        self.__type = self._clean(str(__type))
        self.__array_type = None
        if self.dim > 0 and not self.is_signature():
            self.__class = SVMType.TYPES.ARRAY
            self.__array_type = SVMType(self.__type.replace("[", ""))

    def _clean(self, __type: str) -> str:
        # 1. check if we have a primitive type:
        if re.match(r"\[*[ZCBSIFVJD]$", __type):
            self.__class = SVMType.TYPES.PRIMITIVE
            return __type

        # 2. perform normalization
        value = __type.replace(".", "/")
        if "(" in value:
            # TODO: how to handle malformed method signatures
            self.__class = SVMType.TYPES.METHOD
            return value

        # 3. Perform class normalization
        idx = value.rfind("[") + 1
        if value[idx] != "L":
            if self.dim > 0:
                value = f"{value[:idx]}L{value[idx]}"
            else:
                value = f"L{value}"

        if not value.endswith(";"):
            value = f"{value};"

        self.__class = SVMType.TYPES.CLASS
        return value

    def __str__(self) -> str:
        return self.__type

    def __repr__(self) -> str:
        return f'SVMType("{self.__type}")'

    def is_signature(self) -> bool:
        """Returns whether this type instance is a method signature.

        >>> t = SVMType("<init>(II)V")
        >>> t.is_signature()
        True

        :return: True, if this instance represents a method signature
        :rtype: bool
        """
        return self.__class == SVMType.TYPES.METHOD

    @property
    def signature(self) -> Signature | None:
        """Creates a :class:`Signature` object from this type instance.

        :return: the signature object or nothing if this type does not represent a
                 method signature.
        :rtype: Signature | None
        """
        return None if self.svm_type != SVMType.TYPES.METHOD else Signature(self.__type)

    @property
    def dim(self) -> int:
        """Returns the amount of array dimensions.

        :return: the amount of array dimensions.
        :rtype: int
        """
        return self.__dim

    @property
    def svm_type(self) -> SVMType.TYPES:
        """Returns the descriptor classification (ARRAY, PRIMITIVE, METHOD or CLASS)

        :return: the classification of this type instance
        :rtype: SVMType.TYPES
        """
        return self.__class

    @property
    def array_type(self) -> SVMType:
        """Returns the underlying array type (if any)

        >>> array = SVMType("[[B")

        :return: the underlying array type instance
        :rtype: SVMType
        """
        return self.__array_type

    @property
    def pretty_name(self) -> str:
        """Returns a prettified version of the class name.

        >>> array = SVMType("[[Lcom/example/Class;")
        >>> array.pretty_name
        'com.example.Class[][]'

        :return: full name without ``L`` and ``;``; ``/`` is replaced by a dot.
        :rtype: str
        """
        array_type = self.array_type
        if not array_type:
            value = str(self)
        else:
            value = str(array_type)
        return re.sub(r"\/|(->)", ".", value.removeprefix("L").removesuffix(";")) + (
            "[]" * self.dim
        )

    @property
    def dvm_name(self) -> str:
        """Returns the DVM representation of this type descriptor.

        >>> cls = SVMType("Lcom/example/Class;")
        >>> cls.dvm_name
        'com/example/Class'

        Arrays won't be covered by this method, thus the returned value
        returns the full class name only:

        >>> cls = SVMType("[[Lcom/example/Class;")
        >>> cls.dvm_name
        'com/example/Class'

        :return: the full name without ``L`` and ``;``.
        :rtype: str
        """
        array_type = self.array_type
        if not array_type:
            value = str(self)
        else:
            value = str(array_type)
        return value.removeprefix("L").removesuffix(";")

    @property
    def full_name(self) -> str:
        """Returns the full name of this type descriptor (input value)

        >>> cls = SVMType("com.example.Class")
        >>> cls.full_name
        'Lcom/example/Class;'

        :return: the full name
        :rtype: str
        """
        return str(self)

    @property
    def simple_name(self) -> str:
        """Returns only the class name (not applicable to method signatures)

        :return: the class' name
        :rtype: str
        """
        return self.pretty_name.split(".")[-1]


def smali_value(value: str) -> int | float | str | SVMType | bool:
    """Parses the given string and returns its Smali value representation.

    :param value: the value as a string
    :type value: str
    :raises ValueError: if it has no valid Smali type
    :return: the Smali value representation
    :rtype: int | float | str | SVMType | bool
    """
    actual_value = None
    for i, entry in enumerate(TYPE_MAP):
        matcher, wrapper = entry
        if matcher.match(value):
            if i <= 3:  # hex value possible
                hex_val = RE_HEX_VALUE.match(value) is not None
                if not hex_val:
                    actual_value = wrapper(value)
                else:
                    actual_value = wrapper(value, base=16)
            else:
                actual_value = wrapper(value)
            break

    # Handling of null values is not implemented yet
    if actual_value is None:
        raise ValueError(f"Could not find any matching primitive type for {value}")

    return actual_value


RE_INT_VALUE = re.compile(r"[\-\+]?(0x)?[\dabcdefABCDEF]+$")
"""Pattern for ``int`` values."""

RE_BYTE_VALUE = re.compile(r"[\-\+]?(0x)?[\dabcdefABCDEF]+t$")
"""Pattern for ``byte`` values."""

RE_SHORT_VALUE = re.compile(r"[\-\+]?(0x)?[\dabcdefABCDEF]+s$")
"""Pattern for ``short`` values."""

RE_FLOAT_VALUE = re.compile(r"[\-\+]?\d+\.\d+f$")
"""Pattern for ``float`` values."""

RE_DOUBLE_VALUE = re.compile(r"[\-\+]?\d+\.\d+")
"""Pattern for ``double`` values."""

RE_LONG_VALUE = re.compile(r"[\-\+]?(0x)?[\dabcdefABCDEF]+l$")
"""Pattern for ``long`` values."""

RE_CHAR_VALUE = re.compile(r"^'.*'$")
"""Pattern for ``char`` values."""

RE_STRING_VALUE = re.compile(r'^".*"$')
"""Pattern for ``String`` values."""

RE_TYPE_VALUE = re.compile(r"\[*((L\S*;$)|([ZCBSIFVJD])$)")  # NOQA
"""Pattern for type descriptors."""

RE_BOOL_VALUE = re.compile(r"true|false")
"""Pattern for ``boolean`` values."""

RE_HEX_VALUE = re.compile(r"[\-\+]?0x[\dabcdefABCDEF]+")
"""Pattern for integer values."""

TYPE_MAP: list = [
    (RE_SHORT_VALUE, lambda x, **kw: int(x[:-1], **kw)),
    (RE_LONG_VALUE, lambda x, **kw: int(x[:-1], **kw)),
    (RE_BYTE_VALUE, lambda x, **kw: int(x[:-1], **kw)),
    (RE_INT_VALUE, int),
    (RE_BOOL_VALUE, lambda x: str(x).lower() == "true"),
    (RE_FLOAT_VALUE, lambda x: float(x[:-1])),
    (RE_DOUBLE_VALUE, lambda x: float(x[:-1])),
    (RE_CHAR_VALUE, lambda x: str(x[1:-1])),
    (
        RE_STRING_VALUE,
        lambda x: str(x[1:-1]).encode().decode("unicode_escape"),
    ),  # support unicode
    (RE_TYPE_VALUE, SVMType),
]
"""Defines custom handlers for actual value defintions

:meta private:
"""


def is_type_descriptor(value: str) -> bool:
    """Returns whether the given value is a valid type descriptor.

    :param value: the value to check
    :type value: str
    :return: True, if the value is a valid type descriptor
    :rtype: bool
    """
    return RE_TYPE_VALUE.match(value) is not None
