"""Interactive CRR tree: drag the two horizontal bars to set the expiry
stock-price thresholds (S_upper / S_lower). Nodes that can no longer reach an
allowed terminal price are greyed out, and the option price is recomputed live.

Usage:  python crr_plot.py [N] [--every-step]
        N = number of steps (default 30)
        --every-step: start with the thresholds applied at every time step
        (can also be toggled with the check box in the window)
Needs test.py (the crr() function) in the same folder.
"""
import importlib.util
import math
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.widgets import CheckButtons

# --- load crr() from test.py (loaded by path: "import test" would clash
#     with Python's built-in "test" package) ---
_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("crr_module", os.path.join(_here, "test.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
crr = _mod.crr

# --- parameters (same as test.py) ---
r = 0.0425
sigma = 0.35
T = 55 / 365
S0 = 225
K = 240
_nums = [a for a in sys.argv[1:] if a.isdigit()]
N = int(_nums[0]) if _nums else 30
state = {"every_step": "--every-step" in sys.argv}

dt = T / N
u = math.exp(sigma * math.sqrt(dt))
d = 1 / u

# --- tree geometry: node (i, j) sits at x = i, y = S0 * u^(i-j) * d^j ---
S = [[S0 * u ** (i - j) * d ** j for j in range(i + 1)] for i in range(N + 1)]
node_id = {}
xs, ys = [], []
for i in range(N + 1):
    for j in range(i + 1):
        node_id[(i, j)] = len(xs)
        xs.append(i)
        ys.append(S[i][j])
edges = []  # (parent (i,j), child (i+1,j) or (i+1,j+1))
segments = []
for i in range(N):
    for j in range(i + 1):
        for cj in (j, j + 1):
            edges.append(((i, j), (i + 1, cj)))
            segments.append([(i, S[i][j]), (i + 1, S[i + 1][cj])])


def alive_nodes(S_upper, S_lower):
    """Pruning rule lives in test.py (single source of truth)."""
    return _mod.alive_nodes(S, S_upper, S_lower, state["every_step"])


# --- figure ---
fig, ax = plt.subplots(figsize=(11, 7))
plt.subplots_adjust(top=0.88, bottom=0.14)

# check box: apply thresholds at every time step or only at expiry
check_ax = fig.add_axes([0.01, 0.005, 0.22, 0.06], frameon=False)
check = CheckButtons(check_ax, ["apply at every time step"], [state["every_step"]])

ymin, ymax = min(ys), max(ys)
pad = 0.05 * (ymax - ymin)
ax.set_xlim(-0.5, N + 0.5)
ax.set_ylim(ymin - pad, ymax + pad)
ax.set_xlabel("time step")
ax.set_ylabel("stock price")

lc = LineCollection(segments, linewidths=0.8)
ax.add_collection(lc)
sc = ax.scatter(xs, ys, s=max(4, 400 // N), zorder=3)
ax.axhline(K, color="k", ls=":", lw=0.8)
ax.text(0, K, " strike", va="bottom", fontsize=8)

# initial thresholds: about +/- 2 standard deviations of the terminal price
init_hi = min(ymax, S0 * math.exp(2 * sigma * math.sqrt(T)))
init_lo = max(ymin, S0 * math.exp(-2 * sigma * math.sqrt(T)))
hi_line = ax.axhline(init_hi, color="tab:red", lw=2.5, picker=True)
lo_line = ax.axhline(init_lo, color="tab:green", lw=2.5, picker=True)
hi_text = ax.text(N, init_hi, "", color="tab:red", ha="right", va="bottom", fontsize=9)
lo_text = ax.text(N, init_lo, "", color="tab:green", ha="right", va="top", fontsize=9)
shade = []  # shaded excluded regions, rebuilt on every update

no_bound_price = crr(S0, K, r, sigma, T, N, verbose=False)


def update():
    S_upper, S_lower = hi_line.get_ydata()[0], lo_line.get_ydata()[0]
    alive = alive_nodes(S_upper, S_lower)

    node_colors = ["tab:blue" if alive[i][j] else "#cccccc" for (i, j) in node_id]
    edge_colors = [
        "#6a8fc7" if alive[a[0]][a[1]] and alive[b[0]][b[1]] else "#e3e3e3"
        for a, b in edges
    ]
    sc.set_facecolors(node_colors)
    sc.set_edgecolors(node_colors)
    lc.set_colors(edge_colors)

    for s in shade:
        s.remove()
    shade.clear()
    shade.append(ax.axhspan(S_upper, ymax + pad, color="tab:red", alpha=0.07))
    shade.append(ax.axhspan(ymin - pad, S_lower, color="tab:green", alpha=0.07))

    hi_text.set_position((N, S_upper))
    hi_text.set_text(f"S_upper = {S_upper:.2f}  ")
    lo_text.set_position((N, S_lower))
    lo_text.set_text(f"S_lower = {S_lower:.2f}  ")

    try:
        price = crr(S0, K, r, sigma, T, N, S_upper=S_upper, S_lower=S_lower,
                    every_step=state["every_step"], verbose=False)
        msg = f"American call price = {price:.4f}   (no bounds: {no_bound_price:.4f})"
    except ValueError:
        msg = "No path survives inside the band - widen it"
    n_alive = sum(alive[N])
    mode = "every step" if state["every_step"] else "expiry only"
    ax.set_title(f"CRR tree, N={N}, thresholds: {mode}\n{msg}   |   terminal nodes kept: {n_alive}/{N + 1}", fontsize=10)
    fig.canvas.draw_idle()


# --- dragging ---
dragging = {"line": None}


def on_press(event):
    if event.inaxes is not ax or event.ydata is None:
        return
    # pick whichever bar is closer (in pixels) if within 8 px
    best, best_px = None, 8
    for line in (hi_line, lo_line):
        py = ax.transData.transform((0, line.get_ydata()[0]))[1]
        if abs(py - event.y) < best_px:
            best, best_px = line, abs(py - event.y)
    dragging["line"] = best


def on_motion(event):
    line = dragging["line"]
    if line is None or event.inaxes is not ax or event.ydata is None:
        return
    y = min(max(event.ydata, ymin), ymax)
    if line is hi_line:
        y = max(y, lo_line.get_ydata()[0])
    else:
        y = min(y, hi_line.get_ydata()[0])
    line.set_ydata([y, y])
    update()


def on_release(event):
    dragging["line"] = None


def on_toggle(_label):
    state["every_step"] = check.get_status()[0]
    update()


check.on_clicked(on_toggle)
fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("motion_notify_event", on_motion)
fig.canvas.mpl_connect("button_release_event", on_release)

update()

if __name__ == "__main__":
    plt.show()
