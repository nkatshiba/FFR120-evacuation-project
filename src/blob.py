# blob.py
import numpy as np


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

