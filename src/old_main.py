import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class Blob:
    def __init__(self, angle, x, y):
        self.angle = angle
        self.x = x
        self.y = y
        self.velocity = np.array([0.0, 0.0])

    def update(self, exit_point, alarm_on, stepsize, eta, D):
        if alarm_on:
            exit_direction = np.arctan2(
                exit_point[1] - self.y, exit_point[0] - self.x)
            self.angle = 0.5 * self.angle + 0.5 * exit_direction
            noise = (-eta / 2 + np.random.rand(1) * eta / 2)
            self.angle = self.angle + noise.item()
            v = self.velocity * \
                np.array([np.cos(self.angle), np.sin(self.angle)])
        else:
            v = self.velocity
        self.x, self.y = np.clip(
            np.array([self.x, self.y]) + stepsize * v, 0, D)


def initializeBlobs(N, D=25):
    blobs = []
    for i in range(N):
        angle = np.random.rand() * 2 * np.pi
        if i < N // 2:
            x = np.random.rand() * D / 2
            y = np.random.rand() * D / 3
        else:
            x = D / 2 + np.random.rand() * D / 2
            y = np.random.rand() * D
        blobs.append(Blob(angle, x, y))
    return blobs


def setup_plot(D):
    plt.ion()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#242424')
    ax.set_facecolor('#020202')
    ax.grid(color='#fff', linestyle='-', linewidth=0.5)
    ax.set_xlim(0, D)
    ax.set_ylim(0, D)
    border = Rectangle((0, 0), D, D, linewidth=1,
                       edgecolor='white', facecolor='none')
    ax.add_patch(border)
    return fig, ax


def experiment(N=30, T=1000, R=1, D=25, eta=0.1, stepsize=2):
    blobs = initializeBlobs(N, D=D)
    fig, ax = setup_plot(D)
    exit_point = np.array([D/2, D])
    exit_counter = 0
    exited_blobs = set()
    escape_time = None
    k = 0
    for t in range(T-1):
        alarm_on = t >= 50
        if alarm_on and k == 0:
            k = 1
            for blob in blobs:
                blob.velocity = 0.08 * np.random.normal(eta * 5, 0.2)
        for blob in blobs:
            blob.update(exit_point, alarm_on, stepsize, eta, D)
        ax.clear()
        ax.set_xlim(0, D)
        ax.set_ylim(0, D)
        ax.set_title('Simulation of an Evacuation', color='#fdb777', y=1.05)
        for blob in blobs:
            ax.plot(blob.x, blob.y, '.')
        for i, blob in enumerate(blobs):
            if i not in exited_blobs and np.linalg.norm(np.array([blob.x, blob.y]) - exit_point) < R:
                exit_counter += 1
                exited_blobs.add(i)
        if exit_counter == N:
            escape_time = t
        ax.scatter(*exit_point, color='#00A26B', s=200)
        ax.text(*exit_point, 'Exit', ha='center', va='bottom', color='#00A26B')
        ax.text(0, D - 0.1, 'Exit counter: {}'.format(exit_counter),
                ha='left', va='top', color='#74e3b1', weight='bold', fontsize=10)
        if alarm_on:
            ax.text(D/2, 0, 'Alarm ON', ha='center',
                    va='bottom', color='#E61C29', fontsize=14)
        plt.draw()
        plt.pause(0.01)
        if escape_time is not None:
            break
    plt.ioff()
    if escape_time is not None:
        print(f"Escape time: {escape_time} time steps")
    else:
        print("Simulation ended without all individuals escaping.")


experiment()
