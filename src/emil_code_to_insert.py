import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


D = 25

def initializeCells(N, D=25):
    state0 = np.zeros(shape=(N*3,))

    # Initialize half of the individuals in the bottom left quadrant
    for i in range(N // 2):
        state0[0 + 3 * i] = np.random.rand() * 2 * np.pi  # Angle
        state0[1 + 3 * i] = np.random.rand() * D / 2  # X-coordinate (left half of the space)
        state0[2 + 3 * i] = np.random.rand() * D / 3  # Y-coordinate (bottom third of the space)

    # Initialize the rest randomly in the remaining quadrants
    for i in range(N // 2, N):
        state0[0 + 3 * i] = np.random.rand() * 2 * np.pi  # Angle
        state0[1 + 3 * i] = D / 2 + np.random.rand() * D / 2  # X-coordinate (right half of the space)
        state0[2 + 3 * i] = np.random.rand() * D  # Y-coordinate (entire height of the space)

    return state0

def find_close_blobs(trajectory, threshold_distance, exit_point, exit_dist_threshold):
    N = len(trajectory) // 3
    close_blobs = set()
    close_to_exit = []

    for i in range(N):
        for j in range(i + 1, N):
            pos_i = trajectory[np.array([1, 2]) + 3 * i]
            pos_j = trajectory[np.array([1, 2]) + 3 * j]
            distance = np.linalg.norm(pos_i - pos_j)
            distance_exit_i = np.linalg.norm(pos_i - exit_point)
            distance_exit_j = np.linalg.norm(pos_j - exit_point)

            if distance < threshold_distance:
                close_blobs.add(i)
                close_blobs.add(j)

            if distance_exit_i < exit_dist_threshold:
                close_to_exit.append(i)

            if distance_exit_j < exit_dist_threshold:
                close_to_exit.append(j)

    return close_blobs, close_to_exit


def update_rule_4(present, exit_point, alarm_on, velocities, proximity_threshold = 0.8, exit_dist_threshold = 1.5, stepsize=1, eta=0.1, D=25, R=1):
    future = np.copy(present)
    N = np.size(present) // 3

    close_blobs, close_to_exit = find_close_blobs(present, proximity_threshold, exit_point, exit_dist_threshold)


    for n in range(N):
        mytheta = np.mod(present[3 * n], 2 * np.pi)
        mypos = present[np.array([1, 2]) + 3 * n]

        if alarm_on:
            exit_direction = np.arctan2(exit_point[1] - mypos[1], exit_point[0] - mypos[0])
            mytheta = 0.5 * mytheta + 0.5 * exit_direction
            noise = (-eta / 2 + np.random.rand(1) * eta / 2)
            mytheta = mytheta + noise.item()
            if n in close_blobs and n in close_to_exit:
                v = velocities[n] * 0.05 * np.array([np.cos(mytheta), np.sin(mytheta)])
            elif n in close_blobs:
                v = velocities[n] * 0.5 * np.array([np.cos(mytheta), np.sin(mytheta)])
            else:
                v = velocities[n]* np.array([np.cos(mytheta), np.sin(mytheta)])

        else:
            # If alarm is not on, use the original velocity
            v = 0.0001

        future[3 * n] = mytheta
        future[np.array([1, 2]) + 3 * n] = present[np.array([1, 2]) + 3 * n] + stepsize * v

        # Ensure individuals stay within the boundaries
        future[np.array([1, 2]) + 3 * n] = np.clip(future[np.array([1, 2]) + 3 * n], 0, D)

    return future

def experiment(N=30, T=1000, R=1, D=25, eta=0.1, stepsize=4):
    velocities = np.zeros((N, 2))  # Initialize an array to store velocities

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
    escape_time = None  # Initialize escape time variable
    k = 0
    for t in range(T-1):
        alarm_on = t >= 50  # Turn on the alarm after 5 seconds (50 time steps)

        if alarm_on and k == 0:
            k = 1
            for i in range(N):
                velocities[i] = 0.1 * np.random.normal(eta * 5, 0.1)

        trajectory[:, t+1] = update_rule_4(trajectory[:, t], exit_point, alarm_on, stepsize=stepsize, eta=eta, R=R, D=D, velocities=velocities)
        ax.clear()  # Clear the axes
        ax.set_xlim(0, D)
        ax.set_ylim(0, D)
        ax.set_title('Simulation of an Evacuation', color='#fdb777',
                     y=1.05)  # Set the title after clearing the axes
        for i in range(0, len(trajectory[:, t+1]), 3):
            # Plot the current state
            ax.plot(trajectory[i+1, t+1], trajectory[i+2, t+1], '.')
            # Check if the blob has reached the exit and hasn't been counted yet
            if i not in exited_blobs and np.linalg.norm(trajectory[i+1:i+3, t+1] - exit_point) < R:
                exit_counter += 1
                exited_blobs.add(i)
                if exit_counter == N:
                    escape_time = t
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

        if escape_time is not None:
            break  # End the simulation if all individuals have escaped

    plt.ioff()  # Turn off interactive mode
    if escape_time is not None:
        print(f"Escape time: {escape_time} time steps")
    else:
        print("Simulation ended without all individuals escaping.")

    return trajectory


trajectory = experiment()