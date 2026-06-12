"""Analytical Keplerian ephemeris (no SPICE dependency)."""
import numpy as np
from ..constants import MU_SUN, AU
from ..astrodynamics.kepler import solve_kepler


PLANETS = {
    "Mercury": (0.387*AU, 0.2056, 87.969),
    "Venus":   (0.723*AU, 0.0068, 224.701),
    "Earth":   (1.000*AU, 0.0167, 365.256),
    "Mars":    (1.524*AU, 0.0934, 686.971),
    "Jupiter": (5.203*AU, 0.0489, 4332.59),
    "Saturn":  (9.537*AU, 0.0565, 10759.22),
}


def planet_state(name, t_days, mu=MU_SUN):
    a, e, period = PLANETS[name]
    M = 2.0*np.pi*t_days/period
    E = solve_kepler(M, e)
    nu = 2.0*np.arctan2(np.sqrt(1.0+e)*np.sin(E/2.0), np.sqrt(1.0-e)*np.cos(E/2.0))
    r = a*(1.0-e**2)/(1.0+e*np.cos(nu))
    v = np.sqrt(mu*(2.0/r - 1.0/a))
    x = r*np.cos(nu); y = r*np.sin(nu)
    return np.array([x, y, 0.0]), np.array([-v*np.sin(nu), v*np.cos(nu), 0.0])
