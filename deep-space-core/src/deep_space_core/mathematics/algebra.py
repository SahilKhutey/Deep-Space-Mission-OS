"""
Algebraic solvers and equations for deep space engineering.
Includes rocket equation and basic solver helpers.
"""

import numpy as np
from deep_space_core.constants import G0

def rocket_equation_delta_v(Isp, m0, mf):
    """
    Computes delta-V from rocket equation.
    dv = Isp * g0 * ln(m0 / mf)
    """
    if mf <= 0 or m0 <= 0 or m0 < mf:
        raise ValueError("Masses must be positive, and initial mass must be >= final mass.")
    return Isp * G0 * np.log(m0 / mf)

def mass_ratio(Isp, dv):
    """
    Computes mass ratio (m0 / mf) from delta-V and Isp.
    m0/mf = exp(dv / (Isp * g0))
    """
    return np.exp(dv / (Isp * G0))

def propellant_mass(m0, mass_ratio):
    """
    Computes propellant mass required.
    mp = m0 * (1 - 1/mass_ratio)
    """
    if mass_ratio < 1.0:
        raise ValueError("Mass ratio must be >= 1.0")
    return m0 * (1.0 - 1.0 / mass_ratio)

def solve_quadratic(a, b, c):
    """
    Solves ax^2 + bx + c = 0.
    Returns roots (x1, x2).
    """
    disc = b**2 - 4*a*c
    if disc < 0:
        return float('nan'), float('nan')
    sqrt_disc = np.sqrt(disc)
    x1 = (-b + sqrt_disc) / (2*a)
    x2 = (-b - sqrt_disc) / (2*a)
    return x1, x2

def solve_linear_system(A, b):
    """
    Solves A x = b.
    """
    return np.linalg.solve(np.array(A), np.array(b))
