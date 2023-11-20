import numpy as np
import matplotlib.pyplot as plt

D = 25


def initializeCells(N, D=25):
    state0 = np.zeros(shape=(N*3,))
    state0[0::3] = np.random.rand(N,) * 2 * np.pi
    state0[1::3] = np.random.rand(N,) * D
    state0[2::3] = np.random.rand(N,) * D
    return state0


def update_rule_4(present, stepsize = 1, eta=0.1, D=25, R = 1, v0=0.03):
     future = np.copy(present)
     N = np.size(present) // 3
     neighborMeanAngles = np.zeros(N,) 
     for n in range(N):
        mytheta = np.mod(present[3*n], 2*np.pi)
        mypos = present[np.array([1,2]) + 3*n ]
        angleList = []
        for m in range(N):
            if m != n:
                themPos = present[np.array([1,2]) + 3*m ]
                if (np.linalg.norm(mypos - themPos) < R) :
                  angleList.append( present[3*m] )
        if len(angleList) > 0:
            neighborMeanAngles[n] = np.sum( np.array( angleList ) ) / len(angleList)
        noise = (-eta/2 + np.random.rand( 1 )* eta/2 )
        mytheta = mytheta + neighborMeanAngles[n] + noise.item()
        v = v0*np.array([np.cos(mytheta), np.sin(mytheta)])
        future[ np.array([1,2]) + 3*n ] = present[ np.array([1,2])+3*n ] + stepsize*v
        future[ np.array([1,2]) + 3*n ] = np.mod( future[ np.array([1,2]) + 3*n ], D)
     return(future)


def experiment(N=30, T=1000, R=1, D=25, eta=0.1, stepsize=1):
    state0 = initializeCells(N, D=D)
    trajectory = np.zeros(shape=(N*3, T))
    trajectory[:,0] = state0

    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()  # Create a figure and an axes
    ax.set_xlim(0, D)
    ax.set_ylim(0, D)

    for t in range(T-1):
        trajectory[:,t+1] = update_rule_4(trajectory[:,t], stepsize=stepsize, eta=eta, R=R, D=D)

        ax.clear()  # Clear the axes
        ax.set_xlim(0, D)
        ax.set_ylim(0, D)
        for i in range(0, len(trajectory[:,t+1]), 3):
            ax.plot(trajectory[i+1,t+1], trajectory[i+2,t+1], '.')  # Plot the current state
        plt.draw()  # Redraw the figure
        plt.pause(0.01)  # Pause for a short period

    plt.ioff()  # Turn off interactive mode
    return trajectory


def plotcells(state):
    ax = plt.axes()
    ax.set_xlim(0,D)
    ax.set_ylim(0,D)
    for i in range(0, len(state), 3):
        plt.plot(state[i+1], state[i+2], '.')
    plt.show()


trajectory = experiment()
plotcells(trajectory)
