"""
Gravity Assist (Swing-by) Trajectory Calculations
Computes flyby mechanics, including turning angle and velocity vector changes.
"""

import numpy as np


def gravity_assist_delta_v(v_inf_in, v_inf_out, mu_planet, rp):
    """
    Compute ΔV and turning angle for a powered gravity assist.
    If it is unpowered, magnitude of v_inf is conserved, and ΔV = 0.
    
    Parameters
    ----------
    v_inf_in  : array-like - Incoming hyperbolic excess velocity vector (km/s)
    v_inf_out : array-like - Outgoing hyperbolic excess velocity vector (km/s)
    mu_planet : float      - Gravitational parameter of the flyby planet (km^3/s^2)
    rp        : float      - Periapsis altitude/radius of the flyby hyperbola (km)
    
    Returns
    -------
    delta_v    : float - Required powered maneuver velocity change (km/s)
    turn_angle : float - Hyperbolic turning angle (radians)
    """
    v_inf_in = np.array(v_inf_in, dtype=float)
    v_inf_out = np.array(v_inf_out, dtype=float)
    
    v_in_mag = np.linalg.norm(v_inf_in)
    v_out_mag = np.linalg.norm(v_inf_out)
    
    if v_in_mag < 1e-6 or v_out_mag < 1e-6:
        return 0.0, 0.0
        
    # Semi-major axis of incoming hyperbola
    a_in = -mu_planet / v_in_mag**2
    e_in = 1.0 - rp / a_in
    
    # Semi-major axis of outgoing hyperbola
    a_out = -mu_planet / v_out_mag**2
    e_out = 1.0 - rp / a_out
    
    # Calculate deflection angles (turn angle = delta_in/2 + delta_out/2)
    delta_in = 2.0 * np.arcsin(1.0 / e_in)
    delta_out = 2.0 * np.arcsin(1.0 / e_out)
    
    turn_angle = (delta_in + delta_out) / 2.0
    
    # Powered maneuver burn at periapsis
    # v_peri_in = sqrt(v_inf_in^2 + 2*mu/rp)
    # v_peri_out = sqrt(v_inf_out^2 + 2*mu/rp)
    v_peri_in = np.sqrt(v_in_mag**2 + 2.0 * mu_planet / rp)
    v_peri_out = np.sqrt(v_out_mag**2 + 2.0 * mu_planet / rp)
    
    delta_v = abs(v_peri_out - v_peri_in)
    return delta_v, turn_angle
