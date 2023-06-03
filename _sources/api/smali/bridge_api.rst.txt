.. _smali_bridge_api:

****************
Smali Bridge API
****************

Execution Frame
===============

.. automodule:: smali.bridge.frame

.. autoclass:: smali.bridge.frame.Frame
    :members:

Language members
================

.. automodule:: smali.bridge.lang

.. autoclass:: smali.bridge.lang.SmaliMember
    :members:

.. autoclass:: smali.bridge.lang.SmaliAnnotation
    :members:

.. autoclass:: smali.bridge.lang.SmaliField
    :members:

.. autoclass:: smali.bridge.lang.SmaliMethod
    :members:

.. autoclass:: smali.bridge.lang._MethodBroker
    :members:

.. autoclass:: smali.bridge.lang.SmaliClass
    :members:

.. autoclass:: smali.bridge.lang.SmaliObject
    :members:

Common error classes
====================

The following classes are defined in the ``smali.bridge.errors`` module:

.. autoclass:: smali.bridge.errors.NoSuchClassError

.. autoclass:: smali.bridge.errors.NoSuchMethodError

.. autoclass:: smali.bridge.errors.NoSuchFieldError

.. autoclass:: smali.bridge.errors.NoSuchOpcodeError

.. autoclass:: smali.bridge.errors.InvalidOpcodeError

.. autoclass:: smali.bridge.errors.NoSuchRegisterError

.. autoclass:: smali.bridge.errors.ExecutionError
    :members:
