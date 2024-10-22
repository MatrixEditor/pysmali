# PySmali

[![python](https://img.shields.io/badge/python-3.9+-blue.svg?logo=python&labelColor=lightgrey)](https://www.python.org/downloads/)
![Status](https://img.shields.io:/static/v1?label=Status&message=Pre-Release&color=teal)
![Platform](https://img.shields.io:/static/v1?label=Platforms&message=Linux|Windows&color=lightgrey)
[![Build and Deploy Sphinx Documentation](https://github.com/MatrixEditor/pysmali/actions/workflows/sphinx.yml/badge.svg)](https://github.com/MatrixEditor/pysmali/actions/workflows/sphinx.yml)
[![PyPI](https://img.shields.io/pypi/v/pysmali)](https://pypi.org/project/pysmali/)


The main functionalities of this repository cover creating and parsing Smali files with Python3 as well as interpret Smali source code files. There is also an interactive interpreter provided that acts as a Python-CLI.

### Contributors

[![TheZ3ro](https://img.shields.io:/static/v1?label=Fixer&message=TheZ3ro)](https://github.com/TheZ3ro)
[![serenees](https://img.shields.io:/static/v1?label=Patcher&message=serenees)](https://github.com/serenees)
[![metalcorpe](https://img.shields.io:/static/v1?label=Patcher&message=metalcorpe)](https://github.com/metalcorpe)


## Installation

By now, the only way to install the python module in this repository is by cloning it and running the following command:

```bash
$ cd ./pysmali && pip install .
# Or with pip
$ pip install pysmali
```

## Usage

For a more detailed explanation of the Smali Visitor-API use the [Github-Pages Docs](https://matrixeditor.github.io/pysmali/).

> **Info**: Make sure you are using ``pysmali>=0.2.0`` as it introduces a user-friendly type system to mitigate possible issues from parsing type descriptors.

### ISmali (Interactive Smali Interpreter)

As of version `0.1.2` the interactive interpreter can be used to execute Smali code directly:

```bash
$ ismali example.ssf
# or start interactive mode
$ ismali
>>> vars
{'p0': <SmaliObject@195f5c0da90>}
```

Some notes:

* ``p0``: This register always stores the root-instance where defined fields and methods will be stored.
* ``vars``: This command can be used to print all registers together with their values
* `L<Root>;`: The name of the root-context class

The API [documentation](https://matrixeditor.github.io/pysmali/) provides some usage examples and usage hints.

### Parsing Smali-Files

The simplest way to parse code is to use a `SmaliReader` together with a visitor:

```python
from smali import SmaliReader, ClassVisitor

code = """
.class public final Lcom/example/Hello;
.super Ljava/lang/Object;
# One line comment
.source "SourceFile" # EOL comment
"""

reader = SmaliReader()
reader.visit(code, ClassVisitor())
```

There are a few options to have in mind when parsing with a `SmaliReader`:

* `comments`: To explicitly parse comments, set this variable to True (in constructor or directly)
* `snippet`: To parse simple code snippets without a .class definition, use the 'snippet' variable (or within the constructor). Use this property only if you don't have a '.class' definition at the start of the source code
* `validate`: Validates the parsed code
* `errors`: With values `"strict"` or `"ignore"` this attribute will cause the reader to raise or ignore exceptions

Actually, the code above does nothing as the `ClassVisitor` class does not handle any notification by the reader. For instance, to print out the class name of a parsed code, the following implementation could be used:

```python
from smali import SmaliReader, ClassVisitor, SVMType

class NamePrinterVisitor(ClassVisitor):
    def visit_class(self, name: str, access_flags: int) -> None:
        # The provided name is the type descriptor, so we have to
        # convert it:
        cls_type = SVMType(name)
        print('Class:', cls_type.pretty_name) # prints: com.example.Hello

reader = SmaliReader()
reader.visit(".class public final Lcom/example/Hello;", NamePrinterVisitor())
```

> [!TIP]
> There is an example Smali file in this repository. If you want to print out **all**
> defined classes, you have to implement another method (based on the example above):
> ```python
> class NamePrinterVisitor(ClassVisitor):
>   # ... method from above does not change
>   def visit_inner_class(self, name: str, access_flags: int) -> ClassVisitor:
>        cls_type = SVMType(name) # same as above
>        print("Inner Class:", cls_type.pretty_name)
>        return self
> ```

### Writing Smali-Files

Writing is as simple as parsing files. To write the exact same document the has been parsed, the `SmaliWriter` class can be used as the visitor:

```python
from smali import SmaliReader, SmaliWriter

reader = SmaliReader()
writer = SmaliWriter()

reader.visit(".class public final Lcom/example/Hello;", writer)
# The source code can be retrieved via a property
text = writer.code
```

To create own Smali files, the pre-defined `SmaliWriter` can be used again:

```python
from smali import SmaliWriter, AccessType

writer = SmaliWriter()
# create the class definition
writer.visit_class("Lcom/example/Hello;", AccessType.PUBLIC + AccessType.FINAL)
writer.visit_super("Ljava/lang/Object;")

# create a field
field_writer = writer.visit_field("foo", AccessType.PRIVATE, "Ljava/lang/String")

# create the finished source code, BUT don't forget visit_end()
writer.visit_end()
text = writer.code
```

### Importing classes and execute methods

As of version `0.1.2` you can import Smali files and execute defined methods:

```python
from smali.bridge import SmaliVM, SmaliObject

vm = SmaliVM()
# Import class definition
with open('example.smali', 'r', encoding='utf-8') as fp:
    smali_class = vm.classloader.load_class(fp, init=False)
# Call <clinit> method
smali_class.clinit()

# Create a new instance of the imported class
instance = SmaliObject(smali_class)
# Call the object's constructor
instance.init()

# Execute the method 'toString'
toString = instance.smali_class.method("toString")
# The instance must be always the first element (on
# static methods this argument must be None)
value = toString(instance)
print(value)
```



## License

Distributed under the GNU GPLv3. See `LICENSE` for more information.
