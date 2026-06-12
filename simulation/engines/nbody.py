"""
N-Body Gravitational Dynamics Engine
Propagates state under the gravitational influence of multiple celestial bodies.
Uses analytical ephemerides to obtain body positions, and gravitational softening to prevent singularities.
"""

import numpy as np
from core.constants import MU_SUN, MU_EARTH, MU_MARS, MU_MOON, R_EARTH, R_MARS, R_MOON, DAY_S
from core.astrodynamics.ephemeris.analytical import planet_state

# Active bodies database with their gravitational parameters and physical radii
BODIES = {
    "sun": {"mu": MU_SUN, "radius": 696340.0},
    "earth": {"mu": MU_EARTH, "radius": R_EARTH},
    "mars": {"mu": MU_MARS, "radius": R_MARS},
    "moon": {"mu": MU_MOON, "radius": R_MOON},
    "bennu": {"mu": 4.89e-9, "radius": 0.26},
    "psyche": {"mu": 1.5e-3, "radius": 113.0}
}

def nbody_dynamics(t, state, jd_start, bodies_list):
    """
    Computes derivatives for N-body heliocentric motion.
    
    Parameters
    ----------
    t           : float - Time since jd_start (seconds)
    state       : array-like - Heliocentric state [x, y, z, vx, vy, vz] (km, km/s)
    jd_start    : float - Initial Julian Date of the simulation
    bodies_list : list of str - Names of bodies to include in the gravitational field
                                (excluding Sun, which is always included as the center)
    
    Returns
    -------
    derivatives : numpy array - [vx, vy, vz, ax, ay, az]
    """
    r_sc = np.array(state[:3])
    v_sc = np.array(state[3:])
    
    # Julian date at current time step
    jd_current = jd_start + (t / DAY_S)
    
    # 1. Acceleration from Sun (origin of coordinate system)
    r_sun = np.linalg.norm(r_sc)
    if r_sun < 1.0:
        a_sun = np.zeros(3)
    else:
        # Soften near Sun just in case
        a_sun = -MU_SUN * r_sc / (r_sun**2 + BODIES["sun"]["radius"]**2)**1.5
        
    a_perturbations = np.zeros(3)
    
    # 2. Add perturbations from other bodies
    for body_name in bodies_list:
        body = body_name.lower().strip()
        if body not in BODIES:
            continue
            
        mu_body = BODIES[body]["mu"]
        radius_body = BODIES[body]["radius"]
        
        # Position of body relative to the Sun
        try:
            r_body, _ = planet_state(body, jd_current)
        except Exception:
            continue
            
        # Vector from body to spacecraft
        r_sc_body = r_sc - r_body
        r_sc_body_norm = np.linalg.norm(r_sc_body)
        
        # Acceleration of spacecraft due to the perturbing body (softened using physical radius)
        a_sc_body = -mu_body * r_sc_body / (r_sc_body_norm**2 + radius_body**2)**1.5
        
        # Acceleration of the Sun due to the perturbing body (indirect term)
        r_body_norm = np.linalg.norm(r_body)
        a_sun_body = -mu_body * r_body / (r_body_norm**2 + radius_body**2)**1.5
        
        # Net perturbing acceleration (direct + indirect)
        a_perturbations += (a_sc_body - a_sun_body)
        
    a_total = a_sun + a_perturbations
    
    return np.concatenate([v_sc, a_total])
