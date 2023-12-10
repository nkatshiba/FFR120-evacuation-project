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

    def get_second_closest_exit(self, exit_points):
        distances = []
        for point in exit_points:
            distances.append(np.sqrt((self.x - point[0]) ** 2 + (self.y - point[1]) ** 2))

        if len(distances) >= 2:
            sorted_indices = np.argsort(distances)
            second_closest_index = sorted_indices[1]
            second_closest_exit = exit_points[second_closest_index]
            return second_closest_exit
        else:
            return None

    def check_proximity(self, blobs, threshold, min_velocity):
        close_blobs = 0
        for other_blob in blobs:
            if other_blob is not self:
                distance = np.sqrt((self.x - other_blob.x)**2 + (self.y - other_blob.y)**2)
                if distance < threshold:
                    close_blobs += 1
        if close_blobs >= 2:
            self.velocity /= 1.1
            self.velocity = np.maximum(self.velocity, min_velocity)

    def closest_checkpoint(self, checkpoints):
        distances = [np.linalg.norm(np.array([self.x, self.y]) - cp) for cp in checkpoints]
        closest_index = np.argmin(distances)
        return checkpoints[closest_index]

    def update(self, exit_points, checkpoints, alarm_on, stepsize, eta, D, blobs, threshold, min_velocity, max_velocity, turn_around_steps):
        self.check_proximity(blobs, threshold, min_velocity)

        if alarm_on:
            quadrant = self.get_quadrant(D)
            if quadrant in [1, 2]:
                preferred_exit = exit_points[0] if quadrant == 1 else exit_points[1]
            else:
                if quadrant == 3:
                    preferred_exit = exit_points[2]
                else:
                    preferred_exit = exit_points[1]

                if not hasattr(self, 'reached_checkpoint'):
                    closest_cp = self.closest_checkpoint(checkpoints)
                    if np.linalg.norm(np.array([self.x, self.y]) - closest_cp) < threshold:
                        self.reached_checkpoint = True
                    else:
                        preferred_exit = closest_cp

            exit_direction = np.arctan2(preferred_exit[1] - self.y, preferred_exit[0] - self.x)

            if np.linalg.norm(self.velocity) > max_velocity:
                second_closest_exit = self.get_second_closest_exit(exit_points)
                if hasattr(self, 'turn_around_count') and self.turn_around_count > 0:
                    exit_direction = np.arctan2(second_closest_exit[1] - self.y, second_closest_exit[0] - self.x)
                    self.angle = 0.5 * self.angle + 0.5 * exit_direction
                    self.angle = self.angle
                    v = self.velocity * 0.5 * np.array([np.cos(self.angle), np.sin(self.angle)])
                    self.turn_around_count -= 1
                else:
                    self.turn_around_count = turn_around_steps
                    exit_direction = np.arctan2(preferred_exit[1] - self.y, preferred_exit[0] - self.x)

            self.angle = 0.5 * self.angle + 0.5 * exit_direction
            self.angle = self.angle
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

