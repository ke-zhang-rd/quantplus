=====
Usage
=====

``quantplus`` provides fast option-pricing routines built on a Cox-Ross-Rubinstein
(CRR) binomial tree, with a closed-form Black-Scholes benchmark for comparison.

Import the package and call the pricing functions with the standard option inputs.

.. code-block:: python

    import quantplus as qp

Basic CRR pricing
-----------------

The main function is :func:`quantplus.crr_price`, which prices a European or
American option by stepping a binomial lattice.

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

The parameters are:

- ``S0``: spot price of the underlying
- ``K``: strike price
- ``r``: continuously compounded risk-free rate
- ``sigma``: volatility
- ``T``: time to maturity in years
- ``N``: number of time steps in the CRR tree
- ``q``: dividend yield or convenience yield (default ``0.0``)
- ``is_call``: ``True`` for a call option, ``False`` for a put option
- ``american``: ``True`` for American exercise, ``False`` for European exercise

The function validates common inputs, including positive maturity and a positive
number of steps. Negative volatilities are rejected.

Black-Scholes comparison
------------------------

For a closed-form benchmark, use :func:`quantplus.black_scholes_price`.

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

This is useful for checking convergence as the number of CRR steps increases.

Inspecting the tree
-------------------

The :func:`quantplus.crr_tree` helper returns the root price together with the
terminal stock prices and option values for the lattice.

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

This can be helpful for debugging, plotting, or understanding how the option
value evolves across the tree.

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

This is a simple way to value a European put using the CRR model.
