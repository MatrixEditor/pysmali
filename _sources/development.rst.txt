.. _development:

===========
Development
===========

Developers working on ``pysmali`` should consider the following guidelines for developing
and releases. 

.. _supported-dependencies:

Supported dependencies
----------------------

The package supports the following dependencies:

.. list-table:: Supported dependencies
    :header-rows: 1
    :widths: 10, 10

    * - Dependency
      - Versions
    * - Python
      - at least Python 3

Roadmap
-------

Several releases are planned in the development roadmap. Backward
incompatible changes, deprecations, and major features are noted for each of
these releases.

Releases published follow `semantic versioning`_, and so it is recommended that 
dependencies on ``pysmali`` are pinned to a specific version below the next major 
version:

.. _semantic versioning: http://semver.org/


1.0.0
~~~~~

:Planned release date: March 2023

This release should contain the code for a fully qualified Smali source parser, 
as well as a robust implementation on decryption of ESA files.