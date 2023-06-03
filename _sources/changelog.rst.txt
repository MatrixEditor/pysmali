.. _changelog:

*********
Changelog
*********

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
