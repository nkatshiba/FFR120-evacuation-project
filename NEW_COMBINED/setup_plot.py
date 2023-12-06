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

    # Add cross-shaped wall
    cross_width = 0.25  # adjust as needed
    passage_width = 2  # adjust as needed

    # vertical_wall_top = Rectangle((D/2 - cross_width/2, D/2 + passage_width/2), cross_width, D/2 - passage_width/2, facecolor='white')
    # vertical_wall_bottom = Rectangle((D/2 - cross_width/2, 0), cross_width, D/2 - passage_width/2, facecolor='white')
    # horizontal_wall_left = Rectangle((0, D/2 - cross_width/2), D/2 - passage_width/2, cross_width, facecolor='white')
    # horizontal_wall_right = Rectangle((D/2 + passage_width/2, D/2 - cross_width/2), D/2 - passage_width/2, cross_width, facecolor='white')
    #
    # ax.add_patch(vertical_wall_top)
    # ax.add_patch(vertical_wall_bottom)
    # ax.add_patch(horizontal_wall_left)
    # ax.add_patch(horizontal_wall_right)

    ax.add_patch(Rectangle((D/2-0.25, 2), 0.5, D-4, color='white'))
    ax.add_patch(Rectangle((2, D/2-0.25), D-4, 0.5, color='white'))

    return fig, ax
