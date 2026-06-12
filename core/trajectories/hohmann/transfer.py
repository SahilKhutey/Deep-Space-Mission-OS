"""
Hohmann Transfer Trajectory calculations
Minimum-energy, two-impulse transfer between two coplanar circular orbits.
"""

import numpy as np
from core.constants import MU_SUN

def hohmann_transfer(r1, r2, mu=MU_SUN):
    """
    Computes delta-v and time-of-flight for a Hohmann transfer.
    
    Parameters
    ----------
    r1 : float - Radius of departure circular orbit (km)
    r2 : float - Radius of arrival circular orbit (km)
    mu : float - Central body gravitational parameter (km^3/s^2)
    
    Returns
    -------
    dict with:
        dv1_km_s      : Departure delta-v (km/s)
        dv2_km_s      : Arrival delta-v (km/s)
        total_dv_km_s : Total delta-v budget (km/s)
        tof_seconds   : Time of flight (seconds)
        tof_days      : Time of flight (days)
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbital radii must be positive.")
        
    # Semi-major axis of the transfer ellipse
    a_trans = (r1 + r2) / 2.0
    
    # Velocities in circular orbits
    v_circ1 = np.sqrt(mu / r1)
    v_circ2 = np.sqrt(mu / r2)
    
    # Velocities at periapsis/apoapsis of the transfer ellipse
    v_trans1 = np.sqrt(mu * (2.0 / r1 - 1.0 / a_trans))
    v_trans2 = np.sqrt(mu * (2.0 / r2 - 1.0 / a_trans))
    
    # Delta-v burns
    dv1 = abs(v_trans1 - v_circ1)
    dv2 = abs(v_circ2 - v_trans2)
    
    # Time of flight (half of the orbital period of the transfer ellipse)
    tof = np.pi * np.sqrt(a_trans**3 / mu)
    
    return {
        "dv1_km_s": dv1,
        "dv2_km_s": dv2,
        "total_dv_km_s": dv1 + dv2,
        "tof_seconds": tof,
        "tof_days": tof / 86400.0
    }
