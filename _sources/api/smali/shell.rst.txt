.. _smali_shell:

********************
Smali Shell (ISmali)
********************

Introducing a new file format that combines the simplicity of shell scripts with the power of Smali-Code 
in version :ref:`release-0.1.1` of this project. This new format, which will be called Smali-Script is 
defined by the file suffix ``".ssf"``. It is designed to allow users to create and run Smali-Code directly 
from a single file, using Smali's syntax.

To use a Smali-Script file, users simply need to create a new file with the ``.ssf`` suffix and write their 
Smali-Code. They can then run it with ``ismali``. This makes it an ideal format for executing small code 
snippets that can be used within deobfuscation.

.. code-block:: bash

    $ ismali
    ISmali $VERSION on $PLATFORM
    >>> # put Smali instructions here

Before starting to execute Smali instructions, it is worth to know that there are some
global variables that can be queried:

* ``vars``: This command will print out all registers with their values
* ``label``: Prints the name of the current label
* ``fields``: Prints all fields that have been defined in the root context
* ``import``: Loads a class defined in a ``*.smali`` file. The class can be used afterwards

.. note::

    By now, only primitive types and ``String`` objects can be instantiated. Instances of other
    types can be created after importing the class. All instructions will be executed directly and
    fields will be stored in the root class named ``L<Root>;``.


Define Smali-Fields
===================

Fields can be defined rather easily. By now, only one-liner are accepted:

.. code-block:: bash
    :linenos:

    >>> .field public static abc:Ljava/lang/String; = "Hello, World!"
    >>> # Retrieve the value via sget on static fields
    >>> sget v0, L<Root>;->abc:Ljava/lang/String;
    >>> vars
    {'p0': <SmaliObject@289e5e06fd0>, 'v0': 'Hello, World!'}

In the first line of the code above we defined a new static field with a pre-defined value 
``"Hello, World!"``. Next, the value of our field is stored in the register ``v0`` (actually,
the name can be customized). Because we moved abc's value into a register, we can see that
value by typing ``vars``.

Execute Smali-Methods
=====================

The next example illustrates how to simply invoke a method within the interpreter.

.. warning::

    As of version ``0.2.0`` it is not possible two define methods in the root-context. This feature
    is proposed to be released in the next version.

.. code-block:: bash
    :linenos:

    >>> invoke-virtual {p0}, Ljava/lang/Object;->toString()Ljava/lang/String;
    >>> move-result-object v1
    >>> vars
    {'p0': <SmaliObject@25490b06fd0>,
     'v1': '<SmaliObject@25490b06fd0 fields=0 type=<SmaliClass L<Root>;>'}
    
In this example we called ``Object.toString()`` within the root-context. As we can see, the first 
register stores the actual instance and the second (``v0``) a string representation of it.


Shell Components
================

.. automodule:: smali.shell
    :members:

.. autoclass:: smali.shell.ISmaliShell
    :members:

