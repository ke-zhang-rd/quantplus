=====
Usage
=====

``quantplus`` is designed around a straightforward numerical-finance workflow:
price an option using a CRR binomial lattice, compare the result against the
Black-Scholes closed form, and inspect tree values when needed for debugging or
visualization.

The package is intentionally small and exposes a few top-level functions:

- :func:`quantplus.crr_price` for CRR option pricing
- :func:`quantplus.black_scholes_price` for the benchmark formula
- :func:`quantplus.crr_tree` for examining terminal stock prices and payoffs
- :func:`quantplus.plot_crr_tree` for an interactive thresholded tree view

Importing the package
---------------------

.. code-block:: python

    import quantplus as qp

This is the standard import pattern used in the examples below.

How the package is organized
----------------------------

The source tree is organized as follows:

.. code-block:: text

    quantplus/
    ├── __init__.py
    ├── _crr_pricer.pyx
    ├── plotting.py
    ├── csrc/
    │   ├── crr_core.cpp
    │   └── crr_core.h
    └── tests/
        └── test_quantplus.py

A few important points:

- ``quantplus/__init__.py`` re-exports the public Python functions.
- ``quantplus/_crr_pricer.pyx`` is the Cython bridge between Python and native
  C++ code.
- ``quantplus/plotting.py`` provides the optional interactive Matplotlib view.
- ``quantplus/csrc/crr_core.cpp`` contains the numerical implementation for the
  CRR and Black-Scholes pricing logic.
- ``quantplus/tests/test_quantplus.py`` contains regression and validation tests.

This split is useful because Python is best for ergonomics and API design, while
C++ is excellent for performance-sensitive root-finding, loops, and lattice
operations.

CRR option pricing
------------------

The core function is :func:`quantplus.crr_price`. It values a European or
American option by building a binomial tree and recursively evaluating the value
at each node.

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
        american=False,
    )

    print(price)

Parameter meaning
~~~~~~~~~~~~~~~~~

- ``S0``: current underlying price
- ``K``: strike price
- ``r``: continuously compounded risk-free rate
- ``sigma``: volatility
- ``T``: time to maturity in years
- ``N``: number of time steps in the CRR tree
- ``q``: dividend yield or cost-of-carry adjustment
- ``is_call``: ``True`` for a call, ``False`` for a put
- ``american``: ``True`` for American exercise, ``False`` for European exercise

The implementation validates common edge cases such as non-positive time to
maturity, non-positive step counts, and negative volatility.

Threshold-pruned pricing
------------------------

The CRR pricer can restrict the tree to an inclusive stock-price band. Bounds
apply to expiry nodes by default. With ``every_step=True``, intermediate nodes
outside the band are also pruned. Earlier nodes are considered alive only when
they can reach an allowed terminal node (and, in every-step mode, are themselves
inside the band).

.. code-block:: python

    bounded_call = qp.crr_price(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=200,
        q=0.01,
        is_call=True,
        american=True,
        S_lower=80.0,
        S_upper=120.0,
        every_step=False,
    )

    every_step_call = qp.crr_price(
        S0=100.0, K=100.0, r=0.05, sigma=0.20, T=1.0, N=200,
        q=0.01, is_call=True, american=True,
        S_lower=80.0, S_upper=120.0, every_step=True,
    )

When both child nodes survive, the usual risk-neutral probabilities are used.
When only one child survives, it receives the remaining probability. Bounds that
are reversed or leave no terminal node reachable from the root raise
``ValueError``.

European vs American options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The difference between European and American exercise is controlled by the
``american`` flag.

.. code-block:: python

    european_call = qp.crr_price(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=200,
        q=0.01,
        is_call=True,
        american=False,
    )

    american_call = qp.crr_price(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=200,
        q=0.01,
        is_call=True,
        american=True,
    )

    print(european_call)
    print(american_call)

American options are at least as valuable as their European counterparts because
exercising early is a right, not an obligation.

Black-Scholes benchmark
-----------------------

For closed-form comparison, use :func:`quantplus.black_scholes_price`.
This implements the standard Black-Scholes-Merton formula and is often used to
check whether the CRR price converges as the lattice becomes finer.

.. code-block:: python

    bs_price = qp.black_scholes_price(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        q=0.01,
        is_call=True,
    )

    print(bs_price)

Interesting fact: as ``N`` becomes large, the CRR binomial price approaches the
Black-Scholes value. This makes the CRR model intuitive and also gives a useful
sanity check during testing.

Inspecting the tree
-------------------

The :func:`quantplus.crr_tree` helper returns the root price, the terminal stock
values, and the terminal option values for the lattice. This is useful for
debugging, plotting, or understanding how the payoff evolves across the tree.

.. code-block:: python

    root, stocks, values = qp.crr_tree(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=5,
        q=0.01,
        is_call=True,
    )

    print(root)
    print(stocks)
    print(values)

The call returns three items:

- ``root``: the option value at the tree root
- ``stocks``: the terminal stock prices at maturity
- ``values``: the terminal option payoffs at maturity

Interactive tree plot
----------------------

Use :func:`quantplus.plot_crr_tree` to visualize the lattice and adjust the
thresholds interactively. The red and green bars set the upper and lower bounds;
the checkbox switches between expiry-only and every-step filtering.

.. code-block:: python

    fig, ax = qp.plot_crr_tree(
        S0=100.0,
        K=100.0,
        r=0.05,
        sigma=0.20,
        T=1.0,
        N=30,
        q=0.01,
        is_call=True,
        american=True,
        S_lower=80.0,
        S_upper=120.0,
        show=True,
    )

The function returns the Matplotlib ``(figure, axes)`` pair. Set ``show=False``
to construct the figure without starting the GUI event loop. Matplotlib is needed
only when this plotting function is called.

Example: put option pricing
---------------------------

.. code-block:: python

    put_price = qp.crr_price(
        S0=90.0,
        K=100.0,
        r=0.03,
        sigma=0.25,
        T=2.0,
        N=500,
        q=0.00,
        is_call=False,
        american=False,
    )

    print(f"European put price: {put_price:.4f}")

C++ and Python working together
-------------------------------

The package is a good example of a hybrid numerical library:

1. Python defines the public API and validation logic.
2. The Cython bridge exposes a low-level extension module.
3. The native C++ implementation performs the numerical calculations.
4. The compiled extension is loaded by Python at import time.

The C++ layer is compiled as part of the extension module using ``setup.py`` and
Cython. This allows the runtime to call the C++ pricing functions directly while
keeping the end-user experience simple and Pythonic.

The performance benefit is especially noticeable in repeated lattice calculations,
where the hot loop is executed in compiled C++ rather than pure Python.
