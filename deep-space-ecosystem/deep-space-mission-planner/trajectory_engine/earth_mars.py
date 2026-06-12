"""
Heliocentric Ephemerides for Earth and Mars
Computes positions and velocities of Earth and Mars relative to the Sun.
Based on Keplerian elements and J2000 epoch.
"""

import numpy as np
from deep_space_core.constants import MU_SUN, AU, DAY_S
from deep_space_core.astrodynamics import keplerian_to_cartesian, solve_kepler, true_anomaly


def get_earth_elements(jd):
    """
    Get Earth's Keplerian orbital elements at a given Julian Date (jd).
    Returns a dict with: a (km), e, i (rad), raan (rad), arg_p (rad), M (rad)
    """
    T = (jd - 2451545.0) / 36525.0  # Centuries since J2000

    a_au = 1.00000261 - 0.00000003 * T
    a = a_au * AU
    e = 0.01671123 - 0.00003804 * T
    i = np.radians(-0.00001531 - 0.01294668 * T)
    raan = np.radians(0.0)  # Earth is reference plane
    lon_peri = np.radians(102.93768193 + 0.32327364 * T)
    arg_p = lon_peri - raan
    L = np.radians(100.46457166 + 35999.37244981 * T)
    M = L - lon_peri

    return {
        "a": a,
        "e": e,
        "i": i,
        "raan": raan,
        "arg_p": arg_p,
        "M": np.mod(M, 2.0 * np.pi)
    }


def get_mars_elements(jd):
    """
    Get Mars's Keplerian orbital elements at a given Julian Date (jd).
    Returns a dict with: a (km), e, i (rad), raan (rad), arg_p (rad), M (rad)
    """
    T = (jd - 2451545.0) / 36525.0  # Centuries since J2000

    a_au = 1.52371034 + 0.00001847 * T
    a = a_au * AU
    e = 0.09339410 + 0.00007882 * T
    i = np.radians(1.84969142 - 0.00813131 * T)
    raan = np.radians(49.55953891 - 0.29257343 * T)
    lon_peri = np.radians(336.04084084 + 0.44383974 * T)
    arg_p = lon_peri - raan
    L = np.radians(355.45332 - 1.5e-5 * T + 19140.302684 * T)
    M = L - lon_peri

    return {
        "a": a,
        "e": e,
        "i": i,
        "raan": raan,
        "arg_p": arg_p,
        "M": np.mod(M, 2.0 * np.pi)
    }


def get_planet_state(planet_name, jd, mu=MU_SUN):
    """
    Calculate 3D position (km) and velocity (km/s) vectors of a planet relative to the Sun.
    """
    planet_name = planet_name.lower().strip()
    if planet_name == "earth":
        elem = get_earth_elements(jd)
    elif planet_name == "mars":
        elem = get_mars_elements(jd)
    else:
        raise ValueError(f"Planet '{planet_name}' ephemeris not supported.")

    E = solve_kepler(elem["M"], elem["e"])
    nu = true_anomaly(E, elem["e"])
    
    r_vec, v_vec = keplerian_to_cartesian(
        elem["a"], elem["e"], elem["i"], elem["raan"], elem["arg_p"], nu, mu
    )
    return r_vec, v_vec


def date_to_jd(year, month, day):
    """Convert YYYY, MM, DD calendar date to Julian Date (JD)."""
    if month <= 2:
        year -= 1
        month += 12
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    return jd


def jd_to_date(jd):
    """Convert Julian Date to calendar tuple (year, month, day)."""
    jd_f = jd + 0.5
    I_val = int(jd_f)
    F = jd_f - I_val
    if I_val > 2299160:
        A = int((I_val - 1867216.25) / 36524.25)
        B = I_val + 1 + A - int(A / 4)
    else:
        B = I_val
    C = B + 1524
    D = int((C - 122.1) / 365.25)
    E = int(365.25 * D)
    G = int((C - E) / 30.6001)
    day = C - E - int(30.6001 * G) + F
    if G < 14:
        month = G - 1
    else:
        month = G - 13
    if month > 2:
        year = D - 4716
    else:
        year = D - 4715
    return int(year), int(month), int(day)
