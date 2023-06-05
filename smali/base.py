# This file is part of pysmali's Smali API
# Copyright (C) 2023 MatrixEditor

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
Basic component classes when working with the Smali language.
"""

import re

from enum import Enum, IntFlag

__all__ = ["AccessType", "Token", "Line", "Type", "smali_value", "SmaliValueProxy"]


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

    RE_EOL_COMMENT = re.compile(r"\s*#.*")
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
            if end - 1 > 0 and cleaned[end - 1] == '"':
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


class Type:
    """Basic type definition that can handle both class and method types."""

    CLINIT = "<clinit>"
    """Static block initializer"""

    INIT = "<init>"
    """Constructor method"""

    def __init__(self, signature: str) -> None:
        self.__signature = signature.strip()
        if isinstance(signature, type):
            self.__signature = f"{signature.__module__}.{signature.__name__}"

    @property
    def descriptor(self) -> str:
        """Returns the type descriptor of this type.

        :return: the type descriptor used in the DVM (e.g. "Lcom/example/ABC;")
        :rtype: str
        """
        name = self.__signature
        if SmaliValueProxy.RE_TYPE_VALUE.match(name):
            return name

        if name.startswith("["):
            idx = name.rfind("[")
            prefix = name[:idx]
            if not name.endswith(";") and name not in "ZCBSIFVJD":
                return prefix + f"L{name[idx+1:].replace('.', '/')};"

            return prefix + f"{name[idx+1:].replace('.', '/')}"

        name = f"{name.replace('.', '/')}"
        if name[-1] != ";" and name not in "ZCBSIFVJD":
            name = f"L{name};"
        return name

    @property
    def dim(self) -> int:
        """Returns the amount of array dimensions.

        :return: the amount of array dimensions.
        :rtype: int
        """
        return self.__signature.count("[")

    @property
    def type_name(self) -> str:
        """Returns the type name without 'L' and ';'

        :return: the type name
        :rtype: str
        """
        if not SmaliValueProxy.RE_TYPE_VALUE.match(self.__signature):
            return self.__signature
        name = self.__signature.lstrip("[").replace(".", "/")
        return name.lstrip("L").rstrip(";")

    @property
    def class_name(self) -> str:
        """Returns the Smali class name equivalent to Smali class names.

        :return: the class name (e.g. "com.example.ABC")
        :rtype: str
        """
        return self.type_name.replace("/", ".").replace("[", "")

    def get_method_name(self) -> str:
        """Returns the method name

        :return: the absolute method name
        :rtype: str
        """
        idx = self.__signature.find("(")
        if idx == -1:
            raise TypeError(
                f"Invalid method signature: could not find name ({self.__signature})"
            )


        name = self.__signature[:idx]
        if "->" in name:
            name = name[name.find("->") + 2:]
        # Handle bracket names if not <clinit> or <init>
        if name in (Type.INIT, Type.CLINIT):
            return name

        return name.rstrip(">").lstrip("<")

    def get_method_params(self) -> list:
        """Returns the method parameter internal names.

        :return: the method parameters
        :rtype: list
        """
        start = self.__signature.find("(")
        end = self.__signature.find(")")
        if start == -1 or end == -1 or (end < start):
            raise TypeError("Invalid method signature")

        params = self.__signature[start + 1 : end]

        d = ";"
        param_list = [param + d for param in params.split(d) if param]

        return param_list

    def get_method_return_type(self) -> str:
        """Retrieves the method's return type

        :raises TypeError: if there is no valid return type
        :return: the return type's descriptor
        :rtype: str
        """
        end = self.__signature.find(")")
        if end == -1:
            raise TypeError("Invalid method signature")
        return self.__signature[end + 1 :]

    def __str__(self) -> str:
        return self.__signature

    def __repr__(self) -> str:
        return f"<Type sig='{self.__signature}'>"

def smali_value(value: str) -> "SmaliValueProxy":
    """Parses the given string and returns its Smali value representation.

    :param value: the value as a string
    :type value: str
    :raises ValueError: if it has no valid Smali type
    :return: the Smali value representation
    :rtype: SmaliValueProxy
    """
    sm_value = SmaliValueProxy()
    sm_value.value = value
    sm_value.actual_value = None
    for i, entry in enumerate(SmaliValueProxy.TYPE_MAP):
        matcher, wrapper = entry
        if matcher.match(sm_value.value):
            if i <= 3:  # hex value possible
                hex_val = SmaliValueProxy.RE_HEX_VALUE.match(value) is not None
                if not hex_val:
                    sm_value.actual_value = wrapper(value)
                else:
                    sm_value.actual_value = wrapper(value, base=16)
            else:
                sm_value.actual_value = wrapper(value)
            break

    # Handling of null values is not implemented yet
    if sm_value.actual_value is None:
        raise ValueError(f"Could not find any matching primitive type for {value}")

    sm_locals = {}
    for key in __smali_builtins__:
        if hasattr(sm_value.actual_value, key):
            sm_locals[key] = getattr(sm_value.actual_value, key)

    vars(sm_value).update(sm_locals)
    return sm_value


class SmaliValueProxy:
    """Wrapper class for primitives in Smali.

    Use this class to retrieve the actual primitiva value for a parsed
    source code snippet. As this class overrides most of the internal
    special functions, objects of this class can be used as regualar
    strings or numeric values:

    >>> value = SmaliValue("1234")
    1234
    >>> value += 1
    1235

    The same behaviour applies to parsed strings (note that you need
    quotation marks):

    >>> string = SmaliValue('"Hello World"')
    'Hello World'
    >>> len(string)
    11
    """

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

    RE_HEX_VALUE = re.compile(r"0x[\dabcdefABCDEF]+")
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
        (RE_STRING_VALUE, lambda x: str(x[1:-1])),
        (RE_TYPE_VALUE, Type),
    ]
    """Defines custom handlers for actual value defintions

    :meta private:
    """

    value: str
    """The initial source code value (string)"""

    actual_value = None
    """The actual value of any type"""

    @staticmethod
    def is_type_descriptor(value: str) -> bool:
        """Returns whether the given value is a valid type descriptor.

        :param value: the value to check
        :type value: str
        :return: True, if the value is a valid type descriptor
        :rtype: bool
        """
        return SmaliValueProxy.RE_TYPE_VALUE.match(value) is not None


####################################################################################
# INTERNAL
####################################################################################

__smali_builtins__ = [
    "__contains__", "__eq__", "__ne__", "__len__", "__str__", "__next__", "__bool__",
    "__repr__", "__str__", "__bytes__", "__format__", "__lt__", "__le__", "__eq__",
    "__ne__", "__gt__", "__ge__", "__hash__", "__bool__", "__len__", "__length_hint__",
    "__getitem__", "__setitem__", "__delitem__", "__missing__", "__iter__", "__reversed__",
    "__contains__", "__add__", "__sub__", "__mul__", "__truediv__", "__floordiv__",
    "__mod__", "__divmod__", "__lshift__", "__rshift__", "__and__", "__xor__", "__or__",
    "__radd__", "__rsub__", "__rmul__", "__rtruediv__", "__rfloordiv__", "__rmod__",
    "__rdivmod__", "__rlshift__", "__rrshift__", "__rand__", "__rxor__", "__ror__",
    "__neg__", "__pos__", "__abs__", "__invert__", "__complex__", "__int__", "__float__",
    "__index__", "__trunc__", "__floor__", "__ceil__",
]

__smali_specials__ = [
    ("__iadd__", lambda x, y: x.actual_value + y.actual_value),
    ("__isub__", lambda x, y: x.actual_value - y.actual_value),
    ("__imul__", lambda x, y: x.actual_value * y.actual_value),
    ("__itruediv__", lambda x, y: x.actual_value / y.actual_value),
    ("__ifloordiv__", lambda x, y: x.actual_value // y.actual_value),
    ("__imod__", lambda x, y: x.actual_value % y.actual_value),
    ("__ilshift__", lambda x, y: x.actual_value << y.actual_value),
    ("__irshift__", lambda x, y: x.actual_value >> y.actual_value),
    ("__iand__", lambda x, y: x.actual_value & y.actual_value),
    ("__ixor__", lambda x, y: x.actual_value ^ y.actual_value),
    ("__ior__", lambda x, y: x.actual_value | y.actual_value),
]


def __wrap_args__(self, target: str, *args):
    """Tries to wrap ``SmalivalueProxy`` objects before calling the special method.

    :param target: the method to call
    :type target: str
    """
    if len(args) == 0:
        return self.__dict__[target](*args)

    new_args = []
    for val in args:
        # Built-in types will throw errors when using executing
        # SmaliValueProxy * SmaliValueProxy, so we have to convert
        # the proxy argument by using the actual value
        if isinstance(val, SmaliValueProxy):
            new_args.append(val.actual_value)
        else:
            new_args.append(val)

    return self.__dict__[target](*new_args)


for method in __smali_builtins__:
    setattr(
        SmaliValueProxy,
        method,
        lambda self, *args, method=method: __wrap_args__(self, method, *args),
    )


def __wrap_special__(instance, actual_val, val, funct):
    funct(actual_val, val)
    return instance


for method, func in __smali_specials__:
    setattr(
        SmaliValueProxy,
        method,
        lambda self, val, func=func: __wrap_special__(
            self, self.actual_value, val, func
        ),
    )

del method
del func
