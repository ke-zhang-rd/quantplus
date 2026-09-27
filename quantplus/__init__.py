"""
quantplus: Cox-Ross-Rubinstein binomial option pricer.

The pricing math is implemented in C++ (quantplus/csrc/crr_core.cpp)
and compiled directly into a native Python extension module via
Cython (quantplus/_crr_pricer.pyx).

Example
-------
>>> import quantplus as qp
>>> qp.crr_price(S0=225, K=240, r=0.0425, sigma=0.40, T=55/365, N=1000, q=0.0045)
8.542142620861936
"""

from ._crr_pricer import black_scholes_price, crr_price, crr_tree

try:
    # Generated at build time by setuptools_scm from the nearest git tag.
    # See pyproject.toml's [tool.setuptools_scm] section.
    from ._version import version as __version__
except ImportError:  # pragma: no cover - only hit in an unbuilt source tree
    __version__ = "0+unknown"

__all__ = ["crr_price", "black_scholes_price", "crr_tree", "__version__"]
