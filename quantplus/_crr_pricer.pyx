# distutils: language = c++
# cython: language_level=3
"""
_crr_pricer.pyx

Cython layer between Python and the C++ CRR core (crr_core.cpp).
Compiled by setup.py into quantplus._crr_pricer, a native extension
module. quantplus/__init__.py re-exports the functions defined here
so users just do `import quantplus as qp`.
"""

from libc.stdlib cimport malloc, free

# ---------------------------------------------------------------------
# Declare the C++ (extern "C") functions from crr_core.h. The names on
# the right of each line ("crr_price", etc.) must match crr_core.h
# exactly; the names on the left (c_crr_price, etc.) are just how this
# .pyx file refers to them, renamed so they don't collide with the
# Python-level wrapper functions of (almost) the same name below.
# ---------------------------------------------------------------------
cdef extern from "csrc/crr_core.h":
    double c_crr_price "crr_price"(
        double S0, double K, double r, double q, double sigma,
        double T, int N, int isCall, int american,
        double S_upper, double S_lower, int everyStep)

    double c_black_scholes_price "black_scholes_price"(
        double S0, double K, double r, double q, double sigma,
        double T, int isCall)

    double c_crr_price_with_terminal_nodes "crr_price_with_terminal_nodes"(
        double S0, double K, double r, double q, double sigma,
        double T, int N, int isCall, int american,
        double* out_stock, double* out_value)


def crr_price(double S0, double K, double r, double sigma, double T, int N,
              double q=0.0, bint is_call=True, bint american=False,
              S_upper=None, S_lower=None, bint every_step=False):
    """Price a European or American option with the CRR binomial tree.

    Thin, statically-typed wrapper around the C++ core -- the actual
    tree construction and backward induction happen entirely in C++.

    ``S_lower`` and ``S_upper`` are inclusive stock-price thresholds. By
    default, they filter terminal nodes only; with ``every_step=True``, nodes
    outside the band are also pruned at intermediate steps. At a node with
    only one surviving child, that child receives the remaining probability.
    Raises ``ValueError`` when no terminal node is reachable from the root.
    """
    if N <= 0:
        raise ValueError(f"N must be a positive integer, got {N}")
    if T <= 0:
        raise ValueError(f"T must be positive, got {T}")
    if sigma < 0:
        raise ValueError(f"sigma must be non-negative, got {sigma}")

    cdef double upper = float("inf") if S_upper is None else float(S_upper)
    cdef double lower = -float("inf") if S_lower is None else float(S_lower)
    if upper != upper or lower != lower:
        raise ValueError("stock-price thresholds must not be NaN")
    if lower > upper:
        raise ValueError("S_lower must be less than or equal to S_upper")

    cdef double price = c_crr_price(
        S0, K, r, q, sigma, T, N, int(is_call), int(american),
        upper, lower, int(every_step),
    )
    if price != price and (S_upper is not None or S_lower is not None):
        raise ValueError("No path survives inside [S_lower, S_upper]")
    return price


def black_scholes_price(double S0, double K, double r, double sigma,
                         double T, double q=0.0, bint is_call=True):
    """Closed-form Black-Scholes-Merton price (the CRR tree's N -> infinity limit)."""
    if T <= 0:
        raise ValueError(f"T must be positive, got {T}")
    if sigma <= 0:
        raise ValueError(f"sigma must be positive, got {sigma}")

    return c_black_scholes_price(S0, K, r, q, sigma, T, int(is_call))


def crr_tree(double S0, double K, double r, double sigma, double T, int N,
             double q=0.0, bint is_call=True, bint american=False):
    """Like crr_price, but also returns the terminal stock prices and
    option payoffs as Python lists, e.g. for plotting or inspection.

    Returns
    -------
    (root_price, terminal_stock_prices, terminal_option_values)
    """
    if N <= 0:
        raise ValueError(f"N must be a positive integer, got {N}")

    cdef double* stock_arr = <double*> malloc((N + 1) * sizeof(double))
    cdef double* value_arr = <double*> malloc((N + 1) * sizeof(double))
    if stock_arr is NULL or value_arr is NULL:
        if stock_arr is not NULL:
            free(stock_arr)
        if value_arr is not NULL:
            free(value_arr)
        raise MemoryError("Failed to allocate tree buffers")

    cdef double root
    cdef int i
    try:
        root = c_crr_price_with_terminal_nodes(
            S0, K, r, q, sigma, T, N, int(is_call), int(american),
            stock_arr, value_arr,
        )
        stocks = [stock_arr[i] for i in range(N + 1)]
        values = [value_arr[i] for i in range(N + 1)]
    finally:
        free(stock_arr)
        free(value_arr)

    return root, stocks, values
