.. _smali_bridge:

********
Smali VM
********

.. automodule:: smali.bridge.vm

As of version ``0.1.1`` it is possible to import Smali source code files into
the provided :class:`SmaliVM`. All classes are stored globally, so there can't be
two classes with the same type descriptor. To create a simple Smali emulator,
just create a new :class:`SmaliVM` instance:

.. code:: python

    from smali.bridge import SmaliVM

    vm = SmaliVM()


.. hint::

    If you want to create a custom import process, just create sub-class of
    :class:`ClassLoader` and provide an instance of it in the constructor of the
    :class:`SmaliVM`.

Next, classes are used as prototypes to create new objects of their type. The
class creation and object initialization is rather simple:

.. code-block:: python
    :linenos:

    from smali.bridge import SmaliClass, SmaliObject, SmaliVM

    # Let's assume, the class' source code is stored here
    source = ...

    vm = SmaliVM()
    # Load and define the class (don't call the <clinit> method)
    my_class = vm.classloader.load_class(source, init=False)

    # To manually initialize the class, call <clinit>
    my_class.clinit()

    # Instances can be created by providing the class object
    instance = SmaliObject(my_class)

    # Initialization must be done separately:
    instance.init(...)

    # Methods are stored in our class object (not in the
    # actual instance)
    toString = my_class.method("toString")

    # The first argument of instance method must be the
    # object itself (on static methods, just use None)
    value = toString(instance)

    # The returned value behaves like a string
    print("Returned value:", value)


.. autoclass:: smali.bridge.vm.SmaliVM
    :members:

.. autoclass:: smali.bridge.vm.ClassLoader
    :members: