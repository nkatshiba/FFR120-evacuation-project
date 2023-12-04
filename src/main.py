import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


D = 25


def initializeCells(N, D=25):
    state0 = np.zeros(shape=(N*3,))
    state0[0::3] = np.random.rand(N,) * 2 * np.pi
    state0[1::3] = np.random.rand(N,) * D
    state0[2::3] = np.random.rand(N,) * D
    return state0


def update_rule_4(present, exit_point, alarm_on, stepsize=1, eta=0.1, D=25, R=1, v0=0.03):
    future = np.copy(present)
    N = np.size(present) // 3
    for n in range(N):
        mytheta = np.mod(present[3*n], 2*np.pi)
        mypos = present[np.array([1, 2]) + 3*n]
        if alarm_on:
            exit_direction = np.arctan2(
                exit_point[1] - mypos[1], exit_point[0] - mypos[0])
            mytheta = 0.5 * mytheta + 0.5 * exit_direction
            noise = (-eta/2 + np.random.rand(1) * eta/2)
            mytheta = mytheta + noise.item()
        v = v0*np.array([np.cos(mytheta), np.sin(mytheta)])
        future[3*n] = mytheta
        future[np.array([1, 2]) + 3 *
               n] = present[np.array([1, 2])+3*n] + stepsize*v
        future[np.array([1, 2]) + 3 *
               n] = np.mod(future[np.array([1, 2]) + 3*n], D)
    return (future)


def experiment(N=30, T=1000, R=1, D=25, eta=0.1, stepsize=1):
    state0 = initializeCells(N, D=D)
    trajectory = np.zeros(shape=(N*3, T))
    trajectory[:, 0] = state0
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()  # Create a figure and an axes
    # Set the figure background color to black
    fig.patch.set_facecolor('#242424')
    ax.set_facecolor('#020202')  # Set the axes background color to dark gray
    # Set the grid color to white
    ax.grid(color='#fff', linestyle='-', linewidth=0.5)
    ax.set_xlim(0, D)
    ax.set_ylim(0, D)
    # Create a border around the plot
    border = Rectangle((0, 0), D, D, linewidth=1,
                       edgecolor='white', facecolor='none')
    ax.add_patch(border)
    exit_point = np.array([D/2, D])  # Define the exit point
    exit_counter = 0  # Initialize the exit counter
    exited_blobs = set()  # Keep track of which blobs have exited
    for t in range(T-1):
        alarm_on = t >= 50  # Turn on the alarm after 5 seconds (50 time steps)
        trajectory[:, t+1] = update_rule_4(
            trajectory[:, t], exit_point, alarm_on, stepsize=stepsize, eta=eta, R=R, D=D)
        ax.clear()  # Clear the axes
        ax.set_xlim(0, D)
        ax.set_ylim(0, D)
        ax.set_title('Simulaion of an Evacuation', color='#fdb777',
                     y=1.05)  # Set the title after clearing the axes
        for i in range(0, len(trajectory[:, t+1]), 3):
            # Plot the current state
            ax.plot(trajectory[i+1, t+1], trajectory[i+2, t+1], '.')
            # Check if the blob has reached the exit and hasn't been counted yet
            if i not in exited_blobs and np.linalg.norm(trajectory[i+1:i+3, t+1] - exit_point) < R:
                exit_counter += 1
                exited_blobs.add(i)
        ax.scatter(*exit_point, color='#00A26B', s=200)  # Plot the exit point
        ax.text(exit_point[0], exit_point[1], 'Exit', ha='center',
                va='bottom', color='#00A26B')  # Add a label for the exit
        ax.text(0, D - 0.1, 'Exit counter: {}'.format(exit_counter),
                ha='left', va='top', color='#74e3b1', weight='bold', fontsize=10)
        if alarm_on:
            ax.text(D/2, 0, 'Alarm ON', ha='center', va='bottom',
                    color='#E61C29', fontsize=14)  # Display the alarm status
        plt.draw()  # Redraw the figure
        plt.pause(0.01)  # Pause for a short period
    plt.ioff()  # Turn off interactive mode
    return trajectory

#test
trajectory = experiment()
