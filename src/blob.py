# blob.py
import numpy as np
import time


class Blob:
    def __init__(self, angle, x, y, threshold, min_velocity):
        self.angle = angle
        self.x = x
        self.y = y
        self.velocity = np.array([0.0, 0.0])
        self.threshold = threshold
        self.min_velocity = min_velocity
        self.last_exec_time = 0  # Add this line

    def average_neighbor_direction(self, blobs, radius):
        neighbor_count = 0
        avg_direction = np.array([0.0, 0.0])

        for other_blob in blobs:
            if other_blob is not self:
                distance = np.sqrt((self.x - other_blob.x)**2 + (self.y - other_blob.y)**2)
                if distance < radius:
                    avg_direction += np.array([np.cos(other_blob.angle), np.sin(other_blob.angle)])
                    neighbor_count += 1

        if neighbor_count > 0:
            avg_direction /= neighbor_count
            return np.arctan2(avg_direction[1], avg_direction[0])
        else:
            return self.angle

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

    # exit_point[0] = np.array([D/2, D])  # TOP
    # exit_point[1] = np.array([D, D/2])  # RIGHT
    # exit_point[2] = np.array([0, D/2])  # LEFT
    # exit_point[3] = np.array([D/2, 0])  # BOT
    def update(self, exit_points, checkpoints, alarm_on, stepsize, eta, D, blobs, threshold, min_velocity, max_velocity, turn_around_steps, exit_counter, exited_blobs, alignment_strength, neighbor_radius):
        # Check if the blob has reached the exit point
        if np.linalg.norm(np.array([self.x, self.y]) - exit_points[1]) < 0.25:
            exit_counter += 1
            exited_blobs.add(self)
            return
        self.check_proximity(blobs, threshold, min_velocity)
        if alarm_on:
            quadrant = self.get_quadrant(D)
            if quadrant == 3:
                if not hasattr(self, "reached_checkpoint_0"):
                    closest_cp = self.closest_checkpoint(checkpoints)
                    if (
                        np.linalg.norm(np.array([self.x, self.y]) - checkpoints[0])
                        < 3
                    ):
                        self.reached_checkpoint_0 = True
                    preferred_exit = (
                        exit_points[0]
                        if hasattr(self, "reached_checkpoint_0")
                        else closest_cp
                    )
                elif not hasattr(self, "reached_checkpoint_1"):
                    closest_cp = self.closest_checkpoint(checkpoints)
                    if (
                        np.linalg.norm(np.array([self.x, self.y]) - checkpoints[1])
                        < 3
                    ):
                        self.reached_checkpoint_1 = True
                    preferred_exit = (
                        exit_points[1]
                        if hasattr(self, "reached_checkpoint_1")
                        else closest_cp
                    )
                else:
                    preferred_exit = exit_points[0]
            elif quadrant == 1:
                preferred_exit = exit_points[0]
            elif quadrant == 2:
                preferred_exit = exit_points[0]
            elif quadrant == 4:
                preferred_exit = exit_points[1]
            else:
                preferred_exit = exit_points[0]

            exit_direction = np.arctan2(
                preferred_exit[1] - self.y, preferred_exit[0] - self.x
            )

            # Update the angle based on the average direction of neighbors
            avg_neighbor_dir = self.average_neighbor_direction(blobs, neighbor_radius)
            self.angle = (1 - alignment_strength) * self.angle + alignment_strength * avg_neighbor_dir


            if np.linalg.norm(self.velocity) > max_velocity:
                second_closest_exit = self.get_second_closest_exit(exit_points)
                if hasattr(self, "turn_around_count") and self.turn_around_count > 0:
                    exit_direction = np.arctan2(
                        second_closest_exit[1] - self.y, second_closest_exit[0] - self.x
                    )
                    self.angle = 0.5 * self.angle + 0.5 * exit_direction
                    self.angle = self.angle
                    v = (
                        self.velocity
                        * 0.5
                        * np.array([np.cos(self.angle), np.sin(self.angle)])
                    )
                    self.turn_around_count -= 1
                else:

                    current_time = time.time()
                    if current_time - self.last_exec_time >= 10:  # Check if 5 seconds have passed
                        self.turn_around_count = turn_around_steps
                        exit_direction = np.arctan2(
                            preferred_exit[1] - self.y, preferred_exit[0] - self.x
                        )

                        self.last_exec_time = current_time  # Update the timestamp

            self.angle = 0.5 * self.angle + 0.5 * exit_direction
            v = self.velocity * np.array([np.cos(self.angle), np.sin(self.angle)])

            proposed_position = np.array([self.x, self.y]) + stepsize * v
            if not self.intersects_wall(proposed_position):
                self.x, self.y = np.clip(proposed_position, 0, D)
            # else:
                # self.angle = 0.5 * self.angle + 0.5 * exit_direction
                # self.angle = self.angle
                # self.x, self.y = np.clip(proposed_position, 0, D)

    def intersects_wall(self, proposed_position):
        x, y = proposed_position
        return (2 <= x <= 23 and 12 <= y <= 13) or (2 <= y <= 23 and 12 <= x <= 13)

