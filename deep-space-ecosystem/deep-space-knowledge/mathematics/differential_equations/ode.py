"""
Ordinary Differential Equations (ODEs) for satellite motion and propagations.
"""

import numpy as np

def two_body_ode(t, state, mu):
    """
    Standard two-body geocentric/heliocentric equations of motion:
    d²r/dt² = -mu * r / r³
    """
    r_vec = state[:3]
    v_vec = state[3:]
    r_norm = np.linalg.norm(r_vec)
    if r_norm < 1e-6:
        a_vec = np.zeros(3)
    else:
        a_vec = -mu * r_vec / r_norm**3
    return np.concatenate([v_vec, a_vec])

def harmonic_oscillator_ode(t, state, k_over_m=1.0):
    """
    Simple harmonic oscillator:
    ẍ + (k/m)*x = 0
    state = [x, v]
    """
    x, v = state
    return np.array([v, -k_over_m * x])
