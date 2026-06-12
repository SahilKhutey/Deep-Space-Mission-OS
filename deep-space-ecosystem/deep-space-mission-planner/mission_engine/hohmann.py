"""
Hohmann and Bi-elliptic Transfer Calculations
Includes coplanar transfers and transfers combined with inclination changes.
"""

import numpy as np
from deep_space_core.constants import MU_SUN, R_EARTH, R_MOON, MU_EARTH, MU_MOON


def hohmann_transfer(r1, r2, mu=MU_SUN):
    """
    Compute Hohmann transfer delta-Vs between two circular, coplanar orbits.
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbital radii must be positive.")
        
    a_transfer = (r1 + r2) / 2.0

    v1_initial = np.sqrt(mu / r1)
    v1_transfer = np.sqrt(mu * (2.0 / r1 - 1.0 / a_transfer))
    dv1 = abs(v1_transfer - v1_initial)

    v2_transfer = np.sqrt(mu * (2.0 / r2 - 1.0 / a_transfer))
    v2_final = np.sqrt(mu / r2)
    dv2 = abs(v2_final - v2_transfer)

    transfer_time = np.pi * np.sqrt(a_transfer**3 / mu)

    return {
        "dv1": dv1,
        "dv2": dv2,
        "total_dv": dv1 + dv2,
        "transfer_time_s": transfer_time,
        "transfer_time_days": transfer_time / 86400.0,
        "a_transfer_km": a_transfer
    }


def bi_elliptic_transfer(r1, rb, r2, mu=MU_SUN):
    """
    Compute Bi-elliptic transfer delta-Vs.
    """
    if rb <= r1 or rb <= r2:
        raise ValueError("Intermediate radius 'rb' must be larger than both 'r1' and 'r2'.")

    v1 = np.sqrt(mu / r1)
    a1 = (r1 + rb) / 2.0
    v1_trans1 = np.sqrt(mu * (2.0 / r1 - 1.0 / a1))
    dv1 = abs(v1_trans1 - v1)
    v_ap1 = np.sqrt(mu * (2.0 / rb - 1.0 / a1))

    a2 = (r2 + rb) / 2.0
    v_ap2 = np.sqrt(mu * (2.0 / rb - 1.0 / a2))
    dv2 = abs(v_ap2 - v_ap1)
    v2_trans2 = np.sqrt(mu * (2.0 / r2 - 1.0 / a2))
    v2 = np.sqrt(mu / r2)
    dv3 = abs(v2 - v2_trans2)

    total_dv = dv1 + dv2 + dv3
    
    t1 = np.pi * np.sqrt(a1**3 / mu)
    t2 = np.pi * np.sqrt(a2**3 / mu)
    transfer_time = t1 + t2

    return {
        "dv1": dv1,
        "dv2": dv2,
        "dv3": dv3,
        "total_dv": total_dv,
        "transfer_time_s": transfer_time,
        "transfer_time_days": transfer_time / 86400.0,
        "a_trans1_km": a1,
        "a_trans2_km": a2
    }


def hohmann_with_plane_change(r1, r2, delta_i, mu=MU_SUN):
    """
    Compute Hohmann transfer combined with an inclination change delta_i (in radians).
    """
    a_transfer = (r1 + r2) / 2.0
    v1_initial = np.sqrt(mu / r1)
    v1_transfer = np.sqrt(mu * (2.0 / r1 - 1.0 / a_transfer))
    dv1 = abs(v1_transfer - v1_initial)

    v2_transfer = np.sqrt(mu * (2.0 / r2 - 1.0 / a_transfer))
    v2_final = np.sqrt(mu / r2)
    dv2 = np.sqrt(v2_transfer**2 + v2_final**2 - 2.0 * v2_transfer * v2_final * np.cos(delta_i))

    transfer_time = np.pi * np.sqrt(a_transfer**3 / mu)

    return {
        "dv1": dv1,
        "dv2": dv2,
        "total_dv": dv1 + dv2,
        "transfer_time_s": transfer_time,
        "transfer_time_days": transfer_time / 86400.0
    }


def leo_to_lunar_transfer(leo_alt=300.0, mu_earth=MU_EARTH, r_earth=R_EARTH):
    """
    Calculate approximate LEO to Lunar transfer delta-Vs.
    """
    r_leo = r_earth + leo_alt
    r_moon = 384400.0  # Average distance from Earth to Moon (km)

    a_trans = (r_leo + r_moon) / 2.0
    v_leo = np.sqrt(mu_earth / r_leo)
    v_tli = np.sqrt(mu_earth * (2.0 / r_leo - 1.0 / a_trans))
    dv_tli = v_tli - v_leo

    v_arr_earth_frame = np.sqrt(mu_earth * (2.0 / r_moon - 1.0 / a_trans))
    v_moon_earth_frame = np.sqrt(mu_earth / r_moon)
    v_inf_lunar = abs(v_arr_earth_frame - v_moon_earth_frame)
    
    r_lunar_orbit = R_MOON + 100.0  # 100 km altitude lunar orbit
    v_per_hyperbola = np.sqrt(v_inf_lunar**2 + 2.0 * MU_MOON / r_lunar_orbit)
    v_lunar_circular = np.sqrt(MU_MOON / r_lunar_orbit)
    dv_loi = v_per_hyperbola - v_lunar_circular

    return {
        "leo_injection_dv": 9.4,  # km/s (typical surface to LEO launch)
        "tli_dv": dv_tli,
        "loi_dv": dv_loi,
        "total_dv": 9.4 + dv_tli + dv_loi,
        "transfer_time_days": 4.5
    }
