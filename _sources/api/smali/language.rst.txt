.. _smali_language:

**************
Smali Language
**************

Smali is an assembly-like language used to write code for Android 
apps. It is designed to be human-readable as well as easy to understand, 
while still being low-level enough to allow for fine-grained control 
over the app's behavior. 

.. contents:: Contents

Smali files come with the extension ``.smali`` and each of them 
correspond to a single Java class and has the same name as the class, 
but with slashes (``/``) replacing dots (``.``) in the package name. 
For example, the Java class ``com.example.MyClass`` would be represented 
by the Smali file ``com/example/MyClass.smali``. These names are referred
to *internal names*.

The structure of a Smali source code can be broken down into the following
sections:

Class Header
------------

The header of a Smali file contains several pieces of information that are 
used by the Smali assembler to build the final ``.dex`` file for an Android 
app. It starts with the ``.class`` directive, which specifies the name of the 
class being defined in the file. Here's an example:

.. code-block:: smali

    .class public Lcom/example/MyClass;

Here, we are defining a class called ``MyClass`` in the package ``com.example`` 
with ``public`` as its access modifier.  The class name is preceded by the letter
``L`` and is followed by a semicolon, which is the standard syntax for type 
descriptors in Smali. For more information about type descriptors, see chapter
:ref:`section-1.1.1` of the Smali API.

After the ``.class`` directive, the header can include several optional directives 
to provide additional information about the class. For example, you can use the 
``.super`` directive to specify the parent class of the current:

.. code-block:: smali

    .super Ljava/lang/Object;

This directive specifies that the our class inherits contents and functionalities
from ``java.lang.Object``.

Other optional directives that can appear in the header include:

* ``.implements``: 
    This directive is used to specify that the current class implements one or 
    more interfaces. For instance, the following code specifies that our class
    implements ``java.io.Serializable`` and ``android.os.Parcelable``:

    .. code-block:: smali

        .implements Ljava/io/Serializable;
        .implements Landroid/os/Parcelable;

* ``.source``:
    This directive is used to specify the name of the original source that Smali code 
    was generated from. This information can be useful for debugging purposes. Note 
    that for lambda-classes the source definition would point to ``lambda``:

    .. code-block:: smali

        .source "MyClass.java"

* ``.debug``:
    This directive is used to enable debug information for the current class. When 
    it is present, the Smali assembler will include additional metadata in the 
    final ``.dex`` file that can be used by debuggers:

    .. code-block:: smali

        .debug 0

.. note::

    The visitor API provided by this repository uses different method call for each of
    these directives to provide more flexibility while parsing. Therefore, if you want
    to get the header information on a class, you have to implement the following 
    methods:

        - ``visit_class``, and optionally
        - ``visit_super``, 
        - ``visit_source``,
        - ``visit_implements`` and
        - ``visit_debug``


In summary, the header of a Smali source file contains important metadata about the 
class being defined, as well as optional directives that provide additional information.

Class Annotations
-----------------

In Smali, class annotations are used to provide metadata information about a class. They 
are defined using the ``.annotation`` directive followed by their descriptor and elements.
Here is an example of how class annotations are defined in Smali:

.. code-block:: smali
    :linenos:

    .class public Lcom/example/MyClass;
    .super Ljava/lang/Object;

    .annotation runtime Ljava/lang/Deprecated;
    .end annotation

    .annotation system Ldalvik/annotation/EnclosingClass;
        value = Lcom/example/OuterClass;
    .end annotation

    .annotation system Ldalvik/annotation/InnerClass;
        accessFlags = 0x0008
        name = "MyClass"
        outer = Lcom/example/OuterClass;
    .end annotation

    # class definition and methods go here

In this example, we have defined three different class annotations:

* ``@Deprecated``:

    This runtime annotation indicates that the class is deprecated and should no 
    longer be used. It is defined using the ``@java/lang/Deprecated`` annotation 
    descriptor.

* ``@EnclosingClass``:

    This system annotation specifies the enclosing class of the current. It is 
    defined using the ``@dalvik/annotation/EnclosingClass`` descriptor. In this 
    case, it specifies that the enclosing class of ``MyClass`` is ``OuterClass``.

* ``@InnerClass``:
    
    This system annotation specifies that the class is an inner class. It is 
    defined using the ``@dalvik/annotation/InnerClass`` descriptor. In this case, 
    it specifies that the access flags for the class are ``0x0008`` (which means 
    it is static), the name of the class is ``MyClass``, and the outer class is 
    ``OuterClass``.

There is also a special annotation used to mark classes to contain generic types,
named `@Signature`. When used on a class, the annotation specifies the generic 
signature of the class, including its type parameters.

Here is an example of how the signature annotation can be used on a class in Smali:

.. code-block::
    :linenos:

    .class public interface abstract Lcom/example/MyClass;
    .super Ljava/lang/Object;

    # add the Signature annotation to the class
    .annotation system Ldalvik/annotation/Signature;
        value = {
            "<T:",
            "Ljava/lang/Object;
            ">",
            "Ljava/lang/Object;"
        }
    .end annotation

In this example, the ``MyClass`` class is defined with a type parameter `T` using 
the signature annotation. Converted into Java code, the class would look like the
folowing:

.. code-block:: java
    :linenos:

    public interface MyClass<T> {
        // ...
    }

.. note::

    All type descriptors that are defined after geenric type descriptors define the
    super classes of the declared class. In this case, there is only one super class
    (`Ljava/lang/Object;`).

Fields
------

The ``.field`` directive in Smali is used to define a field within a class. The general 
syntax for the field directive is as follows:

.. code-block:: bnf

    .field <access_flags> <name>:<type_descriptor> [ = <value> ]

Here is a breakdown of the different components of the field directive:

* ``access_flags``: 

    Access flags specifiy the access modifiers for the field being defined. It can be
    one of the following values:

    .. list-table:: Access flags of the ``.field`` directive
        :header-rows: 1
        :widths: 10, 15

        * - Name
          - Description
        * - ``public``
          - The field can be accessed from anywhere within the application.
        * - ``protected``
          - The field can be accessed within the same package or by a subclass.
        * - ``private``
          - The field can only be accessed within the same class or by a non-static
            subclass.
        * - ``static``
          - The field belongs to the class, but not to any instance of the class.
        * - ``final``
          - The field cannot be modified once it has been initialized.
        * - ``synthetic``
          - The field is generated by the compiler and not present in the original source code.
    
    You can use a combination of these flags to specify the desired access level for 
    the field. They can be retrieved by using the ``AccessType`` class:

    .. code-block:: python
        :linenos:

        from smali import AccessType

        # Retrieve integer flags for access modifiers
        flags: int = AccessType.get_flags(["public", "static", "final"])
        # Convert the flags back into human readable names
        flag_names: list[str] = AccessType.get_names(flags)

        # or reference them directly
        flags: int = AccessType.PUBLIC + AccessType.STATIC + AccessType.FINAL

* ``<name>``:

    This section specifies the name of the field. It should start with a letter and can contain 
    letters, digits, underscores, and dollar signs. It must not start with a number.

* ``<type_descriptor>``:

    The type descriptor is a string that represents the type of the field. The structure of type
    descriptors is described in the :ref:`section-1.1.1` chapter of the Smali API.

* ``<value>``:

    The value definition is used when the field should be assigned directly with a value.

Let's take a quick look at a small example of the ``.field`` directive:

.. code-block:: smali

    .field private myField:I

Here, we are defining a private integer field named *myField*. The ``I`` type descriptor 
indicates that this field has an integer as its value. This field can only be accessed 
within the same class or any non-static sub-class.


Methods
-------

In Smali, a method definition consists of several components, including access modifiers, 
return type, parameter types, and implementation code. The code block contains the actual
assembly-like code that is executed when the method is called. It can contain registers, 
instructions, labels, and exception handlers.

.. code-block:: bnf

    .method <access_flags> <name>(<parameter_types>)<return_type>
        <code_block>
    .end method

Here is a breakdown of the different components of the method directive:

* ``<access_flags>``:

    Access flags specifiy the access modifiers for the method. It can have the
    same values as defined before in field definitions.

* ``<name>``:

    Stores the actual method name used in references. There are two special method
    names that are pre-defined: ``<cinit>`` for constructor methods and ``clinit``
    for static initializer blocks.

* ``<parameter_types>``:

    These are the type descriptors of the parameters of the method. 

* ``<return_type>``:

    Defines the return type for this method (type descriptor).

* ``<code_block>``:

    This is the actual code that performs the functionality of the method. It may
    contain the following sections:

    - Registers: 
        
        Registers are used to store temporary data and intermediate results during the 
        execution of the method. They are specified using the letter ``v`` followed 
        by a number (e.g., ``v0``, ``v1``, ``v2``, etc.).
   
    - Instructions: 
    
        Instructions are used to perform operations on registers or objects. Each 
        instruction is represented by a mnemonic (e.g., ``move``, ``add``, ``sub``, etc.) 
        followed by its operands. Operands can be registers, constants, or labels.

    - Labels: 
    
        Labels are used to mark specific locations in the code block. They are 
        specified using a colon (``:``) followed by its name (e.g., ``:label1``, 
        ``:label2``, etc.).

    - Exception handlers: 
    
        Exception handlers are used to handle exceptions that may occur during the 
        execution of the method. They are specified using the ``.catch`` directive, 
        followed by the type of the exception that is being caught and the label of the handler.

The following example method written in Smali can be used to print ``"Hello World"``
to the console:

.. code-block:: smali
    :linenos:

    .method public static main([Ljava/lang/String;)V
        .registers 2

        sget-object v0, Ljava/lang/System;->out:Ljava/lang/PrintStream;

        const-string v1, "Hello World"

        invoke-virtual {v0, v1}, Ljava/lang/PrintStream;->println(Ljava/lang/String;)V

        return-void

    .end method

explanation:

- Line 1:
    
    In the first line we defined a method with name ``main`` that returns nothing 
    and takes a string array (``String[]``) as an argument. 

- Line 2:

    ``.registers 2`` declares that the method will use 2 registers, so we can use 
    ``v0`` and ``v1`` within the method.

- Line 4:

    The instruction ``sget-object`` loads the ``PrintStream`` object named *out*
    into the first register (``v0``).

- Line 6:

    The instruction ``const-string`` defines a string variable that will be loaded
    into the register ``v1``.

- Line 8:

    With ``invoke-virtual`` we are calling the method *println* of the Java class
    ``PrintStream`` to print our string in register ``v1`` to the console.

- Line 10:

    ``return-void`` exits the method execution.


Annotations
-----------

The ``.annotation`` directive in Smali is used to define an annotation. The structure of this 
directive is as follows:

.. code-block:: bnf

    .[sub]annotation <visibility> <annotation_type>
        [ <properties> ]
    .end [sub]annotation

The annotation directive starts with the ``.annotation`` or ``.subannotation`` keyword followed 
by the visibility and the type descriptor for the annotation. There are three possible values 
for the annotation's visibility:

- ``runtime``: The annotation is visible at runtime and can be queried using reflection.
- ``system``: The annotation is a system annotation and is not visible to the user.
- ``build``: Another system annotation that indicates special treating of the annotated value.

After the visibility and annotation type descriptor, the properties are defined. These are 
key-value pairs, where the key is the property's name and the value is the property's value. The 
properties are defined using the syntax ``key = value``. It is possible to define multiple 
properties on separate lines within one annotation directive.

Finally, the annotation directive is closed using the ``.end annotation`` keyword. Here is an 
example of an annotation directive in Smali:

.. code-block:: smali
    :linenos:

    .annotation runtime Lcom/example/MyAnnotation;
        name = "John Doe"
        age = .subannotation runtime Lcom/example/Age;
                value = 30
              .end subannotation
    .end annotation

The sample defines an annotation named ``MyAnnotation`` with two properties: *name* and *age*. 
The name property is a simple string and has a value of ``"John Doe"``, and the age property 
is a sub-annotation with a value of 30. The ``runtime`` keyword specifies that the annotation 
is visible at runtime of the application.