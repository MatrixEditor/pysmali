.. _smali_api:

*********
Smali API
*********

.. automodule:: smali

.. contents:: Contents

Overview
========

The overall structur of a decompiled Smali class is rather simple. In fact
a decompiled source class contains:

* A section describing the class' modifiers (such as ``public`` or ``private``), its name, super class and the implemented interfaces.

* One section per annotation at class level. Each section describes the name, modifiers (such as ``runtime`` or ``system``), and the type. Optionally, there are sub-annotations included as values in each section.

* One section per field declared in this class. Each section describes the name, modifiers (such as ``public`` or ``static``), and the type. Optionally, there are annotations placed within the section.

* One section per method, constructor (``<cinit>``) and static initializer block (``clinit``) describing their name, parameter types and return type. Each section may store instruction information.

* Sections for line-based comments (lines that start with a ``#``).

As Smali source code files does not contain any ``package`` or ``import`` statements
like they are present Java classes, all names must be fully qualified. The structure
of these names are described in the Java ASM documentationin section 2.1.2 [1]_.

.. _section-1.1.1:

Type descriptors
----------------

Type descriptors used in Smali source code are similar to those used in compiled
Java classes. The following list was taken from ASM API [1]_:

.. list-table:: Type descriptors of some Smali types
    :header-rows: 1
    :widths: 10, 15, 10

    * - Smali type
      - Type descriptor
      - Example value
    * - ``void``
      - V
      - --
    * - ``boolean``
      - Z
      - ``true`` or ``false``
    * - ``char``
      - C
      - ``'a'``
    * - ``byte``
      - B
      - ``1t``
    * - ``short``
      - S
      - ``2s``
    * - ``int``
      - I
      - ``0x1``
    * - ``float``
      - F
      - ``3.0f``
    * - ``long``
      - J
      - ``5l``
    * - ``double``
      - D
      - ``2.0``
    * - ``Object``
      - Ljava/lang/Object;
      - --
    * - ``boolean[]``
      - [Z
      - --

The descriptors of primitive types can be represented with single characters. Class
type descriptors always start with a ``L`` and end with a semicolon. In addition to
that, array type descriptors will start with opened square brackets according to the
number of dimensions. For instance, a two dimensional array would get two opened square
brackets in its type descriptor.

This API contains a class called :class:`SVMType` that can be used to retrieve type descriptors
as well as class names:

.. code-block:: python
    :linenos:

    from smali import SVMType, Signature

    # simple type instance
    t = SVMType("Lcom/example/Class;")
    t.simple_name # Class
    t.pretty_name # com.example.Class
    t.dvm_name # com/example/Class
    t.full_name # Lcom/example/Class;
    t.svm_type # SVMType.TYPES.CLASS

    # create new type instance for method signature
    m = SVMType("getName([BLjava/lang/String;)Ljava/lang/String;")
    m.svm_type # SVMType.TYPES.METHOD
    # retrieve signature instance
    s = m.signature or Signature(m)
    s.return_type # SVMType("Ljava/lang/String;")
    s.parameter_types # [SVMType("[B"), SVMType("Ljava/lang/String;")]
    s.name # getName
    s.declaring_class # would return the class before '->' (only if defined)

    # array types
    array = SVMType("[B")
    array.svm_type # SVMType.TYPES.ARRAY
    array.array_type # SVMType("B")
    array.dim # 1 (one dimension)

As an input can be used anything that represents the class as type descriptor, original
class name or internal name (array types are supported as well).

Method descriptors
------------------

Unlike method descriptors in compiled Java classes, Smali's method descriptors contain the
method's name. The general structure, described in detail in the ASM API [1]_ documentation,
is the same. To get contents of a method descriptor the :class:`SVMType` class, introduced before,
can be used again:

.. code-block:: python
    :linenos:

    from smali import SVMType

    method = SVMType("getName([BLjava/lang/String;)Ljava/lang/String;")
    # get the method's signature
    signature = method.signature
    # get parameter type descriptors
    params: list[SVMType] = signature.parameter_types
    # get return type descriptor
    return_type = signature.return_type

    # the class type can be retrieved if defined
    cls: SVMType = signature.declaring_class

.. caution::

    The initial method descriptor must be valid as it can cause undefined behaviour
    if custom strings are used.


Interfaces and components
=========================

The Smali Visitor-API for generating and transforming Smali-Source files
(no bytecode data) is based on the :class:`ClassVisitor` class, similar to the
ASM API [1]_ in Java. Each method in
this class is called whenever the corresponding code structure has been
parsed. There are two ways how to visit a code structure:

    1. Simple visit:
        All necessary information are given within the method parameters

    2. Extendend visit:
        To deep further into the source code, another visitor instance is
        needed (for fields, methods, sub-annotations or annotations and
        even inner classes)

The same rules are applied to all other visitor classes. The base class of
all visitors must be :class:`VisitorBase` as it contains common methods all sub
classes need:

.. code-block:: python

    class VisitorBase:
        def __init__(self, delegate) -> None: ...
        def visit_comment(self, text: str) -> None: ...
        def visit_eol_comment(self, text: str) -> None: ...
        def visit_end(self) -> None: ...

All visitor classes come with a delegate that can be used together with the
initial visitor. For instance, we can use our own visitor class together with
the provided :class:`SmaliWriter` that automatically writes the source code.

.. note::
    The delegate must be an instance of the same class, so :class:`FieldVisitor`
    objects can't be applied to :class:`MethodVisitor` objects as a delegate.

The provided Smali API provides three core components:

    * The :class:`SmaliReader` class is an implementation of a line-based parser that can handle *.smali* files. It can use both utf-8 strings or bytes as an input. It calls the corresponding *visitXXX* methods on the :class:`ClassVisitor`.

    * The :class:`SmaliWriter` is a subclass of :class:`ClassVisitor` that tries to build a Smali file based on the visited statements. It comes together with an ``AnnotationWriter``, ``FieldWriter`` and ``MethodWriter``. It produces an output utf-8 string that can be encoded into bytes.

    * The ``XXXVisitor`` classes delegate method calls to internal delegate candicates that must be set with initialisation.

The next sections provide basic usage examples on how to generate or transform Smali class
files with these components.


Parsing classes
---------------

The only required component to parse an existing Smali source file is the :class:`SmaliReader`
component. To illustrate an example usage, assume we want to print out the parsed
class name, super class and implementing interfaces:

.. code-block:: python
    :linenos:

    from smali import ClassVisitor

    class SmaliClassPrinter(ClassVisitor):
        def visit_class(self, name: str, access_flags: int) -> None:
            # The provided name is the type descriptor - if we want the
            # Java class name, use a SVMType() call:
            # cls_name = SVMType(name).simple_name
            print(f'.class {name}')

        def visit_super(self, super_class: str) -> None:
            print(f".super {super_class}")

        def visit_implements(self, interface: str) -> None:
            print(f".implements {interface}")

The second step is to use our previous defined visitor class with a :class:`SmaliReader`
component:

.. code-block:: python
    :linenos:
    :emphasize-lines: 5

    # Let's assume the source code is stored here
    source = ...

    printer = SmaliClassPrinter()
    reader = SmaliReader(comments=False)
    reader.visit(source, printer)

The fifth line creates a :class:`SmaliReader` that ignores all comments in the source
file to parse. The *visit* method is called at the end to parse the source code
file.

Generating classes
------------------

The only required component to generate a new Smali source file is the :class:`SmaliWriter`
component. For instance, consider the following class:

.. code-block:: smali
    :linenos:

    .class public abstract Lcom/example/Car;
    .super Ljava/lang/Object;

    .implements Ljava/lang/Runnable;

    .field private id:I

    .method public abstract run()I
    .end method

It can be generated within seven method calls to a :class:`SmaliWriter`:

.. code-block:: python
    :linenos:
    :emphasize-lines: 3,16,20

    from smali import SmaliWriter, AccessType

    writer = SmaliWriter()
    # Create the .class statement
    writer.visit_class("Lcom/example/Car;", AccessType.PUBLIC + AccessType.ABSTRACT)
    # Declare the super class
    writer.visit_super("Ljava/lang/Object;")
    # Visit the interface implementation
    writer.visit_implements("Ljava/lang/Runnable")

    # Create the field id
    writer.visit_field("id", AccessType.PRIVATE, "I")

    # Create the method
    m_writer = writer.visit_method("run", AccessType.PUBLIC + AccessType.ABSTRACT, [], "V")
    m_writer.visit_end()

    # finish class creation
    writer.visit_end()
    source_code = writer.code

At line 3 a :class:`SmaliWriter` is created that will actually build the source code
string.

The call to ``visit_class`` defines the class header (see line 1 of smali source
code). The first argument represents the class' type descriptor and the second its
modifiers. To specify additional modifiers, use the :class:`AccessType` class. It provides
two ways how to retrieve the actual modifiers:

* Either by referencing the enum (like ``AccessType.PUBLIC``)
* or by providing a list of keywords that should be translated into modifier flags:

    .. code-block:: python

        modifiers = AccessType.get_flags(["public", "final"])

The calls to ``visit_super`` defines the super class of our previously defined
class and to ``visit_implements`` specifies which interfaces are implemented by our
class. All arguments must be type descriptors to generate accurate Smali code (see
section :ref:`section-1.1.1` for more information on the type class)



.. Footnotes

.. [1] ASM API documentation `here <https://asm.ow2.io/asm4-guide.pdf)>`_