# experiment.py
import numpy as np
import matplotlib.pyplot as plt
from initialize_blobs import initializeBlobs
from setup_plot import setup_plot
from matplotlib.patches import Rectangle


def experiment(N, T, R, D, eta, stepsize, threshold, min_velocity):
    blobs = initializeBlobs(N, D, threshold, min_velocity)
    fig, ax = setup_plot(D)
    exit_point = np.array([D/2, D])
    exit_point2 = np.array([D, D/2])  # New exit
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
                blob.update([exit_point, exit_point2], alarm_on, stepsize, eta, D, blobs, threshold=1, min_velocity=0.01)

        ax.clear()
        # Create walls
        ax.add_patch(Rectangle((D/2-0.25, 2), 0.5, D-4, color='white'))
        ax.add_patch(Rectangle((2, D/2-0.25), D-4, 0.5, color='white'))
        ax.set_xlim(0, D)
        ax.set_ylim(0, D)
        ax.set_title('Simulation of an Evacuation', color='#fdb777', y=1.05)
        for blob in blobs:
            ax.plot(blob.x, blob.y, '.')
        for i, blob in enumerate(blobs):
            if i not in exited_blobs and (np.linalg.norm(np.array([blob.x, blob.y]) - exit_point) < R or np.linalg.norm(np.array([blob.x, blob.y]) - exit_point2) < R):
                exit_counter += 1
                exited_blobs.add(i)
            if exit_counter == N:
                escape_time = t
        ax.scatter(*exit_point, color='#00A26B', s=200)
        ax.text(*exit_point, 'Exit', ha='center', va='bottom', color='#00A26B')
        ax.scatter(*exit_point2, color='#a20037', s=200)
        ax.text(*exit_point2, 'Exit', ha='center', va='bottom', color='#a20037')
        ax.text(0, D - 0.1, 'Exit counter: {}'.format(exit_counter), ha='left', va='top', color='#74e3b1', weight='bold', fontsize=10)
        if alarm_on:
            ax.text(D/2, 0, 'Alarm ON', ha='center', va='bottom', color='#E61C29', fontsize=14)
        plt.draw()
        plt.pause(0.01)
        if escape_time is not None:
            break
    plt.ioff()
    if escape_time is not None:
        print(f"Escape time: {escape_time} time steps")
    else:
        print("Simulation ended without all individuals escaping.")

