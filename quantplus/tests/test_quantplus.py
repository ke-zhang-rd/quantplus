"""
Tests for quantplus.

Regression values (e.g. test_matches_verified_reference_value) are
pinned to numbers independently computed with a pure-Python reference
implementation earlier in this project's development and cross-checked
against the ctypes build of the same C++ core -- both agreed to full
double precision before this Cython binding was written. If you change
crr_core.cpp's math, these are the numbers that should catch it.
"""

import math

import pytest

import quantplus as qp

# Shared "NVDA-style" scenario used throughout: S0=225, K=240,
# r=4.25%, sigma=40%, T=55 calendar days, q=0.45% dividend yield.
S0, K, R, SIGMA, T, Q = 225.0, 240.0, 0.0425, 0.40, 55 / 365, 0.0045


class TestCRRPrice:
    def test_matches_verified_reference_value(self):
        # Cross-checked earlier against an independent pure-Python
        # implementation and a ctypes build of the same C++ core.
        price = qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=2, q=Q)
        assert price == pytest.approx(9.431487, abs=1e-5)

    def test_converges_to_black_scholes_as_n_grows(self):
        bs = qp.black_scholes_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, q=Q)
        price_small_n = qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=2, q=Q)
        price_large_n = qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=2000, q=Q)

        assert abs(price_large_n - bs) < abs(price_small_n - bs)
        assert price_large_n == pytest.approx(bs, abs=0.01)

    def test_put_call_parity(self):
        # C - P = S0*e^(-qT) - K*e^(-rT), which must hold for European
        # options regardless of the pricing method.
        call = qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=500, q=Q, is_call=True)
        put = qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=500, q=Q, is_call=False)

        lhs = call - put
        rhs = S0 * math.exp(-Q * T) - K * math.exp(-R * T)
        assert lhs == pytest.approx(rhs, abs=1e-6)

    def test_american_put_at_least_as_valuable_as_european(self):
        # Early exercise is only ever a right, never an obligation, so
        # an American option can never be worth less than its European
        # counterpart under the same parameters.
        european = qp.crr_price(
            S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=200, q=Q, is_call=False, american=False
        )
        american = qp.crr_price(
            S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=200, q=Q, is_call=False, american=True
        )
        assert american >= european - 1e-12

    def test_deep_out_of_the_money_call_is_worth_near_zero(self):
        price = qp.crr_price(S0=100.0, K=10_000.0, r=R, sigma=SIGMA, T=T, N=100)
        assert price == pytest.approx(0.0, abs=1e-6)

    def test_call_price_is_monotonically_increasing_in_volatility(self):
        low_vol = qp.crr_price(S0=S0, K=K, r=R, sigma=0.20, T=T, N=200)
        high_vol = qp.crr_price(S0=S0, K=K, r=R, sigma=0.60, T=T, N=200)
        assert high_vol > low_vol

    @pytest.mark.parametrize("bad_n", [0, -1, -100])
    def test_raises_on_non_positive_steps(self, bad_n):
        with pytest.raises(ValueError):
            qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=bad_n)

    def test_raises_on_non_positive_expiry(self):
        with pytest.raises(ValueError):
            qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=0.0, N=10)

    def test_raises_on_negative_volatility(self):
        with pytest.raises(ValueError):
            qp.crr_price(S0=S0, K=K, r=R, sigma=-0.1, T=T, N=10)


class TestCRRTree:
    def test_terminal_nodes_length_matches_n_plus_one(self):
        _, stocks, values = qp.crr_tree(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=5, q=Q)
        assert len(stocks) == 6
        assert len(values) == 6

    def test_root_price_matches_crr_price(self):
        root, _, _ = qp.crr_tree(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=50, q=Q)
        direct = qp.crr_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=50, q=Q)
        assert root == pytest.approx(direct, abs=1e-10)

    def test_terminal_payoffs_are_non_negative(self):
        _, _, values = qp.crr_tree(S0=S0, K=K, r=R, sigma=SIGMA, T=T, N=20, q=Q)
        assert all(v >= 0 for v in values)


class TestBlackScholes:
    def test_raises_on_non_positive_expiry(self):
        with pytest.raises(ValueError):
            qp.black_scholes_price(S0=S0, K=K, r=R, sigma=SIGMA, T=0.0)

    def test_raises_on_non_positive_volatility(self):
        with pytest.raises(ValueError):
            qp.black_scholes_price(S0=S0, K=K, r=R, sigma=0.0, T=T)

    def test_matches_verified_reference_value(self):
        bs = qp.black_scholes_price(S0=S0, K=K, r=R, sigma=SIGMA, T=T, q=Q)
        assert bs == pytest.approx(8.539182, abs=1e-5)
