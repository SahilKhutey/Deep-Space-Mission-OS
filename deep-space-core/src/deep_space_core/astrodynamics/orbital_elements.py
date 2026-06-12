"""
Astrodynamics utilities: Keplerian <-> Cartesian conversions, vis-viva, energy.
"""

import numpy as np

def vis_viva(r, a, mu):
    """
    Vis-viva equation: v = sqrt(mu * (2/r - 1/a))
    """
    return np.sqrt(mu * (2.0 / r - 1.0 / a))

def specific_energy(a, mu):
    """
    Specific energy: epsilon = -mu / (2*a)
    """
    return -mu / (2.0 * a)

def solve_kepler(M, e, tol=1e-12, max_iter=100):
    """
    Solves Kepler's Equation E - e*sin(E) = M.
    """
    M = np.mod(M, 2.0 * np.pi)
    if e == 0:
        return M
    E = M if e < 0.8 else np.pi
    for _ in range(max_iter):
        f = E - e * np.sin(E) - M
        df = 1.0 - e * np.cos(E)
        dE = f / df
        E -= dE
        if abs(dE) < tol:
            break
    return E

def keplerian_to_cartesian(a, e, i, raan, arg_p, nu, mu):
    """
    Converts Keplerian elements to Cartesian position and velocity vectors.
    """
    p = a * (1.0 - e**2)
    r_mag = p / (1.0 + e * np.cos(nu))
    
    # Perifocal position and velocity
    r_pqw = np.array([r_mag * np.cos(nu), r_mag * np.sin(nu), 0.0])
    v_pqw = np.array([-np.sqrt(mu/p) * np.sin(nu), np.sqrt(mu/p) * (e + np.cos(nu)), 0.0])
    
    # Transformation matrices
    c_raan, s_raan = np.cos(raan), np.sin(raan)
    c_i, s_i = np.cos(i), np.sin(i)
    c_arg, s_arg = np.cos(arg_p), np.sin(arg_p)
    
    R = np.zeros((3, 3))
    R[0, 0] = c_raan * c_arg - s_raan * s_arg * c_i
    R[0, 1] = -c_raan * s_arg - s_raan * c_arg * c_i
    R[0, 2] = s_raan * s_i
    R[1, 0] = s_raan * c_arg + c_raan * s_arg * c_i
    R[1, 1] = -s_raan * s_arg + c_raan * c_arg * c_i
    R[1, 2] = -c_raan * s_i
    R[2, 0] = s_arg * s_i
    R[2, 1] = c_arg * s_i
    R[2, 2] = c_i
    
    r_ijk = R.dot(r_pqw)
    v_ijk = R.dot(v_pqw)
    return r_ijk, v_ijk

def cartesian_to_keplerian(r, v, mu):
    """
    Converts Cartesian position and velocity vectors to Keplerian orbital elements.
    Returns: a, e, i, raan, arg_p, nu
    """
    r_vec = np.array(r, dtype=float)
    v_vec = np.array(v, dtype=float)
    r_mag = np.linalg.norm(r_vec)
    v_mag = np.linalg.norm(v_vec)
    
    h_vec = np.cross(r_vec, v_vec)
    h_mag = np.linalg.norm(h_vec)
    
    # Inclination
    i = np.arccos(h_vec[2] / h_mag)
    
    # Node vector
    n_vec = np.cross([0.0, 0.0, 1.0], h_vec)
    n_mag = np.linalg.norm(n_vec)
    
    if n_mag != 0:
        raan = np.arccos(n_vec[0] / n_mag)
        if n_vec[1] < 0:
            raan = 2.0 * np.pi - raan
    else:
        raan = 0.0
        
    # Eccentricity vector
    e_vec = ((v_mag**2 - mu/r_mag)*r_vec - np.dot(r_vec, v_vec)*v_vec) / mu
    e = np.linalg.norm(e_vec)
    
    # Semi-major axis
    energy = 0.5 * v_mag**2 - mu / r_mag
    if abs(energy) > 1e-12:
        a = -mu / (2.0 * energy)
    else:
        a = float('inf')
        
    # Argument of periapsis
    if n_mag != 0 and e > 1e-12:
        dot_n_e = np.dot(n_vec, e_vec) / (n_mag * e)
        # Handle rounding errors
        dot_n_e = min(max(dot_n_e, -1.0), 1.0)
        arg_p = np.arccos(dot_n_e)
        if e_vec[2] < 0:
            arg_p = 2.0 * np.pi - arg_p
    else:
        arg_p = 0.0
        
    # True anomaly
    if e > 1e-12:
        dot_e_r = np.dot(e_vec, r_vec) / (e * r_mag)
        dot_e_r = min(max(dot_e_r, -1.0), 1.0)
        nu = np.arccos(dot_e_r)
        if np.dot(r_vec, v_vec) < 0:
            nu = 2.0 * np.pi - nu
    else:
        if n_mag != 0:
            dot_n_r = np.dot(n_vec, r_vec) / (n_mag * r_mag)
            dot_n_r = min(max(dot_n_r, -1.0), 1.0)
            nu = np.arccos(dot_n_r)
            if r_vec[2] < 0:
                nu = 2.0 * np.pi - nu
        else:
            nu = np.arctan2(r_vec[1], r_vec[0])
            if nu < 0:
                nu += 2.0 * np.pi
                
    return a, e, i, raan, arg_p, nu
