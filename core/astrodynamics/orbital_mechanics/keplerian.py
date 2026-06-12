"""
Keplerian Orbital Mechanics
Implements Kepler's equation, Keplerian-Cartesian conversions, vis-viva, and orbital energy.
"""

import numpy as np
from core.constants import MU_SUN


def solve_kepler(M, e, tol=1e-11, max_iter=100):
    """
    Solve Kepler's Equation: M = E - e*sin(E)
    Using Newton-Raphson iteration with bisection fallback for robustness.
    """
    M = np.mod(M, 2 * np.pi)
    
    # Initial guess
    if e < 0.8:
        E = M
    else:
        E = np.pi

    # Newton-Raphson iteration
    for _ in range(max_iter):
        f = E - e * np.sin(E) - M
        fp = 1 - e * np.cos(E)
        dE = f / fp
        E_new = E - dE
        if abs(E_new - E) < tol:
            return E_new
        E = E_new

    # Fallback: Bisection method if Newton-Raphson fails to converge
    low, high = 0.0, 2 * np.pi
    for _ in range(max_iter):
        E = (low + high) / 2.0
        f = E - e * np.sin(E) - M
        if abs(f) < tol:
            return E
        if f > 0:
            high = E
        else:
            low = E
    return E


def true_anomaly(E, e):
    """Compute true anomaly (nu) from eccentric anomaly (E)."""
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2.0),
                        np.sqrt(1 - e) * np.cos(E / 2.0))
    return np.mod(nu, 2 * np.pi)


def eccentric_anomaly(nu, e):
    """Compute eccentric anomaly (E) from true anomaly (nu)."""
    E = 2 * np.arctan2(np.sqrt(1 - e) * np.sin(nu / 2.0),
                       np.sqrt(1 + e) * np.cos(nu / 2.0))
    return np.mod(E, 2 * np.pi)


def orbital_energy(a, mu=MU_SUN):
    """
    Specific orbital energy: ε = -μ / (2a)
    """
    if abs(a) < 1e-6:
        raise ValueError("Semi-major axis 'a' cannot be zero.")
    return -mu / (2.0 * a)


def vis_viva(r, a, mu=MU_SUN):
    """
    Vis-Viva equation: v = sqrt(μ * (2/r - 1/a))
    """
    val = mu * (2.0 / r - 1.0 / a)
    if val < 0:
        return 0.0
    return np.sqrt(val)


def orbital_period(a, mu=MU_SUN):
    """Kepler's third law: T = 2π * sqrt(a^3 / μ)"""
    if a <= 0:
        raise ValueError("Semi-major axis 'a' must be positive for closed orbits.")
    return 2.0 * np.pi * np.sqrt(a**3 / mu)


def keplerian_to_cartesian(a, e, i, raan, arg_p, nu, mu=MU_SUN):
    """
    Convert Keplerian elements to Cartesian position/velocity vectors in the inertial frame.
    All angles should be in radians.
    """
    denom = 1.0 + e * np.cos(nu)
    if abs(denom) < 1e-9:
        denom = 1e-9
    
    r = a * (1.0 - e**2) / denom
    
    p = a * (1.0 - e**2)
    if p < 0:
        p = abs(p)
    h = np.sqrt(mu * p)
    
    r_vec_orb = np.array([r * np.cos(nu), r * np.sin(nu), 0.0])
    v_vec_orb = np.array([
        -(mu / h) * np.sin(nu),
        (mu / h) * (e + np.cos(nu)),
        0.0
    ])

    cos_O, sin_O = np.cos(raan), np.sin(raan)
    cos_w, sin_w = np.cos(arg_p), np.sin(arg_p)
    cos_i, sin_i = np.cos(i), np.sin(i)

    R_raan = np.array([[ cos_O, -sin_O, 0.0],
                       [ sin_O,  cos_O, 0.0],
                       [    0.0,    0.0, 1.0]])

    R_inc  = np.array([[1.0,    0.0,     0.0],
                       [0.0,  cos_i,  -sin_i],
                       [0.0,  sin_i,   cos_i]])

    R_argp = np.array([[ cos_w, -sin_w, 0.0],
                       [ sin_w,  cos_w, 0.0],
                       [    0.0,    0.0, 1.0]])

    R = R_raan @ R_inc @ R_argp
    
    r_vec = R @ r_vec_orb
    v_vec = R @ v_vec_orb
    return r_vec, v_vec


def cartesian_to_keplerian(r_vec, v_vec, mu=MU_SUN):
    """
    Convert Cartesian position and velocity vectors to Keplerian elements.
    Returns: a, e, i, raan, arg_p, nu
    All angles are in radians.
    """
    r_vec = np.array(r_vec, dtype=float)
    v_vec = np.array(v_vec, dtype=float)
    
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    
    if r < 1e-6:
        raise ValueError("Position vector magnitude is near zero.")
        
    h_vec = np.cross(r_vec, v_vec)
    h = np.linalg.norm(h_vec)
    
    if h < 1e-9:
        raise ValueError("Angular momentum is zero (straight-line trajectory).")
        
    cos_i = h_vec[2] / h
    cos_i = np.clip(cos_i, -1.0, 1.0)
    i = np.arccos(cos_i)
    
    n_vec = np.cross([0.0, 0.0, 1.0], h_vec)
    n = np.linalg.norm(n_vec)
    
    if n > 1e-9:
        cos_raan = n_vec[0] / n
        cos_raan = np.clip(cos_raan, -1.0, 1.0)
        raan = np.arccos(cos_raan)
        if n_vec[1] < 0:
            raan = 2.0 * np.pi - raan
    else:
        raan = 0.0
        
    e_vec = (1.0 / mu) * ((v**2 - mu / r) * r_vec - np.dot(r_vec, v_vec) * v_vec)
    e = np.linalg.norm(e_vec)
    
    energy = 0.5 * v**2 - mu / r
    if abs(1.0 - e) > 1e-6:
        a = -mu / (2.0 * energy)
    else:
        a = np.inf
        
    if n > 1e-9:
        if e > 1e-9:
            dot_ne = np.dot(n_vec, e_vec) / (n * e)
            dot_ne = np.clip(dot_ne, -1.0, 1.0)
            arg_p = np.arccos(dot_ne)
            if e_vec[2] < 0:
                arg_p = 2.0 * np.pi - arg_p
        else:
            arg_p = 0.0
    else:
        if e > 1e-9:
            arg_p = np.arctan2(e_vec[1], e_vec[0])
            if arg_p < 0:
                arg_p = 2.0 * np.pi + arg_p
        else:
            arg_p = 0.0
            
    if e > 1e-9:
        dot_er = np.dot(e_vec, r_vec) / (e * r)
        dot_er = np.clip(dot_er, -1.0, 1.0)
        nu = np.arccos(dot_er)
        if np.dot(r_vec, v_vec) < 0:
            nu = 2.0 * np.pi - nu
    else:
        if n > 1e-9:
            dot_nr = np.dot(n_vec, r_vec) / (n * r)
            dot_nr = np.clip(dot_nr, -1.0, 1.0)
            nu = np.arccos(dot_nr)
            if r_vec[2] < 0:
                nu = 2.0 * np.pi - nu
        else:
            nu = np.arctan2(r_vec[1], r_vec[0])
            if nu < 0:
                nu = 2.0 * np.pi + nu
                
    return a, e, i, raan, arg_p, nu
