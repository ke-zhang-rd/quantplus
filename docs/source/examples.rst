========
Examples
========

This page shows a few representative ways to use ``quantplus`` in practice.

European call valuation
-----------------------

.. code-block:: python

    import quantplus as qp

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

    print(f"European call price: {price:.6f}")

European put valuation
----------------------

.. code-block:: python

    import quantplus as qp

    put_price = qp.crr_price(
        S0=95.0,
        K=100.0,
        r=0.04,
        sigma=0.25,
        T=2.0,
        N=500,
        q=0.02,
        is_call=False,
        american=False,
    )

    print(f"European put price: {put_price:.6f}")

American option valuation
-------------------------

.. code-block:: python

    import quantplus as qp

    american_put = qp.crr_price(
        S0=90.0,
        K=100.0,
        r=0.03,
        sigma=0.30,
        T=1.5,
        N=300,
        q=0.0,
        is_call=False,
        american=True,
    )

    print(f"American put price: {american_put:.6f}")

Comparing CRR and Black-Scholes
------------------------------

.. code-block:: python

    import quantplus as qp

    s0, k, r, sigma, t, q = 100.0, 100.0, 0.05, 0.20, 1.0, 0.01

    crr_value = qp.crr_price(
        S0=s0,
        K=k,
        r=r,
        sigma=sigma,
        T=t,
        N=500,
        q=q,
        is_call=True,
        american=False,
    )

    bs_value = qp.black_scholes_price(
        S0=s0,
        K=k,
        r=r,
        sigma=sigma,
        T=t,
        q=q,
        is_call=True,
    )

    print(f"CRR price: {crr_value:.6f}")
    print(f"Black-Scholes price: {bs_value:.6f}")

Inspecting the terminal tree
---------------------------

The ``crr_tree`` function is useful when you want to inspect the terminal node
values or build custom visualizations.

.. code-block:: python

    import quantplus as qp

    root, stock_prices, payoffs = qp.crr_tree(
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
    print(stock_prices)
    print(payoffs)

This pattern is especially useful when you are debugging the model or comparing
values across a lattice.

Running a small sensitivity check
---------------------------------

.. code-block:: python

    import quantplus as qp

    params = dict(S0=100.0, K=100.0, r=0.05, T=1.0, N=200, q=0.01)

    for sigma in [0.10, 0.20, 0.30, 0.40]:
        price = qp.crr_price(sigma=sigma, is_call=True, **params)
        print(f"sigma={sigma:.2f}, price={price:.6f}")

As volatility increases, option prices generally increase for standard long
positions, which is consistent with the intuition behind the model.
