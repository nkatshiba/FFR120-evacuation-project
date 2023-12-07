# blob.py
import numpy as np


class Blob:
    def __init__(self, angle, x, y):
        self.angle = angle
        self.x = x
        self.y = y
        self.velocity = np.array([0.0, 0.0])

    def update(self, exit_points, alarm_on, stepsize, eta, D):
        if alarm_on:
            # Determine the closest exit point
            distances = [np.sqrt((exit_point[0] - self.x)**2 + (exit_point[1] - self.y)**2) for exit_point in exit_points]
            closest_exit = exit_points[np.argmin(distances)]
            exit_direction = np.arctan2(closest_exit[1] - self.y, closest_exit[0] - self.x)
            self.angle = 0.5 * self.angle + 0.5 * exit_direction
            noise = (-eta / 2 + np.random.rand(1) * eta / 2)
            self.angle = self.angle + noise.item()
            v = self.velocity * np.array([np.cos(self.angle), np.sin(self.angle)])
        else:
            v = self.velocity

        proposed_position = np.array([self.x, self.y]) + stepsize * v
        if self.intersects_wall(proposed_position, D):
            # If the proposed move intersects the wall, adjust the move to avoid the wall
            # Move along the edge of the wall towards the exit
            if abs(proposed_position[0] - D/2) < abs(proposed_position[1] - D/2):
                proposed_position[0] = self.x
            else:
                proposed_position[1] = self.y

        self.x, self.y = np.clip(proposed_position, 0, D)

    def intersects_wall(self, proposed_position, D):
        cross_width = 1  # adjust as needed
        x, y = proposed_position
        if (((D/2 - cross_width/2 < x) & (x < D/2 + cross_width/2)).any() or ((D/2 - cross_width/2 < y) & (y < D/2 + cross_width/2)).any()):
            return True
        return False

