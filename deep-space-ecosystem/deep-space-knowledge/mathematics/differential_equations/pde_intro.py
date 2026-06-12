"""
Introduction to Partial Differential Equations (PDEs) for heat transfer and plasma.
"""

import numpy as np

def heat_equation_1d(u_prev, alpha, dx, dt):
    """
    Solves 1D heat equation using explicit FTCS (Forward-Time Central-Space) finite difference:
    du/dt = alpha * d^2u/dx^2
    """
    n = len(u_prev)
    u_next = np.copy(u_prev)
    r = alpha * dt / dx**2
    if r >= 0.5:
        # FTCS is unstable for r >= 0.5
        pass
    for i in range(1, n-1):
        u_next[i] = u_prev[i] + r * (u_prev[i+1] - 2*u_prev[i] + u_prev[i-1])
    return u_next
