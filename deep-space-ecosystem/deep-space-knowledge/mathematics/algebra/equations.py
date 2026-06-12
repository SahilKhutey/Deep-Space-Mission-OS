"""
Algebraic operations including quadratic equations and logarithmic rocket equations.
"""

import numpy as np

def solve_quadratic(a, b, c):
    """
    Solves the quadratic equation ax^2 + bx + c = 0.
    Returns real or complex roots.
    """
    a = float(a)
    b = float(b)
    c = float(c)
    if a == 0.0:
        if b == 0.0:
            raise ValueError("No solution possible.")
        return (-c / b,)
        
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        return ((-b + np.sqrt(discriminant)) / (2*a), (-b - np.sqrt(discriminant)) / (2*a))
    elif discriminant == 0:
        return (-b / (2*a),)
    else:
        # Complex roots
        return ((-b + 1j*np.sqrt(-discriminant)) / (2*a), (-b - 1j*np.sqrt(-discriminant)) / (2*a))

def tsiolkovsky_dv(isp, m0, mf, g0=9.80665):
    """
    Tsiolkovsky Rocket Equation:
    Delta-V = Isp * g0 * ln(m0 / mf)
    """
    if m0 <= 0 or mf <= 0:
        raise ValueError("Masses must be positive.")
    if m0 < mf:
        raise ValueError("Initial mass m0 must be greater than or equal to final mass mf.")
    return isp * g0 * np.log(m0 / mf)

def tsiolkovsky_mf(isp, m0, dv, g0=9.80665):
    """
    Computes final spacecraft mass after a Delta-V burn:
    mf = m0 * e^(-dv / (Isp * g0))
    """
    return m0 * np.exp(-dv / (isp * g0))
