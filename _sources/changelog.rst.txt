.. _changelog:

*********
Changelog
*********

.. _release-0.2.6:

0.2.6
-----

Some bug fixes by `WaferJay <https://github.com/WaferJay>`_.

* Fixed a bug in end of line comments not parsed properly in strings with `#` inside
* Improved `.catchall` directive
* Other fixes, see `Commit details <https://github.com/MatrixEditor/pysmali/commit/e33b88426bb65eea474d85032c3185a8089a2b92>`_


.. _release-0.2.5:

0.2.5
-----

Some fixes around :class:`_SmaliMethodWriter` by `WaferJay <https://github.com/WaferJay>`_.

* Added missing `.end` directives for packed-switch, sparse-switch and array-data

.. _release-0.2.4:

0.2.4
-----

* Improved `pretty_name` and `dvm_name` of :class:`SVMType`

.. _release-0.2.3:

0.2.3
-----

* Fixed issues #1 and `#2 <https://github.com/MatrixEditor/pysmali/issues/2>`_
* Added an appropriate error message upon invalid statements.

.. _release-0.2.2:

0.2.2
-----

A small patch created by `TheZ3ro <https://github.com/TheZ3ro>`_ fixing the following issues:

* Fixed ``sparse_switch`` executor that was not executed due to a typo
* String regex now support handling of unicode strings (e.g. ``const-string v0, "\u06e4\u06eb``"), which initially would result in an error

In addition, this patch introduces the following new features:

* Hex values regex now support negative and positive numbers (e.g. ``const v1, -0x1``)
* Added ``move_object`` executor
* Added ``java.lang.String.hashCode()`` implementation as a direct-call
* Refactored direct-call implementations for Object and Class

.. _release-0.2.1:

0.2.1
-----

Kudos to `serenees <https://github.com/serenees>`_ for fixing these issues:

* Fixed an issue where ``Line.split_line`` would return incorrect results if the input string started with the provided separator.
* Added *".subannotation"* token verification
* Added support to handle unnamed *".param"* declarations
* Changed exception descriptor of *".catchall"* to ``Ljava/lang/Exception;`` for all cases


.. _release-0.2.0:

0.2.0
=====

This minor update includes a new smali type system and removes the ``SmaliValueProxy``. The following changes were made:

* Removed the class ``SmaliValueProxy`` completely, the method ``smali_value`` now returns one of: int, float, str, SVMType, bool
* New classes :class:`SVMType` and :class:`Signature` to represent smali types:

    .. code-block:: python
        :caption: Some usage examples
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

.. _release-0.1.3:

0.1.3
=====

* Fixed an issue in :class:`SmaliReader` that causes it to run into infinite loops (kudos to `metalcorpe <https://github.com/metalcorpe>`_)
* Moved to Github-Pages instead of ReadTheDocs
* Added the field ``parent`` to an execution :class:`Frame` to enable backtracking of call stacks
* Some issues around :class:`Type` and :class:`SmaliValueProxy` fixed

.. _release-0.1.2:

0.1.2
=====

* :class:`SmaliVM` is now able to use customized executors.

    .. note::
        The default class loader won't throw any exception upon unknown by default. You
        can change this behaviour by setting the ``use_strict`` attribute to ``True``:

        .. code-block:: python

            vm = SmaliVM(use_strict=True)

* Code was formatted properly
* Documentation update


.. _release-0.1.1:

0.1.1
=====

* ISmali (interactive Smali shell) pre-release
* Implementation of almost half of all Smali-opcodes
* Fixed an error of :class:`SmaliValueProxy` that caused exceptions on operations with an object of the same class
* Multiple bug fixes in the process of class definition (import)

.. _release-1.0.0:

0.0.1
=====

* Start keeping changelog :)
* Documentation on Smali language
* Smali parser implementation (line-based)
* Small Smali-VM
