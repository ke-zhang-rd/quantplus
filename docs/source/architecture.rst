============
Architecture
============

``quantplus`` is intentionally small and modular. The project separates the
public Python API from the performance-critical numerical implementation so that
users interact with a clean interface while the expensive work runs in compiled
code.

High-level layout
-----------------

.. code-block:: text

    quantplus/
    ├── __init__.py              # public exports
    ├── _crr_pricer.pyx          # Cython bridge to native C++
    ├── csrc/
    │   ├── crr_core.cpp         # CRR and Black-Scholes math
    │   └── crr_core.h           # C interface declarations
    └── tests/
        └── test_quantplus.py    # regression and validation tests

Public Python API
------------------

The package user interface lives in ``quantplus/__init__.py``. This file imports
and re-exports the functions that are intended for normal use:

- ``crr_price``
- ``black_scholes_price``
- ``crr_tree``

This makes the API easy to discover and keeps the import path simple:

.. code-block:: python

    import quantplus as qp

    price = qp.crr_price(...)

Cython bridge layer
-------------------

The ``_crr_pricer.pyx`` file is a thin wrapper around the compiled C++ core. It
is written in Cython so that Python can call native functions while preserving a
Pythonic API.

This is where the package handles several concerns:

- argument validation
- conversion from Python values to native types
- calling the C++ implementation
- packaging the result back into native Python objects

The bridge is deliberately lightweight. It does not duplicate the numerical logic;
it mostly delegates to the native implementation and enforces sensible input
checks.

Native C++ implementation
-------------------------

The actual model logic is implemented in ``quantplus/csrc/crr_core.cpp``.
It exposes plain C-linkage functions through ``crr_core.h``. The functions are:

- ``crr_price``
- ``black_scholes_price``
- ``crr_price_with_terminal_nodes``

These functions are defined using a simple C ABI so Cython can call them without
relying on C++ name mangling or class-based object models.

This design matters because it keeps the compiled part:

- fast
- easy to call from Cython
- independent of Python object management

Build pipeline
--------------

The package is built through ``setup.py`` and the metadata in ``pyproject.toml``.
The build process does the following:

1. Cython compiles ``_crr_pricer.pyx`` into a Python extension.
2. The native C++ source is compiled and linked into the same extension module.
3. Python imports the resulting ``quantplus._crr_pricer`` extension at runtime.

This hybrid approach is common in numerical libraries: Python handles the public
interface and automation, while the inner loop runs in compiled code.

Why this architecture works well
--------------------------------

The package stays easy to understand because each layer has a clear responsibility:

- Python: user-facing API and validation
- Cython: interop glue and conversion
- C++: performance-critical option-pricing logic
- tests: numerical correctness and regression protection

This separation keeps the code readable while still giving the package the speed of
native execution for repeated computations and lattice evaluations.
