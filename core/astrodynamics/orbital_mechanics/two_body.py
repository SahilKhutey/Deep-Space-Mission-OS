"""
Two-Body Problem — Analytical solutions and vectors.
"""

import numpy as np
from core.constants import MU_SUN


def orbital_state_vector(a, e, i, raan, arg_p, nu, mu=MU_SUN):
    """Return position/velocity state vector from classical elements."""
    from core.astrodynamics.orbital_mechanics.keplerian import keplerian_to_cartesian
    return keplerian_to_cartesian(a, e, i, raan, arg_p, nu, mu)


def specific_energy(a, mu=MU_SUN):
    """Specific orbital energy: ε = -μ / (2a)"""
    if abs(a) < 1e-6:
        raise ValueError("Semi-major axis 'a' cannot be zero.")
    return -mu / (2.0 * a)


def semi_major_axis_from_energy(energy, mu=MU_SUN):
    """Recover semi-major axis from specific energy."""
    if abs(energy) < 1e-12:
        return np.inf
    return -mu / (2.0 * energy)


def eccentricity_vector(r_vec, v_vec, mu):
    """Compute eccentricity vector: e = 1/μ * ((v² - μ/r)r - (r·v)v)"""
    r_vec = np.array(r_vec, dtype=float)
    v_vec = np.array(v_vec, dtype=float)
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    if r < 1e-6:
        return np.zeros(3), 0.0
    e_vec = (1.0 / mu) * ((v**2 - mu / r) * r_vec - np.dot(r_vec, v_vec) * v_vec)
    return e_vec, np.linalg.norm(e_vec)


def specific_angular_momentum(r_vec, v_vec):
    """h = r × v"""
    return np.cross(r_vec, v_vec)
