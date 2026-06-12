"""
Lyapunov stability criteria and Jacobian analysis.
"""

import numpy as np

def is_stable_equilibrium(df_dx, x_eq):
    """
    Checks 1D stability of dy/dt = f(x) at x_eq.
    If f'(x_eq) < 0, it is stable.
    """
    return df_dx(x_eq) < 0.0

def lyapunov_candidate(x):
    """V(x) = x^2, positive definite candidate."""
    return x**2
