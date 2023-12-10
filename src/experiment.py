# experiment.py
import numpy as np
import matplotlib.pyplot as plt
from initialize_blobs import initializeBlobs
from setup_plot import setup_plot


def experiment(N, T, R, D, eta, stepsize, threshold, min_velocity):
    blobs = initializeBlobs(N, D, threshold, min_velocity)
    fig, ax = plt.subplots()
    setup_plot(fig, ax, D)  # Pass the ax object to setup_plot
    # exit_point = np.array([D/2, D])
    # exit_point2 = np.array([D, D/2])  # New exit

    exit_point1 = np.array([D/2, D])  # TOP
    exit_point2 = np.array([D, D/2])  # RIGHT
    exit_point3 = np.array([0, D/2])  # LEFT
    exit_point4 = np.array([D/2, 0])  # BOT

    exit_counter = 0
    exited_blobs = set()
    escape_time = None
    k = 0

    for t in range(T-1):
        alarm_on = t >= 50
        if alarm_on:
            if k == 0:
                k = 1
                for blob in blobs:
                    blob.velocity = 0.08 * np.random.normal(eta * 5, 0.2)

        for blob in blobs:
            # blob.update([exit_point, exit_point2], alarm_on, stepsize, eta, D, blobs, threshold=1, min_velocity=0.01)

            blob.update([exit_point1, exit_point2, exit_point3, exit_point4], alarm_on, stepsize, eta, D, blobs, threshold=1, min_velocity=0.01)

        ax.clear()
        setup_plot(fig, ax, D)  # Reset the plot using the existing ax object

        for blob in blobs:
            if blob in exited_blobs:
                ax.plot(blob.x, blob.y, '.', color='#808080')  # Exited blobs in gray
            else:
                ax.plot(blob.x, blob.y, '.', color='#0000FF')  # Moving blobs in blue

        for blob in blobs:
            if blob not in exited_blobs and (np.linalg.norm(np.array([blob.x, blob.y]) - exit_point1) < R or np.linalg.norm(np.array([blob.x, blob.y]) - exit_point2) < R):
                exit_counter += 1
                exited_blobs.add(blob)  # Add the blob object, not its index

        if exit_counter == N:
            escape_time = t

        exit_col1 = '#ff003d'
        exit_col2 = '#ff003d'
        exit_col3 = '#69c3c3'
        exit_col4 = '#ffa0cd'
        exit_count_col = '#74e3b1'
        time_col = '#D3D3D3'
        alarm_col = '#FFFF00'

        ax.scatter(*exit_point1, color=exit_col1, s=200)
        ax.text(*exit_point1, 'Exit 1', ha='center', va='bottom', color=exit_col1)
        ax.scatter(*exit_point2, color=exit_col2, s=200)
        ax.text(*exit_point2, 'Exit 2', ha='left', va='center', color=exit_col2)
        ax.scatter(*exit_point3, color=exit_col3, s=200)
        ax.text(*exit_point3, 'CP 1', ha='right', va='center', color=exit_col3)
        ax.scatter(*exit_point4, color=exit_col4, s=200)
        ax.text(*exit_point4, 'CP 2', ha='center', va='top', color=exit_col4)

        ax.text(0 + 0.2, D - 0.7, 'Exit counter: {}'.format(exit_counter), ha='left', va='top', color=exit_count_col, weight='bold', fontsize=10)
        ax.text(0 + 0.2, D - 0.2, f'Time step: {t}', ha='left', va='top', color=time_col, weight='bold', fontsize=10)

        if alarm_on:
            ax.text(D/2, 0.7, 'Alarm ON', ha='center', va='bottom', color=alarm_col, fontsize=14)

        plt.draw()
        plt.pause(0.01)

        if escape_time is not None:
            break

    plt.ioff()

    if escape_time is not None:
        print(f"Escape time: {escape_time} time steps")
    else:
        print("Simulation ended without all individuals escaping.")

