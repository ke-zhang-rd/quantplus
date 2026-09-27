===
API
===

This page summarizes the public API exposed by the package.

Top-level functions
-------------------

The package exports the following functions at the top level:

.. autofunction:: quantplus.crr_price

.. autofunction:: quantplus.black_scholes_price

.. autofunction:: quantplus.crr_tree

Module overview
---------------

The public package is intentionally lightweight and exposes only the functions
that users are expected to call directly. The numerical implementation itself is
kept in the compiled extension and C++ source files.

You can inspect the runtime package directly in Python:

.. code-block:: python

    import quantplus as qp

    print(qp.__all__)
    print(qp.__version__)

This helps developers confirm which functions are part of the supported public
surface.

Other useful considerations
---------------------------

- ``crr_price`` is the main pricing function for binomial-tree valuation.
- ``black_scholes_price`` is the analytic benchmark for comparison.
- ``crr_tree`` is useful when you want the tree terminal nodes or payoffs.

The package may evolve over time, but the public interface remains intentionally
stable and easy to inspect.
