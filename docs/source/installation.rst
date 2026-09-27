============
Installation
============

``quantplus`` is a Python package with a compiled extension, so installation
requires both Python dependencies and a working C++ toolchain for the native
module build.

Requirements
------------

The package targets Python 3.9 or newer and depends on the standard scientific
Python stack used by the project build. At a minimum, you need:

- Python 3.9+
- a C/C++ compiler available on your system
- pip for installing dependencies and the package

On macOS, the Xcode command-line tools are typically required before building a
compiled extension:

.. code-block:: bash

    xcode-select --install

Install from PyPI
-----------------

The package can be installed from the Python Package Index with:

.. code-block:: bash

    pip install quantplus

Install from a local checkout
-----------------------------

If you are working from a source tree, install the project in editable mode:

.. code-block:: bash

    git clone <repository-url>
    cd quantplus
    python -m pip install -U pip
    python -m pip install -e .

This is the recommended approach for development, since it builds the extension
module in place and lets you test changes immediately.

Build requirements for source installs
--------------------------------------

The project uses modern setuptools configuration and compiles the native
extension through Cython and a C++ source file. During installation, the build
system will automatically compile the Cython layer and the native C++ core. If
Cython is missing, the build will stop with a clear message telling you to install
it first.

In a typical development environment, the command below is enough:

.. code-block:: bash

    python -m pip install -r requirements-dev.txt
    python -m pip install -e .

Verification
------------

Once installed, confirm the package imports correctly:

.. code-block:: python

    import quantplus as qp
    print(qp.__version__)

You can then call the public functions, for example:

.. code-block:: python

    price = qp.crr_price(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=200,
        q=0.01,
        is_call=True,
    )

    print(price)

If you see a numerical output rather than an import error, the package has been
built and is ready to use.
