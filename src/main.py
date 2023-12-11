# main.py
from experiment import experiment


def run_simulation():
    N = 30  # Number of blobs (individuals)
    T = 1000  # Total number of time steps in the simulation
    R = 0.25  # Radius of the exit points
    D = 25  # Height and width of the layout (DxD)
    eta = 0.1  # Noise parameter for the blob movement
    stepsize = 2  # Step size for the blob movement
    threshold = 1  # Distance threshold for checking proximity between blobs
    min_velocity = 0.01  # Minimum velocity of the blobs
    alarm_delay = 50

    # Simulate
    experiment(N, T, R, D, eta, stepsize, threshold, min_velocity, alarm_delay)


if __name__ == "__main__":
    run_simulation()
