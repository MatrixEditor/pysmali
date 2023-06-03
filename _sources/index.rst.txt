.. PySmali documentation master file, created by
   sphinx-quickstart on Wed Mar 8 22:33:21 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PySmali's documentation
=======================

Welcome to the documentation for `pysmali`, a Python3 package designed for parsing,
transforming and generating Smali source code files, as well as interpreting source
code files. This documentation is intended to provide an overview of the package's
features, installation instructions, and usage examples to help you get started with
using the package in your Python projects.

Using this library
------------------

:doc:`installation`
   How to install the python package locally or in a virtal environment.

:doc:`Using the Smali API <api/smali/index>`
   Introduction into Smali and the provided Smali API.

:doc:`Using the Smali-Emulator <api/smali/bridge>`
   Introduction into the provided Smali-Interpreter.

:ref:`supported-dependencies`
   Supported project dependencies.


Examples
--------

.. code-block:: python
   :caption: Reading Smali code
   :linenos:

   from smali import SmaliReader, SmaliWriter

   reader = SmaliReader(comments=False)
   writer = SmaliWriter(reader)

   with open('example.smali', 'r', encoding='utf-8') as fp:
      source = fp.read()

   # The writer can be any instance of a class visitor
   reader.visit(source, writer)
   print(writer.code)
   # or
   print(str(writer))

.. code-block:: python
    :linenos:
    :caption: Modifying Smali code

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


.. code-block:: python
   :linenos:
   :caption: Execute Smali code

   from smali.bridge import SmaliClass, SmaliObject, SmaliVM

   # Let's assume, the class' source code is stored here
   source = ...

   vm = SmaliVM()
   # Load and define the class (don't call the <clinit> method)
   my_class: SmaliClass = vm.classloader.load_class(source, init=False)

   # To manually initialize the class, call <clinit>
   my_class.clinit()

   # Instances can be created by providing the class object
   instance: SmaliObject = SmaliObject(my_class)

   # Initialization must be done separately:
   instance.init(...)

   # Methods are stored in our class object (not in the
   # actual instance)
   toString: SmaliMethod = my_class.method("toString")

   # The first argument of instance method must be the
   # object itself (on static methods, just use None)
   value = toString(instance)

   # The returned value behaves like a string
   print("Returned value:", value)


To execute Smali files from the cli, just use the ``ismali`` command that comes with
installation of this module:

.. code-block:: bash

   $ ismali
   >>> vars
   {'p0': <SmaliObject@20776587040>}
   >>> const-string v1, "Hello World"
   >>> vars
   {'p0': <SmaliObject@20776587040>, 'v1': 'Hello World'}


Development
-----------

:doc:`contributing`
    How to contribute changes to the project.

:doc:`Development guidelines <development>`
    Guidelines the theme developers use for developing and testing changes.

:doc:`changelog`
    The package development changelog.

.. toctree::
   :maxdepth: 3
   :caption: General Documentation
   :hidden:

   installation
   api/smali/language
   development
   contributing
   changelog

.. Hidden TOCs

.. toctree::
   :maxdepth: 3
   :caption: Smali API Documentation
   :hidden:
   :numbered:

   api/smali/index
   api/smali/reader
   api/smali/writer
   api/smali/visitor
   api/smali/base


.. toctree::
   :maxdepth: 3
   :caption: Smali Bridge
   :hidden:
   :numbered:

   api/smali/bridge
   api/smali/bridge_api
   api/smali/shell



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
