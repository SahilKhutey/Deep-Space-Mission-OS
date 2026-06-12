"""
Universal variables Lambert solver.
"""

import numpy as np

def lambert_universal(r1, r2, TOF, mu, prograde=True):
    """
    Solves Lambert's problem using Universal Variables.
    r1: initial position vector (km).
    r2: final position vector (km).
    TOF: time of flight (seconds).
    mu: central body gravitational parameter (km^3/s^2).
    prograde: True for prograde trajectory, False for retrograde.
    Returns:
        v1: velocity at r1 (km/s).
        v2: velocity at r2 (km/s).
    """
    r1 = np.array(r1, dtype=float)
    r2 = np.array(r2, dtype=float)
    r1_mag = np.linalg.norm(r1)
    r2_mag = np.linalg.norm(r2)
    
    # Calculate delta-nu
    cos_dnu = np.dot(r1, r2) / (r1_mag * r2_mag)
    cos_dnu = min(max(cos_dnu, -1.0), 1.0)
    dnu = np.arccos(cos_dnu)
    
    # Cross product to determine orbital plane orientation
    cross_z = r1[0]*r2[1] - r1[1]*r2[0]
    if prograde:
        if cross_z < 0:
            dnu = 2.0 * np.pi - dnu
    else:
        if cross_z >= 0:
            dnu = 2.0 * np.pi - dnu
            
    A = np.sin(dnu) * np.sqrt((r1_mag * r2_mag) / (1.0 - cos_dnu))
    
    if A == 0.0:
        raise ValueError("A cannot be zero (180 degree transfer singularity).")
        
    def get_c_s(z):
        if z > 1e-5:
            sqrt_z = np.sqrt(z)
            c = (1.0 - np.cos(sqrt_z)) / z
            s = (sqrt_z - np.sin(sqrt_z)) / (sqrt_z**3)
        elif z < -1e-5:
            sqrt_nz = np.sqrt(-z)
            c = (np.cosh(sqrt_nz) - 1.0) / (-z)
            s = (np.sinh(sqrt_nz) - sqrt_nz) / (sqrt_nz**3)
        else:
            c = 1.0 / 2.0
            s = 1.0 / 6.0
        return c, s
        
    # Bisection solver for z
    z_min = -40.0
    z_max = 4.0 * np.pi**2 - 1e-2
    z = 0.0
    
    for _ in range(200):
        c, s = get_c_s(z)
        if c == 0:
            c = 1e-12
        y = r1_mag + r2_mag + A * (z * s - 1.0) / np.sqrt(c)
        
        if A > 0.0 and y < 0.0:
            # If y < 0, z is too small
            z_min = z
            z = 0.5 * (z_min + z_max)
            continue
            
        if y < 0:
            z_min = z
            z = 0.5 * (z_min + z_max)
            continue
            
        t = ( (y / c)**1.5 * s + A * np.sqrt(y) ) / np.sqrt(mu)
        
        if abs(t - TOF) < 1e-7:
            break
            
        if t < TOF:
            z_min = z
        else:
            z_max = z
        z = 0.5 * (z_min + z_max)
        
    c, s = get_c_s(z)
    y = r1_mag + r2_mag + A * (z * s - 1.0) / np.sqrt(c)
    
    f = 1.0 - y / r1_mag
    g = A * np.sqrt(y / mu)
    g_dot = 1.0 - y / r2_mag
    
    v1 = (r2 - f * r1) / g
    v2 = (g_dot * r2 - r1) / g
    
    return v1, v2
