"""
Earth-Moon Trajectory Module
Computes position and velocity of the Moon relative to the Earth.
Based on standard lunar orbital elements, including nodal precession.
"""

import numpy as np
from core.constants import MU_EARTH, R_MOON, R_EARTH
from core.astrodynamics.keplerian import keplerian_to_cartesian, solve_kepler, true_anomaly


def get_moon_elements(jd):
    """
    Get Moon's orbital elements relative to the Earth at a given Julian Date (jd).
    Includes nodal precession and periapsis advancement.
    """
    # Days since J2000
    d = jd - 2451545.0

    # Semi-major axis (km, fixed)
    a = 384400.0

    # Eccentricity (average)
    e = 0.0549

    # Inclination to the Earth's equatorial plane (average, deg to rad)
    # The inclination of the Moon's orbit relative to the Earth's equator ranges from 18.3 to 28.6 degrees.
    # We use the average inclination of 23.44 (Earth axial tilt) + 5.15 = 28.59 degrees.
    i = np.radians(28.58)

    # RAAN (longitude of ascending node precesses backwards with a period of 18.6 years)
    # -0.05295377 degrees per day
    raan = np.radians(125.0445 - 0.05295377 * d)

    # Longitude of periapsis advances with a period of 8.85 years
    # +0.11140353 degrees per day
    lon_peri = np.radians(318.15 + 0.11140353 * d)
    arg_p = lon_peri - raan

    # Mean anomaly
    # +13.06499296 degrees per day
    M = np.radians(134.9634 + 13.06499296 * d)

    return {
        "a": a,
        "e": e,
        "i": i,
        "raan": np.mod(raan, 2.0 * np.pi),
        "arg_p": np.mod(arg_p, 2.0 * np.pi),
        "M": np.mod(M, 2.0 * np.pi)
    }


def get_moon_state(jd, mu=MU_EARTH):
    """
    Get 3D position (km) and velocity (km/s) vectors of the Moon relative to the Earth.
    """
    elem = get_moon_elements(jd)
    E = solve_kepler(elem["M"], elem["e"])
    nu = true_anomaly(E, elem["e"])
    
    r_vec, v_vec = keplerian_to_cartesian(
        elem["a"], elem["e"], elem["i"], elem["raan"], elem["arg_p"], nu, mu
    )
    return r_vec, v_vec
