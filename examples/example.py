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

print("\n=== Stock-price threshold pruning ===")
thresholds = {"S_upper": 300.0, "S_lower": 170.0}
tree_steps = 30
expiry_only = qp.crr_price(
    S0=S0, K=K, r=r, sigma=sigma, T=T, N=tree_steps, q=q,
    american=True, **thresholds,
)
every_step = qp.crr_price(
    S0=S0, K=K, r=r, sigma=sigma, T=T, N=tree_steps, q=q,
    american=True, every_step=True, **thresholds,
)
unbounded_call = qp.crr_price(
    S0=S0, K=K, r=r, sigma=sigma, T=T, N=tree_steps, q=q, american=True
)
print(f"American call, no bounds: {unbounded_call:.6f}")
print(f"Thresholds at expiry only: {expiry_only:.6f}")
print(f"Thresholds every step:     {every_step:.6f}")

print("\nOpening interactive CRR tree; drag the threshold lines or toggle every-step pruning.")
qp.plot_crr_tree(
    S0=S0, K=K, r=r, sigma=sigma, T=T, N=tree_steps, q=q,
    american=True, every_step=False, **thresholds,
)
