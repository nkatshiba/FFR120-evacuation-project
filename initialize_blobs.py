# initialize_blobs.py
import numpy as np
from blob import Blob


def initializeBlobs(N, D=25):
    blobs = []
    #####
    vertical_wall_x = D/2
    horizontal_wall_y = D/2
    for i in range(N):

        while True:
            angle = np.random.rand() * 2 * np.pi
            if i < N // 2:
                x = np.random.rand() * D / 2
                y = np.random.rand() * D / 3
            else:
                x = D / 2 + np.random.rand() * D / 2
                y = np.random.rand() * D

            if not ((abs(x-vertical_wall_x) < 0.5) or (abs(y-horizontal_wall_y) < 0.5)):
                break

        blobs.append(Blob(angle, x, y))
    #####
    return blobs