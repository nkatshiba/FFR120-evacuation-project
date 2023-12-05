# setup_plot.py
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def setup_plot(D):
    plt.ion()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#242424')
    ax.set_facecolor('#020202')
    ax.grid(color='#fff', linestyle='-', linewidth=0.5)
    ax.set_xlim(0, D)
    ax.set_ylim(0, D)
    border = Rectangle((0, 0), D, D, linewidth=1, edgecolor='white', facecolor='none')
    ax.add_patch(border)

    return fig, ax