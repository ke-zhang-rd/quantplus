"""Export the CRR threshold plot as a standalone mpld3 HTML page."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import mpld3
import quantplus as qp


output_path = Path(__file__).parent / "build" / "html" / "_static" / "crr_thresholds_mpld3.html"
output_path.parent.mkdir(parents=True, exist_ok=True)

figure, _ = qp.plot_crr_tree(
    S0=100.0,
    K=100.0,
    r=0.05,
    sigma=0.20,
    T=1.0,
    N=12,
    q=0.01,
    is_call=True,
    american=True,
    S_lower=80.0,
    S_upper=120.0,
    every_step=False,
    show=False,
)

try:
    axes = figure.axes[0]
    for extra_axes in figure.axes[1:]:
        figure.delaxes(extra_axes)

    for collection in tuple(axes.collections):
        if isinstance(collection, PolyCollection):
            collection.remove()

    x_limits = axes.get_xlim()
    for line in axes.lines:
        line.set_transform(axes.transData)
        line.set_xdata(x_limits)

    mpld3.save_html(figure, str(output_path))
finally:
    plt.close(figure)

print(f"Wrote mpld3 plot to {output_path}")
