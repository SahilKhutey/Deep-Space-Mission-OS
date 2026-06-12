"""
Lambert's Problem Solver.
"""

import numpy as np

def stumpff_functions(z):
    """Computes Stumpff functions S(z) and C(z)."""
    if z > 1e-6:
        sz = np.sqrt(z)
        S = (np.sinh(sz) - sz) / (sz**3)
        C = (np.cosh(sz) - 1.0) / z
    elif z < -1e-6:
        sz = np.sqrt(-z)
        S = (sz - np.sin(sz)) / (sz**3)
        C = (1.0 - np.cos(sz)) / (-z)
    else:
        S = 1.0 / 6.0
        C = 0.5
    return S, C

def lambert_solver(r1, r2, dt, mu, prograde=True, tolerance=1e-10, max_iterations=200):
    """
    Lambert universal variable solver.
    """
    r1 = np.array(r1, dtype=float)
    r2 = np.array(r2, dtype=float)
    r1_mag = np.linalg.norm(r1)
    r2_mag = np.linalg.norm(r2)
    
    cos_theta = np.dot(r1, r2) / (r1_mag * r2_mag)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    theta = np.arccos(cos_theta)
    
    if not prograde:
        theta = 2.0 * np.pi - theta
        
    cross_prod = np.cross(r1, r2)
    A = np.sin(theta) * np.sqrt(r1_mag * r2_mag / (1.0 - cos_theta))
    if not prograde and cross_prod[2] >= 0:
        A = -A
        
    z = 0.0
    for _ in range(max_iterations):
        S, C = stumpff_functions(z)
        y = r1_mag + r2_mag + A * (z*S - 1.0) / np.sqrt(C)
        F = (y / S)**1.5 * S + A * np.sqrt(y) - np.sqrt(mu) * dt
        if abs(F) < tolerance:
            break
            
        # Derivative approximation
        dz = 1e-5
        S_p, _ = stumpff_functions(z + dz)
        y_p = r1_mag + r2_mag + A * ((z+dz)*S_p - 1.0) / np.sqrt(_)
        F_p = (y_p / S_p)**1.5 * S_p + A * np.sqrt(y_p) - np.sqrt(mu) * dt
        dF = (F_p - F) / dz
        if abs(dF) < 1e-30:
            break
        z -= F / dF
        
    # Recompute Lagrange coefficients
    S, C = stumpff_functions(z)
    y = r1_mag + r2_mag + A * (z*S - 1.0) / np.sqrt(C)
    
    f = 1.0 - y / r1_mag
    g = A * np.sqrt(y / mu)
    gdot = 1.0 - y / r2_mag
    
    v1 = (r2 - f * r1) / g
    v2 = (gdot * r2 - r1) / g
    return v1, v2
