"""
Hohmann transfer trajectory calculations.
"""

import numpy as np

def hohmann_transfer(r1, r2, mu):
    """
    Computes Hohmann transfer between two circular, coplanar orbits.
    r1: initial orbit radius (km).
    r2: final orbit radius (km).
    mu: gravitational parameter (km^3/s^2).
    Returns dictionary with:
        dv1_km_s: first burn delta-V.
        dv2_km_s: second burn delta-V.
        total_dv_km_s: total transfer delta-V.
        tof_hours: time of flight in hours.
    """
    a_tx = (r1 + r2) / 2.0
    v_c1 = np.sqrt(mu / r1)
    v_tx1 = np.sqrt(mu * (2.0 / r1 - 1.0 / a_tx))
    dv1 = abs(v_tx1 - v_c1)
    
    v_c2 = np.sqrt(mu / r2)
    v_tx2 = np.sqrt(mu * (2.0 / r2 - 1.0 / a_tx))
    dv2 = abs(v_c2 - v_tx2)
    
    total_dv = dv1 + dv2
    tof = np.pi * np.sqrt((a_tx ** 3) / mu)
    tof_hours = tof / 3600.0
    
    return {
        "dv1_km_s": dv1,
        "dv2_km_s": dv2,
        "total_dv_km_s": total_dv,
        "tof_hours": tof_hours
    }
