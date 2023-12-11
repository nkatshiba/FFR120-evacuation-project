# main.py
import logging
from experiment import experiment

logging.basicConfig(filename='simulation.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def run_simulation():
    results = []  # List to store simulation results

    # Run the simulation for different values of N
    for N in range(10, 111, 10):
        T = 1000
        R = 0.25
        D = 25
        eta = 0.1
        stepsize = 2
        threshold = 1
        min_velocity = 0.03
        alarm_delay = 1

        # Log the parameters
        logging.info(f"Parameters: N={N}, T={T}, R={R}, D={D}, eta={eta}, stepsize={stepsize}, "
                     f"threshold={threshold}, min_velocity={min_velocity}, alarm_delay={alarm_delay}")

        # Simulate
        escape_time, escape_time_80 = experiment(N, T, R, D, eta, stepsize, threshold, min_velocity, alarm_delay)

        # Store the result in the list
        results.append((N, escape_time, escape_time_80))

        # Log the result
        logging.info(f"Result: N={N}, Escape Time={escape_time}, Escape Time (80%)={escape_time_80}")

    # Print or use the results as needed
    print("Simulation Results:")
    for result in results:
        print(f"N: {result[0]}, Escape Time: {result[1]}, Escape Time (80%): {result[2]}")


if __name__ == "__main__":
    run_simulation()
