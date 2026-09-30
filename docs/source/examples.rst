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
-------------------------------

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
----------------------------

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

Pricing with stock-price thresholds
-----------------------------------

Use ``S_lower`` and ``S_upper`` to keep only paths that can reach an allowed
terminal stock-price range. The defaults apply the band at expiry; setting
``every_step=True`` also prunes intermediate nodes outside it.

.. code-block:: python

    import quantplus as qp

    parameters = dict(
        S0=100.0, K=100.0, r=0.05, sigma=0.20, T=1.0, N=200, q=0.01
    )
    expiry_only = qp.crr_price(
        **parameters,
        is_call=True,
        american=True,
        S_lower=80.0,
        S_upper=120.0,
    )
    every_step = qp.crr_price(
        **parameters,
        is_call=True,
        american=True,
        S_lower=80.0,
        S_upper=120.0,
        every_step=True,
    )

    print(f"Expiry-only thresholds: {expiry_only:.4f}")
    print(f"Every-step thresholds:  {every_step:.4f}")

Reversed bounds or bounds that leave no terminal path reachable from the root
raise ``ValueError``. If a node has one surviving child, that child receives the
remaining transition probability.

Interactive threshold plot
--------------------------

The plot below is exported from the Matplotlib figure with ``mpld3``. It is a
standalone HTML file with browser-side pan and zoom. The Python drag callbacks
and checkbox are not transferred by mpld3. To adjust the thresholds and
reprice the tree, call ``plot_crr_tree`` in a live Matplotlib session.

.. code-block:: python

    fig, ax = qp.plot_crr_tree(
        **parameters,
        is_call=True,
        american=True,
        S_lower=80.0,
        S_upper=120.0,
        every_step=False,
    )

``plot_crr_tree`` returns a Matplotlib ``(figure, axes)`` pair. Use
``show=False`` to create the plot without calling ``plt.show()``. Matplotlib is
loaded lazily by the plotting function.

.. raw:: html

    <iframe src="_static/crr_thresholds_mpld3.html"
            title="mpld3 CRR threshold plot" width="100%" height="760"
            loading="lazy" style="border: 1px solid #ccc;"></iframe>
