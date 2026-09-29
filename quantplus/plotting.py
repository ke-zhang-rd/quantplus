"""Interactive plotting helpers for CRR option trees."""

import math

from ._crr_pricer import crr_price


def _alive_nodes(stock_tree, S_upper, S_lower, every_step):
    steps = len(stock_tree) - 1
    upper = math.inf if S_upper is None else S_upper
    lower = -math.inf if S_lower is None else S_lower
    alive = [[False] * (i + 1) for i in range(steps + 1)]

    for j, stock in enumerate(stock_tree[steps]):
        alive[steps][j] = lower <= stock <= upper

    for i in range(steps - 1, -1, -1):
        for j, stock in enumerate(stock_tree[i]):
            can_reach = alive[i + 1][j] or alive[i + 1][j + 1]
            alive[i][j] = can_reach and (not every_step or lower <= stock <= upper)
    return alive


def plot_crr_tree(
    S0,
    K,
    r,
    sigma,
    T,
    N,
    q=0.0,
    is_call=True,
    american=True,
    S_upper=None,
    S_lower=None,
    every_step=False,
    show=True,
):
    """Show an interactive CRR tree with draggable stock-price thresholds.

    Nodes that cannot reach a terminal stock price inside ``[S_lower,
    S_upper]`` are greyed out. Drag either horizontal threshold to update the
    bounded option price. ``matplotlib`` is needed only when this function is
    called.

    Returns the ``(figure, axes)`` pair. Set ``show=False`` to build the plot
    without entering Matplotlib's GUI event loop.
    """
    if N <= 0:
        raise ValueError(f"N must be a positive integer, got {N}")
    if T <= 0:
        raise ValueError(f"T must be positive, got {T}")
    if sigma < 0:
        raise ValueError(f"sigma must be non-negative, got {sigma}")

    try:
        import matplotlib.pyplot as plt
        from matplotlib.collections import LineCollection
        from matplotlib.widgets import CheckButtons
    except ImportError as exc:
        raise ImportError("plot_crr_tree requires matplotlib") from exc

    dt = T / N
    up = math.exp(sigma * math.sqrt(dt))
    down = 1.0 / up
    stock_tree = [
        [S0 * up ** (i - j) * down**j for j in range(i + 1)]
        for i in range(N + 1)
    ]
    nodes = [(i, j) for i in range(N + 1) for j in range(i + 1)]
    edges = [
        ((i, j), (i + 1, child_j))
        for i in range(N)
        for j in range(i + 1)
        for child_j in (j, j + 1)
    ]
    segments = [
        [(parent[0], stock_tree[parent[0]][parent[1]]),
         (child[0], stock_tree[child[0]][child[1]])]
        for parent, child in edges
    ]
    xs = [i for i, _ in nodes]
    ys = [stock_tree[i][j] for i, j in nodes]
    ymin, ymax = min(ys), max(ys)
    pad = 0.05 * (ymax - ymin) if ymax != ymin else max(abs(ymax) * 0.05, 1.0)

    default_upper = min(ymax, S0 * math.exp(2 * sigma * math.sqrt(T)))
    default_lower = max(ymin, S0 * math.exp(-2 * sigma * math.sqrt(T)))
    hi = default_upper if S_upper is None else min(max(S_upper, ymin), ymax)
    lo = default_lower if S_lower is None else min(max(S_lower, ymin), ymax)
    if lo > hi:
        raise ValueError("S_lower must be less than or equal to S_upper")
    state = {"every_step": bool(every_step)}

    fig, ax = plt.subplots(figsize=(11, 7))
    plt.subplots_adjust(top=0.88, bottom=0.14)
    check_ax = fig.add_axes([0.01, 0.005, 0.25, 0.06], frameon=False)
    check = CheckButtons(check_ax, ["apply at every time step"], [state["every_step"]])
    ax.set_xlim(-0.5, N + 0.5)
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.set_xlabel("time step")
    ax.set_ylabel("stock price")

    lines = LineCollection(segments, linewidths=0.8)
    ax.add_collection(lines)
    points = ax.scatter(xs, ys, s=max(4, 400 // N), zorder=3)
    ax.axhline(K, color="black", linestyle=":", linewidth=0.8)
    ax.text(0, K, " strike", va="bottom", fontsize=8)
    upper_line = ax.axhline(hi, color="tab:red", linewidth=2.5)
    lower_line = ax.axhline(lo, color="tab:green", linewidth=2.5)
    upper_text = ax.text(N, hi, "", color="tab:red", ha="right", va="bottom", fontsize=9)
    lower_text = ax.text(N, lo, "", color="tab:green", ha="right", va="top", fontsize=9)
    shades = []
    full_price = crr_price(S0, K, r, sigma, T, N, q, is_call, american)

    def update():
        upper = upper_line.get_ydata()[0]
        lower = lower_line.get_ydata()[0]
        alive = _alive_nodes(stock_tree, upper, lower, state["every_step"])
        colors = ["tab:blue" if alive[i][j] else "#cccccc" for i, j in nodes]
        edge_colors = [
            "#6a8fc7" if alive[a[0]][a[1]] and alive[b[0]][b[1]] else "#e3e3e3"
            for a, b in edges
        ]
        points.set_facecolors(colors)
        points.set_edgecolors(colors)
        lines.set_colors(edge_colors)

        for shade in shades:
            shade.remove()
        shades.clear()
        shades.append(ax.axhspan(upper, ymax + pad, color="tab:red", alpha=0.07))
        shades.append(ax.axhspan(ymin - pad, lower, color="tab:green", alpha=0.07))
        upper_text.set_position((N, upper))
        upper_text.set_text(f"S_upper = {upper:.2f}  ")
        lower_text.set_position((N, lower))
        lower_text.set_text(f"S_lower = {lower:.2f}  ")

        try:
            price = crr_price(
                S0, K, r, sigma, T, N, q, is_call, american,
                upper, lower, state["every_step"],
            )
            price_text = f"option price = {price:.4f}   (no bounds: {full_price:.4f})"
        except ValueError:
            price_text = "No path survives inside the band - widen it"
        kept = sum(alive[N])
        mode = "every step" if state["every_step"] else "expiry only"
        ax.set_title(
            f"CRR tree, N={N}, thresholds: {mode}\n{price_text}   |   "
            f"terminal nodes kept: {kept}/{N + 1}",
            fontsize=10,
        )
        fig.canvas.draw_idle()

    dragging = {"line": None}

    def on_press(event):
        if event.inaxes is not ax or event.y is None:
            return
        closest, distance = None, 8
        for line in (upper_line, lower_line):
            pixel_y = ax.transData.transform((0, line.get_ydata()[0]))[1]
            if abs(pixel_y - event.y) < distance:
                closest, distance = line, abs(pixel_y - event.y)
        dragging["line"] = closest

    def on_motion(event):
        line = dragging["line"]
        if line is None or event.inaxes is not ax or event.ydata is None:
            return
        y = min(max(event.ydata, ymin), ymax)
        if line is upper_line:
            y = max(y, lower_line.get_ydata()[0])
        else:
            y = min(y, upper_line.get_ydata()[0])
        line.set_ydata([y, y])
        update()

    def on_release(_event):
        dragging["line"] = None

    def on_toggle(_label):
        state["every_step"] = check.get_status()[0]
        update()

    check.on_clicked(on_toggle)
    fig.canvas.mpl_connect("button_press_event", on_press)
    fig.canvas.mpl_connect("motion_notify_event", on_motion)
    fig.canvas.mpl_connect("button_release_event", on_release)
    update()
    if show:
        plt.show()
    return fig, ax


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Plot an interactive CRR price tree.")
    parser.add_argument("N", nargs="?", type=int, default=30)
    parser.add_argument("--every-step", action="store_true")
    args = parser.parse_args()
    plot_crr_tree(
        S0=225.0,
        K=240.0,
        r=0.0425,
        sigma=0.35,
        T=55 / 365,
        N=args.N,
        every_step=args.every_step,
    )
