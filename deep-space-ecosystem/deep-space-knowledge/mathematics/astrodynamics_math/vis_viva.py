"""
Vis-Viva equations and orbital energy calculations.
"""

import numpy as np

def vis_viva(r, a, mu):
    """
    Vis-Viva orbital velocity equation:
    v = sqrt(mu * (2/r - 1/a))
    """
    if r <= 0 or a == 0:
        raise ValueError("Invalid radius or semi-major axis.")
    val = mu * (2.0 / r - 1.0 / a)
    if val < 0.0:
        return 0.0
    return np.sqrt(val)

def orbital_energy(a, mu):
    """
    Specific energy of orbit:
    epsilon = -mu / (2*a)
    """
    if a == 0:
        raise ValueError("Semi-major axis cannot be zero.")
    return -mu / (2.0 * a)
