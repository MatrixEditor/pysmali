.. _smali_reader_api:

*******************
Smali Reader API
*******************

.. automodule:: smali.reader

The parsing model is rather simple and will be described in the
following chapter.

.. note::
    Please note that no optimization is done by default, so methods or fields
    that won't be visited by a :class:`SmaliWriter` won't be covered and won't be
    visible in the final file.

To copy non-visited structures, just add the reader variable to the
:class:`SmaliWriter` when creating a new one:

.. code-block:: python
    :linenos:

    reader = SmaliReader(...)
    writer = SmaliWriter(reader)

    reader.visit(source_code, writer)

.. hint::
    You can add your own *copy_handler* to the reader instance if you want
    to use your own callback to copy raw lines.


Parsing model
=============

Parsing is done by inspecting each line as a possible input. Although, some
statements consume more than one line, only one line per statement is used.

Speaking of statements, they can be devided into groups:

- Token:

    Statements begin with a leading ``.`` and can open a new statement block.
    They are specified in the :class:`Token` class described in :ref:`Token-class`

- Invocation blocks:

    Block statements used within method declarations start with a ``:`` and
    just specify the block's id.

- Annotation values:

    Annotation values don't have a leading identifier and will only be parsed
    within ``.annotation`` or ``.subannotation`` statements.

- Method instructions:

    Same goes with method instructions - they will be handled only if a method
    context is present.

.. autoclass:: smali.reader.SupportsCopy
    :members:

.. autoclass:: smali.reader.SmaliReader
    :members:


