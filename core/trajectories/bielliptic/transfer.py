"""
Bi-elliptic Transfer Trajectory calculations
Three-impulse transfer between two coplanar circular orbits.
Can be more fuel-efficient than Hohmann transfer when r2/r1 > 11.94 (depending on the boost radius rb).
"""

import numpy as np
from core.constants import MU_SUN

def bielliptic_transfer(r1, r2, rb, mu=MU_SUN):
    """
    Computes delta-v and time-of-flight for a bi-elliptic transfer.
    
    Parameters
    ----------
    r1 : float - Radius of departure circular orbit (km)
    r2 : float - Radius of arrival circular orbit (km)
    rb : float - Apoapsis radius of the intermediate transfer orbits (km)
                 Must be greater than both r1 and r2.
    mu : float - Central body gravitational parameter (km^3/s^2)
    
    Returns
    -------
    dict with:
        dv1_km_s      : First burn delta-v at departure r1 (km/s)
        dv2_km_s      : Second burn delta-v at apoapsis rb (km/s)
        dv3_km_s      : Third burn delta-v at arrival r2 (km/s)
        total_dv_km_s : Total delta-v budget (km/s)
        tof_seconds   : Total time of flight (seconds)
        tof_days      : Total time of flight (days)
    """
    if r1 <= 0 or r2 <= 0 or rb <= 0:
        raise ValueError("All orbital radii (r1, r2, rb) must be positive.")
    if rb < r1 or rb < r2:
        raise ValueError("Boost apoapsis radius rb must be greater than or equal to both r1 and r2.")
        
    # Semi-major axis of the first transfer ellipse (r1 -> rb)
    a1 = (r1 + rb) / 2.0
    # Semi-major axis of the second transfer ellipse (rb -> r2)
    a2 = (r2 + rb) / 2.0
    
    # Velocities in circular orbits
    v_circ1 = np.sqrt(mu / r1)
    v_circ2 = np.sqrt(mu / r2)
    
    # Velocities on first transfer ellipse
    v_trans1_peri = np.sqrt(mu * (2.0 / r1 - 1.0 / a1))
    v_trans1_apo  = np.sqrt(mu * (2.0 / rb - 1.0 / a1))
    
    # Velocities on second transfer ellipse
    v_trans2_apo  = np.sqrt(mu * (2.0 / rb - 1.0 / a2))
    v_trans2_peri = np.sqrt(mu * (2.0 / r2 - 1.0 / a2))
    
    # Delta-v burns
    dv1 = abs(v_trans1_peri - v_circ1)
    dv2 = abs(v_trans2_apo - v_trans1_apo)
    dv3 = abs(v_circ2 - v_trans2_peri)
    
    # Times of flight (half period of ellipse 1 + half period of ellipse 2)
    tof1 = np.pi * np.sqrt(a1**3 / mu)
    tof2 = np.pi * np.sqrt(a2**3 / mu)
    tof = tof1 + tof2
    
    return {
        "dv1_km_s": dv1,
        "dv2_km_s": dv2,
        "dv3_km_s": dv3,
        "total_dv_km_s": dv1 + dv2 + dv3,
        "tof_seconds": tof,
        "tof_days": tof / 86400.0
    }
