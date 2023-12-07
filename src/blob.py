# blob.py
import numpy as np


class Blob:
    def __init__(self, angle, x, y, threshold, min_velocity):
        self.angle = angle
        self.x = x
        self.y = y
        self.velocity = np.array([0.0, 0.0])
        self.threshold = threshold
        self.min_velocity = min_velocity

    def get_quadrant(self, D):
        if self.x >= D/2 and self.y >= D/2:
            return 1
        elif self.x < D/2 and self.y > D/2:
            return 2
        elif self.x < D/2 and self.y < D/2:
            return 3
        else:
            return 4

    def check_proximity(self, blobs, threshold, min_velocity):
        close_blobs = 0
        for other_blob in blobs:
            if other_blob is not self:
                distance = np.sqrt((self.x - other_blob.x)**2 + (self.y - other_blob.y)**2)
                if distance < threshold:
                    close_blobs += 1
        if close_blobs >= 2:
            self.velocity /= 2
            self.velocity = np.maximum(self.velocity, min_velocity)

    def update(self, exit_points, alarm_on, stepsize, eta, D, blobs, threshold, min_velocity):
        self.check_proximity(blobs, threshold, min_velocity)
        if alarm_on:
            quadrant = self.get_quadrant(D)
            if quadrant == 1:
                preferred_exit = exit_points[0]
            elif quadrant == 2:
                preferred_exit = exit_points[0]
            elif quadrant == 3:
                preferred_exit = exit_points[2]
            else:
                preferred_exit = exit_points[1]

            exit_direction = np.arctan2(preferred_exit[1] - self.y, preferred_exit[0] - self.x)
            self.angle = 0.5 * self.angle + 0.5 * exit_direction
            noise = (-eta / 2 + np.random.rand(1) * eta / 2)
            self.angle = self.angle + noise.item()
            v = self.velocity * np.array([np.cos(self.angle), np.sin(self.angle)])
        else:
            v = self.velocity

        proposed_position = np.array([self.x, self.y]) + stepsize * v
        if self.intersects_wall(proposed_position, D):
            self.angle += np.pi / 4
            v = self.velocity * np.array([np.cos(self.angle), np.sin(self.angle)])
            proposed_position[0] = self.x
            proposed_position[1] = self.y

        self.x, self.y = np.clip(proposed_position, 0, D)

    def intersects_wall(self, proposed_position, D):
        cross_width = 1  # adjust as needed
        x, y = proposed_position
        if (((D/2 - cross_width/2 < x) & (x < D/2 + cross_width/2)).any() or ((D/2 - cross_width/2 < y) & (y < D/2 + cross_width/2)).any()):
            return True
        return False

