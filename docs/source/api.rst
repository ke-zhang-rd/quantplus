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

.. autofunction:: quantplus.plot_crr_tree

CRR threshold parameters
------------------------

``crr_price`` accepts two optional inclusive stock-price bounds:

- ``S_lower``: lowest stock price to retain; ``None`` leaves the lower side unbounded.
- ``S_upper``: highest stock price to retain; ``None`` leaves the upper side unbounded.
- ``every_step``: when false (default), bounds apply to terminal nodes and earlier
    nodes are retained if they can reach a terminal node in range. When true, a node
    must also be inside the band at every step.

At a surviving node with only one surviving child, that child receives all of the
remaining transition probability. Reversed bounds and bands with no surviving
terminal path raise ``ValueError``.

The interactive plot is opened with ``plot_crr_tree``. It provides draggable
threshold lines and a checkbox for switching ``every_step`` while displaying the
bounded price and the corresponding unbounded price. ``matplotlib`` is imported
only when the plotting function is called.

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
- ``plot_crr_tree`` displays an interactive tree and recalculates a bounded price
    as its thresholds move.

The package may evolve over time, but the public interface remains intentionally
stable and easy to inspect.
