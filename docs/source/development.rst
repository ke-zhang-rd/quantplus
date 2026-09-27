===========
Development
===========

This project is small enough that development remains lightweight, but it still
benefits from a clear workflow for building, testing, and documenting the package.

Recommended environment
------------------------

Use a virtual environment for local development:

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -U pip
    python -m pip install -r requirements-dev.txt

Then install the project itself in editable mode:

.. code-block:: bash

    python -m pip install -e .

This allows changes to the Python files and compiled extension to be picked up
without reinstalling the package repeatedly.

Running tests
-------------

The project uses ``pytest`` for regression and validation testing. Run the suite
with:

.. code-block:: bash

    pytest

This checks the pricing functions against known values and ensures that numerical
behavior stays consistent after changes.

Building the extension
----------------------

The package compiles the native C++ and Cython extension as part of installation.
If you want to trigger a fresh build manually, use:

.. code-block:: bash

    python setup.py build_ext --inplace

This builds the extension in place so it can be imported directly from the source
checkout during testing and debugging.

Building the docs
-----------------

The documentation is built with Sphinx. From the project root, run:

.. code-block:: bash

    python -m sphinx -b html docs/source docs/build/html

This creates a local HTML build that can be reviewed in the browser.

Project conventions
-------------------

A few conventions help keep the package maintainable:

- keep the public API small and deliberate
- prefer simple, explicit function signatures
- validate common inputs early
- add regression tests when changing pricing math
- document numerical assumptions and edge cases clearly

When the pricing logic is modified, it is important to validate the change against
known examples and the existing test suite.

Contribution workflow
--------------------

A typical contribution flow looks like this:

1. create a feature branch
2. make a focused change
3. add or update tests
4. run the relevant test subset
5. update documentation if behavior or usage changes
6. submit a pull request with a clear summary

This keeps the project coherent and makes it easier to review numerical changes
that may affect pricing outcomes.
