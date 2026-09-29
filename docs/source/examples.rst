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
---------------------------

The interactive helper displays the tree, grays out pruned nodes, and updates
the bounded price as the threshold bars move. Its checkbox toggles every-step
pruning.

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

.. plot::
    :caption: Terminal call and put payoffs at the stock-price nodes returned by ``crr_tree``.

    import matplotlib.pyplot as plt
    import quantplus as qp

    parameters = dict(S0=100.0, K=100.0, r=0.05, sigma=0.20, T=1.0, N=8, q=0.01)
    _, call_stocks, call_payoffs = qp.crr_tree(**parameters, is_call=True)
    _, put_stocks, put_payoffs = qp.crr_tree(**parameters, is_call=False)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(call_stocks, call_payoffs, color="#147d78", s=42, label="Call")
    ax.scatter(put_stocks, put_payoffs, color="#c05a36", s=42, label="Put")
    ax.axvline(parameters["K"], color="#667780", linestyle="--", linewidth=1,
                  label="Strike")
    ax.set_xlabel("Stock price at expiry")
    ax.set_ylabel("Option payoff at expiry")
    ax.set_title("Terminal payoffs on the CRR lattice")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()

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
