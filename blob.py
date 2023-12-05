# blob.py
import numpy as np


class Blob:
    def __init__(self, angle, x, y):
        self.angle = angle
        self.x = x
        self.y = y
        self.velocity = np.array([0.0, 0.0])

    def update(self, exit_point, alarm_on, stepsize, eta, D):
        vertical_wall_x = D/2
        horizontal_wall_y = D/2
        if alarm_on:

            #####
            openings = np.array([[D/2,0], [1,D/2], [D-1,D/2], exit_point])
            valid_openings = [opening for opening in openings if opening[1] >= self.y]
            distances = np.linalg.norm(np.array(valid_openings)-np.array([self.x, self.y]), axis=1)
            closest_opening = valid_openings[np.argmin(distances)]

            exit_direction = np.arctan2(
                closest_opening[1] - self.y, closest_opening[0] - self.x)
            #####
            
            self.angle = 0.5 * self.angle + 0.5 * exit_direction
            noise = (-eta / 2 + np.random.rand(1) * eta / 2)
            self.angle = self.angle + noise.item()
            v = self.velocity * \
                np.array([np.cos(self.angle), np.sin(self.angle)])

            ##### Make sure blobs don't go over walls 
            next_x, next_y = np.clip(np.array([self.x, self.y]) + stepsize * v, 0, D)
            if not ((abs(self.x - vertical_wall_x) < 1.5) and (abs(self.y - horizontal_wall_y) < 1.5)):
                self.x, self.y = next_x, next_y
          
            #####

        else:
            v = self.velocity

        self.x, self.y = np.clip(
            np.array([self.x, self.y]) + stepsize * v, 0, D)