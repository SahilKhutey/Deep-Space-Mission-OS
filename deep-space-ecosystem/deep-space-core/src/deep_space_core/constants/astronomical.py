"""
NASA/JPL Standard Astronomical Constants
Source: JPL Planetary and Lunar Ephemeris DE421
"""
import numpy as np

# Gravitational parameters (km^3/s^2)
MU_SUN     = 1.32712440018e11
MU_MERCURY = 2.203209e4
MU_VENUS   = 3.24859e5
MU_EARTH   = 3.986004418e5
MU_MOON    = 4.9048695e3
MU_MARS    = 4.282837e4
MU_JUPITER = 1.26686534e8
MU_SATURN  = 3.7931187e7

# Body radii (km)
R_SUN     = 695700.0
R_MERCURY = 2439.7
R_VENUS   = 6051.8
R_EARTH   = 6378.137
R_MOON    = 1737.4
R_MARS    = 3389.5

# Spheres of influence (km)
SOI_EARTH = 9.29e5
SOI_MOON  = 6.61e4
SOI_MARS  = 5.77e5

# Reference
AU = 1.495978707e8  # km
C  = 299792.458     # km/s (speed of light)
G  = 6.67430e-20    # km^3/(kg·s^2)

# Earth surface gravity
G0 = 9.80665        # m/s^2

# Time constants
DAY_S = 86400.0
YEAR_S = 365.25 * DAY_S

