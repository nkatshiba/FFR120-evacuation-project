# experiment.py
import numpy as np
import matplotlib.pyplot as plt
from initialize_blobs import initializeBlobs
from setup_plot import setup_plot


def experiment(N, T, R, D, eta, stepsize, threshold, min_velocity, alarm_delay):
    blobs = initializeBlobs(N, D, threshold, min_velocity)
    fig, ax = plt.subplots()
    setup_plot(fig, ax, D)  # Pass the ax object to setup_plot
    # exit_point = np.array([D/2, D])
    # exit_point2 = np.array([D, D/2])  # New exit

    exit_point1 = np.array([D/2, D])  # TOP
    exit_point2 = np.array([D, D/2])  # RIGHT
    check_point1 = np.array([0, D/2])  # LEFT
    check_point2 = np.array([D/2, 0])  # BOT

    exit_counter = 0
    exited_blobs = set()
    escape_time = None
    eighty_perc_escape_time = None
    k = 0

    for t in range(T-1):
        alarm_on = t >= alarm_delay
        if alarm_on:
            if k == 0:
                k = 1
                for blob in blobs:
                    blob.velocity = 0.1 * np.random.normal(eta * 5, 0.2)
                    if blob.velocity < min_velocity:
                        blob.velocity = min_velocity
        for blob in blobs:
            blob.update(
                [exit_point1, exit_point2, check_point1, check_point2],
                [check_point1, check_point2],
                alarm_on,
                stepsize,
                eta,
                D,
                blobs,
                threshold=1,
                min_velocity=0.02,
                max_velocity=0.07,
                turn_around_steps=20,
                exit_counter=exit_counter,
                exited_blobs=exited_blobs,
                alignment_strength=0.5,  # Adjust this value to control the strength of alignment
                neighbor_radius=5,  # Adjust this value to control the radius for neighbor detection
            )
        # for blob in blobs:
        #     # blob.update([exit_point1, exit_point2, check_point1, check_point2], alarm_on, stepsize, eta, D, blobs, threshold=1, min_velocity=0.01)
        #     # blob.update([exit_point1, exit_point2, check_point1, check_point2], [check_point1, check_point2], alarm_on, stepsize,
        #     #             eta, D, blobs, threshold=1, min_velocity=0.01, max_velocity=0.05, turn_around_steps=20)
        #     blob.update([exit_point1, exit_point2, check_point1, check_point2], [check_point1, check_point2], alarm_on, stepsize,
        #                 eta, D, blobs, threshold=1, min_velocity=0.01, max_velocity=0.05, turn_around_steps=20, exit_counter=exit_counter, exited_blobs=exited_blobs)

        ax.clear()
        setup_plot(fig, ax, D)  # Reset the plot using the existing ax object

        for blob in blobs:
            if blob in exited_blobs: # Exited blobs in gray
                ax.plot(blob.x, blob.y, 'o', color='#00ff0c', markersize=7)
            else: # Moving blobs in blue
                ax.plot(blob.x, blob.y, 'o', color='#ff02c5', markersize=7)

        for blob in blobs:
            if blob not in exited_blobs and (np.linalg.norm(np.array([blob.x, blob.y]) - exit_point1) < R or np.linalg.norm(np.array([blob.x, blob.y]) - exit_point2) < R):
                exit_counter += 1
                exited_blobs.add(blob)  # Add the blob object, not its index

        if exit_counter == 0.8*N:
            eighty_perc_escape_time = t

        if exit_counter == N:
            escape_time = t

        exit_col1 = '#ff003d'
        exit_col2 = '#ff003d'
        cp_col1 = '#69c3c3'
        cp_col2 = '#ffa0cd'

        exit_count_col = '#74e3b1'
        time_col = '#D3D3D3'
        alarm_col = '#FFFF00'

        ax.scatter(*exit_point1, color=exit_col1, s=200)
        ax.text(*exit_point1, 'Exit 1', ha='center',
                va='bottom', color=exit_col1)
        ax.scatter(*exit_point2, color=exit_col2, s=200)
        ax.text(*exit_point2, 'Exit 2', ha='left',
                va='center', color=exit_col2)
        # ax.scatter(*check_point1, color=cp_col1, s=200)
        # ax.text(*check_point1, 'CP 1', ha='right', va='center', color=cp_col1)
        # ax.scatter(*check_point2, color=cp_col2, s=200)
        # ax.text(*check_point2, 'CP 2', ha='center', va='top', color=cp_col2)

        ax.text(0 + 0.2, D - 0.7, 'Exit counter: {}'.format(exit_counter),
                ha='left', va='top', color=exit_count_col, weight='bold', fontsize=10)
        ax.text(0 + 0.2, D - 0.2, f'Time step: {t}', ha='left',
                va='top', color=time_col, weight='bold', fontsize=10)

        if alarm_on:
            ax.text(D/2, 0.7, 'Alarm ON', ha='center',
                    va='bottom', color=alarm_col, fontsize=14)

        plt.draw()
        plt.pause(0.01)

        if escape_time is not None:
            break

    plt.ioff()
    plt.close(fig)
    if escape_time is not None or eighty_perc_escape_time is not None:
        print(f"Escape time: {escape_time} time steps | Escape time (80%): {eighty_perc_escape_time} time steps")
        return escape_time, eighty_perc_escape_time
    else:
        print("Simulation ended without all individuals escaping.")
        return escape_time, eighty_perc_escape_time
