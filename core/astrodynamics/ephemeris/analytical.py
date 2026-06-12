"""
Analytical Ephemerides for Planets and Moon
Computes position and velocity of planets (relative to Sun) and Moon (relative to Earth).
Based on Keplerian elements and J2000 epoch.
"""

import numpy as np
from core.constants import MU_SUN, MU_EARTH, AU, DAY_S
from core.astrodynamics.keplerian import solve_kepler, true_anomaly, keplerian_to_cartesian

# Planetary orbital elements at J2000 (standard values)
PLANETS_REF = {
    "mercury": {
        "a": 0.38709893 * AU,
        "e": 0.20563069,
        "i": np.radians(7.00487),
        "raan": np.radians(48.33167),
        "arg_p": np.radians(77.45645),
        "M0": np.radians(174.796),
        "period_days": 87.969
    },
    "venus": {
        "a": 0.72333199 * AU,
        "e": 0.00677323,
        "i": np.radians(3.39471),
        "raan": np.radians(76.68069),
        "arg_p": np.radians(131.53298),
        "M0": np.radians(50.115),
        "period_days": 224.701
    },
    "earth": {
        "a": 1.00000261 * AU,
        "e": 0.01671123,
        "i": np.radians(-0.00001531),
        "raan": np.radians(0.0),
        "arg_p": np.radians(102.93768),
        "M0": np.radians(357.51768),
        "period_days": 365.256
    },
    "mars": {
        "a": 1.52371034 * AU,
        "e": 0.09339410,
        "i": np.radians(1.84969),
        "raan": np.radians(49.55954),
        "arg_p": np.radians(286.48130), # longitude of perihelion (336.04084) - raan
        "M0": np.radians(19.38816),
        "period_days": 686.971
    },
    "jupiter": {
        "a": 5.20336301 * AU,
        "e": 0.04839266,
        "i": np.radians(1.30530),
        "raan": np.radians(100.55615),
        "arg_p": np.radians(274.19770),
        "M0": np.radians(19.62),
        "period_days": 4332.59
    },
    "saturn": {
        "a": 9.53707032 * AU,
        "e": 0.05415060,
        "i": np.radians(2.48446),
        "raan": np.radians(113.71504),
        "arg_p": np.radians(338.26941),
        "M0": np.radians(317.02),
        "period_days": 10759.22
    }
}

def get_moon_elements(jd):
    """
    Get Moon's orbital elements relative to the Earth at a given Julian Date (jd).
    Includes nodal precession and periapsis advancement.
    """
    d = jd - 2451545.0
    a = 384400.0  # km
    e = 0.0549
    i = np.radians(28.58)
    raan = np.radians(125.0445 - 0.05295377 * d)
    lon_peri = np.radians(318.15 + 0.11140353 * d)
    arg_p = lon_peri - raan
    M = np.radians(134.9634 + 13.06499296 * d)
    
    return {
        "a": a,
        "e": e,
        "i": i,
        "raan": np.mod(raan, 2.0 * np.pi),
        "arg_p": np.mod(arg_p, 2.0 * np.pi),
        "M": np.mod(M, 2.0 * np.pi)
    }

def get_planet_elements(planet_name, jd):
    """
    Get planet's orbital elements relative to the Sun at Julian Date jd.
    """
    name = planet_name.lower().strip()
    if name not in PLANETS_REF:
        raise ValueError(f"Unknown planet: {planet_name}")
    
    ref = PLANETS_REF[name]
    d = jd - 2451545.0
    
    # Simple linear advancement for mean anomaly
    n = 2 * np.pi / ref["period_days"]  # mean motion in rad/day
    M = ref["M0"] + n * d
    
    return {
        "a": ref["a"],
        "e": ref["e"],
        "i": ref["i"],
        "raan": ref["raan"],
        "arg_p": ref["arg_p"],
        "M": np.mod(M, 2.0 * np.pi)
    }

def planet_state(planet_name, jd, mu=MU_SUN):
    """
    Get 3D position (km) and velocity (km/s) vectors of the planet relative to the Sun.
    Special case for moon (relative to Earth).
    """
    name = planet_name.lower().strip()
    if name == "moon":
        elem = get_moon_elements(jd)
        mu_center = MU_EARTH
    else:
        elem = get_planet_elements(name, jd)
        mu_center = mu
        
    E = solve_kepler(elem["M"], elem["e"])
    nu = true_anomaly(E, elem["e"])
    
    r_vec, v_vec = keplerian_to_cartesian(
        elem["a"], elem["e"], elem["i"], elem["raan"], elem["arg_p"], nu, mu_center
    )
    return r_vec, v_vec
