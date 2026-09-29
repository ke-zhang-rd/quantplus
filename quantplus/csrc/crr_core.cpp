// crr_core.cpp
//
// Same CRR / Black-Scholes math verified in the ctypes version of this
// package. Exposed through a plain "extern C" interface (no classes,
// no name mangling) so it can be linked against directly from the
// Cython .pyx file via `cdef extern from "crr_core.h"`.
//
// This file is compiled as one of the sources of the Cython extension
// module (see setup.py) -- Cython/setuptools handles invoking the
// compiler, there's no separate manual build step.

#include "crr_core.h"
#include <cmath>
#include <vector>
#include <algorithm>

namespace {

double normCDF(double x) {
    return 0.5 * std::erfc(-x / std::sqrt(2.0));
}

} // namespace

extern "C" {

// Cox-Ross-Rubinstein binomial price.
// isCall: 1 = call, 0 = put. american: 1 = allow early exercise, 0 = European.
// Returns NaN for invalid inputs or when no terminal node survives the bounds.
double crr_price(double S0, double K, double r, double q, double sigma,
                  double T, int N, int isCall, int american,
                  double S_upper, double S_lower, int everyStep) {
    if (N <= 0 || T <= 0.0 || sigma < 0.0) {
        return std::nan("");
    }

    const double dt   = T / N;
    const double u    = std::exp(sigma * std::sqrt(dt));
    const double d    = 1.0 / u;
    const double disc = std::exp(-r * dt);
    const double p    = (std::exp((r - q) * dt) - d) / (u - d);
    const double qn   = 1.0 - p;

    std::vector<double> value(N + 1);
    std::vector<unsigned char> alive(N + 1, 0);
    for (int j = 0; j <= N; ++j) {
        double ST = S0 * std::pow(u, j) * std::pow(d, N - j);
        alive[j] = S_lower <= ST && ST <= S_upper;
        value[j] = alive[j]
            ? (isCall ? std::max(ST - K, 0.0) : std::max(K - ST, 0.0))
            : 0.0;
    }

    for (int i = N - 1; i >= 0; --i) {
        std::vector<unsigned char> currentAlive(i + 1, 0);
        for (int j = 0; j <= i; ++j) {
            const double ST = S0 * std::pow(u, j) * std::pow(d, i - j);
            const bool upAlive = alive[j + 1] != 0;
            const bool downAlive = alive[j] != 0;
            const bool inBand = S_lower <= ST && ST <= S_upper;
            const bool nodeAlive = (upAlive || downAlive) && (!everyStep || inBand);
            currentAlive[j] = nodeAlive;
            if (!nodeAlive) {
                value[j] = 0.0;
                continue;
            }

            double continuation;
            if (upAlive && downAlive) {
                continuation = disc * (p * value[j + 1] + qn * value[j]);
            } else if (upAlive) {
                continuation = disc * value[j + 1];
            } else {
                continuation = disc * value[j];
            }
            if (american) {
                const double exerciseValue = isCall ? std::max(ST - K, 0.0)
                                                     : std::max(K - ST, 0.0);
                value[j] = std::max(continuation, exerciseValue);
            } else {
                value[j] = continuation;
            }
        }
        alive.swap(currentAlive);
    }
    if (!alive[0]) {
        return std::nan("");
    }
    return value[0];
}

// Closed-form Black-Scholes-Merton price (the N -> infinity limit of crr_price).
double black_scholes_price(double S0, double K, double r, double q,
                            double sigma, double T, int isCall) {
    if (T <= 0.0 || sigma <= 0.0) {
        return std::nan("");
    }
    double d1 = (std::log(S0 / K) + (r - q + 0.5 * sigma * sigma) * T) /
                (sigma * std::sqrt(T));
    double d2 = d1 - sigma * std::sqrt(T);

    if (isCall) {
        return S0 * std::exp(-q * T) * normCDF(d1) -
               K  * std::exp(-r * T) * normCDF(d2);
    } else {
        return K  * std::exp(-r * T) * normCDF(-d2) -
               S0 * std::exp(-q * T) * normCDF(-d1);
    }
}

// Fills two caller-allocated arrays (length N+1 each) with the terminal
// stock prices and option values, so Python can inspect/plot the tree
// without re-deriving it. Returns the root price (same as crr_price)
// for convenience.
double crr_price_with_terminal_nodes(double S0, double K, double r, double q,
                                      double sigma, double T, int N,
                                      int isCall, int american,
                                      double* out_stock, double* out_value) {
    const double dt   = T / N;
    const double u    = std::exp(sigma * std::sqrt(dt));
    const double d    = 1.0 / u;
    const double disc = std::exp(-r * dt);
    const double p    = (std::exp((r - q) * dt) - d) / (u - d);
    const double qn   = 1.0 - p;

    std::vector<double> value(N + 1);
    for (int j = 0; j <= N; ++j) {
        double ST = S0 * std::pow(u, j) * std::pow(d, N - j);
        out_stock[j] = ST;
        value[j] = isCall ? std::max(ST - K, 0.0) : std::max(K - ST, 0.0);
        out_value[j] = value[j];
    }

    for (int i = N - 1; i >= 0; --i) {
        for (int j = 0; j <= i; ++j) {
            double continuation = disc * (p * value[j + 1] + qn * value[j]);
            if (american) {
                double ST = S0 * std::pow(u, j) * std::pow(d, i - j);
                double exerciseValue = isCall ? std::max(ST - K, 0.0)
                                               : std::max(K - ST, 0.0);
                value[j] = std::max(continuation, exerciseValue);
            } else {
                value[j] = continuation;
            }
        }
    }
    return value[0];
}

} // extern "C"
