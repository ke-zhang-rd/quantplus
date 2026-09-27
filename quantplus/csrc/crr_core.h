#ifndef CRR_CORE_H
#define CRR_CORE_H

// Plain C-linkage declarations for the CRR / Black-Scholes core in
// crr_core.cpp. This header is what Cython's `cdef extern from` reads
// to know the function signatures at compile time -- the actual
// implementation is still C++ underneath (see crr_core.cpp), only the
// call boundary is a plain C ABI.

extern "C" {

double crr_price(double S0, double K, double r, double q, double sigma,
                  double T, int N, int isCall, int american);

double black_scholes_price(double S0, double K, double r, double q,
                            double sigma, double T, int isCall);

double crr_price_with_terminal_nodes(double S0, double K, double r, double q,
                                      double sigma, double T, int N,
                                      int isCall, int american,
                                      double* out_stock, double* out_value);

}

#endif // CRR_CORE_H
