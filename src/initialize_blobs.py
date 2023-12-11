import numpy as np
from blob import Blob


def initializeBlobs(N, D, threshold, min_velocity):
    blobs = []
    for i in range(N):
        angle = np.random.rand() * 2 * np.pi
        if i < N // 4:
            x = np.random.rand() * D / 2
            y = np.random.rand() * D / 2
        elif i < N // 2:
            x = D / 2 + np.random.rand() * D / 2
            y = np.random.rand() * D / 2
        elif i < 3 * N // 4:
            x = np.random.rand() * D / 2
            y = D / 2 + np.random.rand() * D / 2
        else:
            x = D / 2 + np.random.rand() * D / 2
            y = D / 2 + np.random.rand() * D / 2
        blobs.append(Blob(angle, x, y, threshold, min_velocity))
    return blobs

