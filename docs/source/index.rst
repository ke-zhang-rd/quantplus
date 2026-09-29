Introduction
============


Python package wrapping a C++ implementation of the Cox-Ross-Rubinstein (CRR) with
probability truncation as mentioned in the `Cass Sunstein paper <https://chicagounbound.uchicago.edu/cgi/viewcontent.cgi?article=1384&context=law_and_economics>`_


Probability truncation restricts the distribution bounds of an event of variable, which is stock price in this case. The
truncation is done by setting upper and lower thresholds for the stock price at expiry
or entire tree.

Source code could be found `here <https://github.com/ke-zhang-rd/quantplus>`_.

Interactive pricing
-------------------

Drag the red and green bars to set the upper and lower stock-price
thresholds at expiry.

.. raw:: html

   <iframe src="_static/crr_thresholds.html"
           width="100%" height="640"
           style="border:1px solid #ccc; border-radius:4px;"></iframe>



Overview
--------

The package supports:

- European and American option pricing
- CRR lattice calculations with adjustable step counts
- Black-Scholes pricing as a benchmark
- access to terminal node information for inspection and plotting

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
    )

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
