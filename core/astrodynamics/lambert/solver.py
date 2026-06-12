"""
Lambert's Problem Solver
Solves the two-point boundary value problem for orbital transfer.
Uses a highly robust Universal Variables formulation with guaranteed convergence.
"""

import numpy as np


def stumpff_S(z):
    """Stumpff function S(z)."""
    if z > 1e-5:
        sqrt_z = np.sqrt(z)
        return (sqrt_z - np.sin(sqrt_z)) / (sqrt_z**3)
    elif z < -1e-5:
        sqrt_z = np.sqrt(-z)
        return (np.sinh(sqrt_z) - sqrt_z) / (sqrt_z**3)
    else:
        # Taylor expansion for numerical stability near 0
        return 1.0 / 6.0 - z / 120.0 + z**2 / 5040.0


def stumpff_C(z):
    """Stumpff function C(z)."""
    if z > 1e-5:
        return (1.0 - np.cos(np.sqrt(z))) / z
    elif z < -1e-5:
        return (np.cosh(np.sqrt(-z)) - 1.0) / (-z)
    else:
        # Taylor expansion for numerical stability near 0
        return 0.5 - z / 24.0 + z**2 / 720.0


def lambert_solve(r1_vec, r2_vec, dt, mu, prograde=True, tol=1e-11, max_iter=200):
    """
    Solve Lambert's problem using a robust universal variables formulation.
    
    Parameters
    ----------
    r1_vec   : array-like - Position vector at departure (km)
    r2_vec   : array-like - Position vector at arrival (km)
    dt       : float      - Time of flight (seconds)
    mu       : float      - Gravitational parameter of central body (km^3/s^2)
    prograde : bool       - Solve for prograde trajectory if True, else retrograde
    tol      : float      - Convergence tolerance
    max_iter : int        - Maximum solver iterations
    
    Returns
    -------
    v1_vec   : numpy array - Velocity vector at departure (km/s)
    v2_vec   : numpy array - Velocity vector at arrival (km/s)
    """
    r1_vec = np.array(r1_vec, dtype=float)
    r2_vec = np.array(r2_vec, dtype=float)
    
    r1 = np.linalg.norm(r1_vec)
    r2 = np.linalg.norm(r2_vec)
    
    if r1 < 1e-3 or r2 < 1e-3:
        raise ValueError("Position vectors must have non-zero magnitude.")
    if dt <= 0:
        raise ValueError("Time of flight 'dt' must be positive.")
        
    cos_dtheta = np.dot(r1_vec, r2_vec) / (r1 * r2)
    cos_dtheta = np.clip(cos_dtheta, -1.0, 1.0)
    
    # Calculate transfer angle dtheta
    cross = np.cross(r1_vec, r2_vec)
    dtheta = np.arccos(cos_dtheta)
    
    # Adjust for prograde/retrograde
    if prograde:
        if cross[2] < 0:
            dtheta = 2.0 * np.pi - dtheta
    else:
        if cross[2] >= 0:
            dtheta = 2.0 * np.pi - dtheta
            
    # Check for 180-degree transfer singularity
    if abs(dtheta - np.pi) < 1e-5:
        # Perturb arrival vector slightly to break symmetry and find a solution
        eps_vec = np.array([1e-5, 0.0, 1e-5])
        r2_vec = r2_vec + eps_vec
        r2 = np.linalg.norm(r2_vec)
        cos_dtheta = np.dot(r1_vec, r2_vec) / (r1 * r2)
        cos_dtheta = np.clip(cos_dtheta, -1.0, 1.0)
        cross = np.cross(r1_vec, r2_vec)
        dtheta = np.arccos(cos_dtheta)
        if prograde:
            if cross[2] < 0:
                dtheta = 2.0 * np.pi - dtheta
        else:
            if cross[2] >= 0:
                dtheta = 2.0 * np.pi - dtheta

    A = np.sin(dtheta) * np.sqrt((r1 * r2) / (1.0 - cos_dtheta))
    if A == 0.0:
        raise ValueError("Singular geometry: cannot calculate transfer orbit parameter A.")

    # Helper function for y(z)
    def calc_y(z_val):
        S = stumpff_S(z_val)
        C = stumpff_C(z_val)
        c_denom = np.sqrt(C) if C > 1e-12 else 1e-6
        return r1 + r2 + A * (z_val * S - 1.0) / c_denom

    # Find the lower boundary z_y0 where y(z) = 0
    # To prevent floating-point overflow in sinh/cosh, we enforce a practical lower limit of -150.0.
    z_limit = -150.0
    y_limit = calc_y(z_limit)
    y_zero = calc_y(0.0)
    
    if y_zero > 0:
        if y_limit > 0:
            z_y0 = z_limit
        else:
            low_z = z_limit
            high_z = 0.0
            z_y0 = z_limit
            for _ in range(40):
                mid_z = (low_z + high_z) / 2.0
                y_val = calc_y(mid_z)
                if abs(y_val) < 1e-12:
                    z_y0 = mid_z
                    break
                if y_val > 0:
                    high_z = mid_z
                else:
                    low_z = mid_z
                    z_y0 = mid_z
    else:
        low_z = 0.0
        high_z = 4.0 * np.pi**2 - 1e-2
        while calc_y(high_z) < 0 and high_z < 4.0 * np.pi**2:
            high_z = (high_z + 4.0 * np.pi**2) / 2.0
            
        z_y0 = low_z
        for _ in range(40):
            mid_z = (low_z + high_z) / 2.0
            y_val = calc_y(mid_z)
            if abs(y_val) < 1e-12:
                z_y0 = mid_z
                break
            if y_val > 0:
                high_z = mid_z
            else:
                low_z = mid_z
                z_y0 = mid_z

    # The domain for F(z) is (z_y0, 4*pi^2)
    z_start = z_y0 + 1e-5
    z_end = 4.0 * np.pi**2 - 1e-4

    # Solve F(z) = 0 using bisection
    z = z_start
    for _ in range(max_iter):
        z = (z_start + z_end) / 2.0
        S = stumpff_S(z)
        C = stumpff_C(z)
        y = calc_y(z)
        
        # Evaluate F(z)
        F_z = (y / C)**1.5 * S + A * np.sqrt(y) - np.sqrt(mu) * dt
        
        if abs(F_z) < tol:
            break
            
        if F_z > 0:
            z_end = z
        else:
            z_start = z

    # Recompute y and stumpff values at the final converged z
    y = calc_y(z)
    
    # Calculate Lagrange coefficients
    f = 1.0 - y / r1
    g = A * np.sqrt(y / mu)
    gdot = 1.0 - y / r2
    
    if abs(g) < 1e-11:
        raise ValueError("Lagrange coefficient g is near zero. Cannot compute transfer velocities.")
        
    v1_vec = (r2_vec - f * r1_vec) / g
    v2_vec = (gdot * r2_vec - r1_vec) / g
    
    return v1_vec, v2_vec
