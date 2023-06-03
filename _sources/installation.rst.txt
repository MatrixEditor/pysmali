.. _installation:

============
Installation
============


How to install the package
--------------------------

Install the whole ``pysmali`` package (or add it to your ``requirements.txt`` file):

.. code:: console

    $ pip install pysmali


.. note:: 

    This package comes with one dependency: `Python cryptography <https://github.com/pyca/cryptography/>`_.
    The reason why to use this specific library when decrypting ESA files is that it is actively
    maintained and provides a user-friendly API documentation. These points makes it easier to work
    with the module in future versions.


.. hint::

    In most cases you want to create a virtual environment as it provides extra security features
    when working with packages. To create a simple virtual environment, run:

    .. code-block:: console
        :caption: Linux

        $ python3 -m venv ./venv && source ./venv/bin/activate

    .. code-block:: console
        :caption: Windows

        $ py -m venv ./venv && ./venv/Scripts/activate.bat

