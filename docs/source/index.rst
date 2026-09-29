Introduction
============


Python package wrapping a C++ implementation of the Cox-Ross-Rubinstein (CRR)
binomial option-pricing model, with optional stock-price threshold pruning.

Set inclusive ``S_lower`` and ``S_upper`` bounds to restrict which stock-price
nodes contribute to the valuation. By default, the bounds apply at expiry;
``every_step=True`` also removes nodes outside the band at intermediate steps.
When only one child survives, it receives the remaining transition probability.

Source code could be found `here <https://github.com/ke-zhang-rd/quantplus>`_.

Interactive pricing
-------------------

Drag the red and green bars to set the upper and lower stock-price thresholds.
Use the controls to change the option inputs and choose whether thresholds apply
only at expiry or at every time step.

.. raw:: html

   <iframe src="_static/crr_thresholds.html"
           width="100%" height="640"
           style="border:1px solid #ccc; border-radius:4px;"></iframe>



Overview
--------

The package supports:

- European and American option pricing
- CRR lattice calculations with adjustable step counts
- optional lower and upper stock-price thresholds, applied at expiry or every step
- Black-Scholes pricing as a benchmark
- access to terminal node information for inspection and plotting
- an interactive CRR tree plot with draggable thresholds

The public API is intentionally simple:

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
        S_lower=80.0,
        S_upper=120.0,
    )

    # Set every_step=True to enforce the band at every time step.

Documentation map
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents

   installation
   usage
   examples
   finance
   architecture
   api
   development
   min_versions
   release-history

The project is designed to be easy to install, quick to use, and transparent in
how the numerical code is structured. The next sections walk through installation,
usage patterns, the technical implementation, and the versioning policy.
