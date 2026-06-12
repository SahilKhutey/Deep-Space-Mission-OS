"""
Hohmann and Bi-elliptic Transfer Calculations
Includes coplanar transfers and transfers combined with inclination changes.
"""

import numpy as np
from core.constants import MU_SUN, R_EARTH, R_MOON


def hohmann_transfer(r1, r2, mu=MU_SUN):
    """
    Compute Hohmann transfer delta-Vs between two circular, coplanar orbits.
    
    Parameters
    ----------
    r1 : float - Initial orbit radius (km)
    r2 : float - Final orbit radius (km)
    mu : float - Central body gravitational parameter (km^3/s^2)
    
    Returns
    -------
    dict containing burn delta-Vs, total delta-V, and transfer duration.
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbital radii must be positive.")
        
    a_transfer = (r1 + r2) / 2.0

    # Initial orbit velocity and transfer ellipse velocity at periapsis
    v1_initial = np.sqrt(mu / r1)
    v1_transfer = np.sqrt(mu * (2.0 / r1 - 1.0 / a_transfer))
    dv1 = abs(v1_transfer - v1_initial)

    # Final orbit velocity and transfer ellipse velocity at apoapsis
    v2_transfer = np.sqrt(mu * (2.0 / r2 - 1.0 / a_transfer))
    v2_final = np.sqrt(mu / r2)
    dv2 = abs(v2_final - v2_transfer)

    # Transfer time (half the period of the transfer ellipse)
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
    A three-burn transfer: circular r1 -> elliptical rb -> elliptical r2 -> circular r2.
    Can be more fuel-efficient than Hohmann if r2/r1 > 11.94 and rb is large.
    
    Parameters
    ----------
    r1 : float - Initial orbit radius (km)
    rb : float - Intermediate apoapsis radius (km), must be > r2 and > r1
    r2 : float - Final orbit radius (km)
    mu : float - Central body gravitational parameter (km^3/s^2)
    """
    if rb <= r1 or rb <= r2:
        raise ValueError("Intermediate radius 'rb' must be larger than both 'r1' and 'r2'.")

    # Orbit 1: r1
    v1 = np.sqrt(mu / r1)
    
    # Transfer 1: ellipse from r1 to rb
    a1 = (r1 + rb) / 2.0
    v1_trans1 = np.sqrt(mu * (2.0 / r1 - 1.0 / a1))
    dv1 = abs(v1_trans1 - v1)
    
    v_ap1 = np.sqrt(mu * (2.0 / rb - 1.0 / a1))

    # Transfer 2: ellipse from rb to r2
    a2 = (r2 + rb) / 2.0
    v_ap2 = np.sqrt(mu * (2.0 / rb - 1.0 / a2))
    
    # Second burn (at apoapsis rb)
    dv2 = abs(v_ap2 - v_ap1)
    
    v2_trans2 = np.sqrt(mu * (2.0 / r2 - 1.0 / a2))
    
    # Orbit 2: r2
    v2 = np.sqrt(mu / r2)
    
    # Third burn (at periapsis r2)
    dv3 = abs(v2 - v2_trans2)

    total_dv = dv1 + dv2 + dv3
    
    # Transfer time: half the period of each ellipse
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
    The inclination change is split or performed at the second burn (cheapest due to lower velocity).
    
    Parameters
    ----------
    r1      : float - Initial orbit radius (km)
    r2      : float - Final orbit radius (km)
    delta_i : float - Inclination change (radians)
    mu      : float - Central body gravitational parameter (km^3/s^2)
    """
    a_transfer = (r1 + r2) / 2.0

    v1_initial = np.sqrt(mu / r1)
    v1_transfer = np.sqrt(mu * (2.0 / r1 - 1.0 / a_transfer))
    
    # Burn 1: pure coplanar expansion at periapsis
    dv1 = abs(v1_transfer - v1_initial)

    # Burn 2: coplanar circularization + inclination change at apoapsis
    # apoapsis velocity of transfer orbit:
    v2_transfer = np.sqrt(mu * (2.0 / r2 - 1.0 / a_transfer))
    v2_final = np.sqrt(mu / r2)
    
    # Law of Cosines for combined velocity change vector
    dv2 = np.sqrt(v2_transfer**2 + v2_final**2 - 2.0 * v2_transfer * v2_final * np.cos(delta_i))

    transfer_time = np.pi * np.sqrt(a_transfer**3 / mu)

    return {
        "dv1": dv1,
        "dv2": dv2,
        "total_dv": dv1 + dv2,
        "transfer_time_s": transfer_time,
        "transfer_time_days": transfer_time / 86400.0
    }


def leo_to_lunar_transfer(leo_alt=300.0, mu_earth=3.986004418e5, r_earth=6378.137):
    """
    Calculate approximate LEO to Lunar transfer delta-Vs.
    Includes escape from Earth LEO, transfer orbit injection (TLI), and lunar orbit insertion (LOI).
    """
    r_leo = r_earth + leo_alt
    r_moon = 384400.0  # Average distance from Earth to Moon (km)

    # TLI delta-V: Hohmann transfer from Earth to Moon's orbit
    a_trans = (r_leo + r_moon) / 2.0
    v_leo = np.sqrt(mu_earth / r_leo)
    v_tli = np.sqrt(mu_earth * (2.0 / r_leo - 1.0 / a_trans))
    dv_tli = v_tli - v_leo

    # LOI delta-V: capture into a circular lunar orbit
    # We estimate arrival velocity relative to Moon
    v_arr_earth_frame = np.sqrt(mu_earth * (2.0 / r_moon - 1.0 / a_trans))
    v_moon_earth_frame = np.sqrt(mu_earth / r_moon)
    
    # Hyperbolic excess velocity at the Moon
    v_inf_lunar = abs(v_arr_earth_frame - v_moon_earth_frame)
    
    # Moon's gravity parameters
    mu_moon = 4.9048695e3
    r_lunar_orbit = 1737.4 + 100.0  # 100 km altitude lunar orbit
    
    # Velocity on lunar orbit insertion hyperbola at periapsis
    v_per_hyperbola = np.sqrt(v_inf_lunar**2 + 2.0 * mu_moon / r_lunar_orbit)
    v_lunar_circular = np.sqrt(mu_moon / r_lunar_orbit)
    dv_loi = v_per_hyperbola - v_lunar_circular

    return {
        "leo_injection_dv": 9.4,  # km/s (typical surface to LEO launch)
        "tli_dv": dv_tli,
        "loi_dv": dv_loi,
        "total_dv": 9.4 + dv_tli + dv_loi,
        "transfer_time_days": 4.5
    }
