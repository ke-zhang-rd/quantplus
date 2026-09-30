============
Installation
============

``quantplus`` is a Python package with a compiled extension, so installation
requires both Python dependencies and a working C++ toolchain for the native
module build.

Install from PyPI
-----------------

The package can be installed from the Python Package Index with:

.. code-block:: bash

    pip install quantplus


Install with uv
---------------

For a project managed by `uv <https://docs.astral.sh/uv/>`__, add ``quantplus``
as a dependency and run Python through uv:

.. code-block:: bash

    uv add quantplus

To install the current checkout in editable mode, run this from the repository
root:

.. code-block:: bash

    uv pip install -e .

As with pip, installing from source builds the Cython/C++ extension and requires
a working C++ compiler.
