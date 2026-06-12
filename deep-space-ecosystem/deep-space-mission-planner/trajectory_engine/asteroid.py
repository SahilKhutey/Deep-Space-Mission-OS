"""
Asteroid Trajectory Module
Computes position and velocity of target asteroids (e.g., Bennu, Psyche) relative to the Sun.
Supports custom Keplerian parameters.
"""

import numpy as np
from deep_space_core.constants import MU_SUN, AU
from deep_space_core.astrodynamics import keplerian_to_cartesian, solve_kepler, true_anomaly


# Orbital elements for reference asteroids
# Epoch: J2000 (JD 2451545.0)
ASTEROIDS = {
    "bennu": {
        "a": 1.12639102 * AU,
        "e": 0.20374511,
        "i": np.radians(6.03494),
        "raan": np.radians(2.06087),
        "arg_p": np.radians(66.22306),
        "M0": np.radians(101.70379),
        "n": np.radians(360.0 / 436.6487)  # Mean motion (rad/day)
    },
    "psyche": {
        "a": 2.9244 * AU,
        "e": 0.1397,
        "i": np.radians(3.095),
        "raan": np.radians(150.2),
        "arg_p": np.radians(228.3),
        "M0": np.radians(95.4),
        "n": np.radians(360.0 / 1826.0)  # Mean motion (rad/day)
    }
}


def get_asteroid_elements(name_or_custom, jd):
    """
    Get asteroid orbital elements at Julian Date.
    name_or_custom can be a string ("bennu", "psyche") or a dict of custom elements.
    """
    d = jd - 2451545.0
    
    if isinstance(name_or_custom, str):
        name = name_or_custom.lower().strip()
        if name not in ASTEROIDS:
            raise ValueError(f"Asteroid '{name}' not found. Use 'bennu', 'psyche' or custom dict.")
        ref = ASTEROIDS[name]
    elif isinstance(name_or_custom, dict):
        ref = name_or_custom
    else:
        raise ValueError("Invalid asteroid specification. Expected name (str) or elements (dict).")

    # Propagate Mean Anomaly over time
    M = ref["M0"] + ref["n"] * d
    
    return {
        "a": ref["a"],
        "e": ref["e"],
        "i": ref["i"],
        "raan": ref["raan"],
        "arg_p": ref["arg_p"],
        "M": np.mod(M, 2.0 * np.pi)
    }


def get_asteroid_state(name_or_custom, jd, mu=MU_SUN):
    """
    Get 3D position (km) and velocity (km/s) vectors of the asteroid relative to the Sun.
    """
    elem = get_asteroid_elements(name_or_custom, jd)
    E = solve_kepler(elem["M"], elem["e"])
    nu = true_anomaly(E, elem["e"])
    
    r_vec, v_vec = keplerian_to_cartesian(
        elem["a"], elem["e"], elem["i"], elem["raan"], elem["arg_p"], nu, mu
    )
    return r_vec, v_vec
