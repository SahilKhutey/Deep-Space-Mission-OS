"""
J2 Perturbation Model
Calculates gravitational perturbations due to the Earth's oblateness (J2).
"""

import numpy as np
from core.constants import MU_EARTH, R_EARTH

J2_EARTH = 1.08262668e-3


def j2_acceleration(r_vec, mu=MU_EARTH, R=R_EARTH, J2=J2_EARTH):
    """
    Calculate J2 perturbation acceleration vector.
    
    Parameters
    ----------
    r_vec : array-like - Geocentric position vector (km)
    mu    : float      - Central body gravitational parameter (km^3/s^2)
    R     : float      - Central body radius (km)
    J2    : float      - Second zonal harmonic coefficient
    
    Returns
    -------
    a_j2  : numpy array - Perturbation acceleration vector (km/s^2)
    """
    r_vec = np.array(r_vec, dtype=float)
    r = np.linalg.norm(r_vec)
    
    if r < 1e-3:
        return np.zeros(3)
        
    x, y, z = r_vec
    
    # Standard J2 acceleration equations in inertial frame:
    # ax = -3/2 * J2 * mu * R^2 / r^5 * x * (1 - 5 * z^2 / r^2)
    # ay = -3/2 * J2 * mu * R^2 / r^5 * y * (1 - 5 * z^2 / r^2)
    # az = -3/2 * J2 * mu * R^2 / r^5 * z * (3 - 5 * z^2 / r^2)
    factor = 1.5 * J2 * mu * (R**2) / (r**5)
    
    ax = factor * x * (5.0 * (z**2) / (r**2) - 1.0)
    ay = factor * y * (5.0 * (z**2) / (r**2) - 1.0)
    az = factor * z * (5.0 * (z**2) / (r**2) - 3.0)
    
    return np.array([ax, ay, az])
