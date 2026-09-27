quantplus Documentation
=======================

``quantplus`` is a compact numerical-finance package for option pricing.
It implements the Cox-Ross-Rubinstein (CRR) binomial tree model, provides a
closed-form Black-Scholes benchmark, and exposes the pricing logic to Python via
Cython bindings around a native C++ core.

The project is intentionally small and focused: pricing functions are exposed at
the top level, the numerical implementation lives in the C++ core, and Python is
used as the ergonomic interface for users and tests.

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
   architecture
   finance
   examples
   api
   development
   min_versions
   release-history

The project is designed to be easy to install, quick to use, and transparent in
how the numerical code is structured. The next sections walk through installation,
usage patterns, the technical implementation, and the versioning policy.
