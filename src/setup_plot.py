# setup_plot.py
# import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def setup_plot(fig, ax, D):  # Only pass the ax object
    # plt.ion()
    ax.clear()  # Clear the existing plot
    ax.set_title('Simulation of an Evacuation', color='#fdb777', y=1.05)
    fig.patch.set_facecolor('#242424')
    ax.set_facecolor('#020202')
    # ax.grid(color='#fff', linestyle='-', linewidth=0.1)
    ax.set_xlim(0, D)
    ax.set_ylim(0, D)
    border = Rectangle((0, 0), D, D, linewidth=1, edgecolor='white', facecolor='none')
    ax.add_patch(border)
    cross_width = 0.25  # adjust as needed
    passage_width = 2  # adjust as needed
    ax.add_patch(Rectangle((D/2-cross_width, passage_width), 0.5, D-4, color='#4f4f4f'))
    ax.add_patch(Rectangle((passage_width, D/2-cross_width), D-4, 0.5, color='#4f4f4f'))

    # return fig, ax


# def setup_exits(ax):
#     ax.scatter(*exit_point, color='#00A26B', s=200)
#     ax.text(*exit_point, 'Exit', ha='center', va='bottom', color='#00A26B')
#     ax.scatter(*exit_point2, color='#a20037', s=200)
#     ax.text(*exit_point2, 'Exit', ha='center', va='bottom', color='#a20037')
#     ax.text(0, D - 0.1, 'Exit counter: {}'.format(exit_counter), ha='left', va='top', color='#74e3b1', weight='bold', fontsize=10)
