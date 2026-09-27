"""
example.py -- demonstrates the quantplus package end to end.

Run after installing the package:
    pip install -e .
    python example.py
"""

import quantplus as qp

S0, K, r, sigma, T, q = 225, 240, 0.0425, 0.40, 55 / 365, 0.0045

print("=== Single price ===")
price = qp.crr_price(S0=S0, K=K, r=r, sigma=sigma, T=T, N=1000, q=q)
bs = qp.black_scholes_price(S0=S0, K=K, r=r, sigma=sigma, T=T, q=q)
print(f"CRR (N=1000): {price:.6f}")
print(f"Black-Scholes limit: {bs:.6f}")

print("\n=== Convergence table ===")
print(f"{'N':>6} {'CRR Price':>14} {'Diff vs BS':>14}")
for N in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1000]:
    p = qp.crr_price(S0=S0, K=K, r=r, sigma=sigma, T=T, N=N, q=q)
    print(f"{N:>6} {p:>14.6f} {p - bs:>14.6f}")

print("\n=== Inspecting the tree (N=2) ===")
root, stocks, values = qp.crr_tree(S0=S0, K=K, r=r, sigma=sigma, T=T, N=2, q=q)
print(f"Root price: {root:.6f}")
for s, v in zip(stocks, values):
    print(f"  S_T = {s:>10.4f}   payoff = {v:>10.4f}")

print("\n=== American vs European put ===")
euro_put = qp.crr_price(
    S0=S0, K=K, r=r, sigma=sigma, T=T, N=200, q=q, is_call=False, american=False
)
amer_put = qp.crr_price(S0=S0, K=K, r=r, sigma=sigma, T=T, N=200, q=q, is_call=False, american=True)
print(f"European put: {euro_put:.6f}")
print(f"American put: {amer_put:.6f}  (early-exercise premium: {amer_put - euro_put:.6f})")
