.. _changelog:

*********
Changelog
*********

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
