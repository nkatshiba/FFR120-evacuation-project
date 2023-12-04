# initialize_blobs.py
import numpy as np
from blob import Blob


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

