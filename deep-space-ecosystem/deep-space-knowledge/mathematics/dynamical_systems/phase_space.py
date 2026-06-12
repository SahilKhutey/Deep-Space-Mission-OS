"""
Phase Space and equilibrium point trackers.
"""

import numpy as np

def find_equilibria(f, val_range, n=1000):
    """
    Finds approximate equilibrium points of 1D dynamical system dx/dt = f(x)
    in the given scalar range.
    """
    grid = np.linspace(val_range[0], val_range[1], n)
    equilibria = []
    for i in range(n-1):
        if f(grid[i]) * f(grid[i+1]) <= 0:
            equilibria.append(0.5 * (grid[i] + grid[i+1]))
    return equilibria
