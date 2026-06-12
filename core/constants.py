"""
Physical and astronomical constants for DSMP
Source: NASA/JPL Standard Values
"""

# Gravitational Parameters (km^3/s^2)
MU_SUN = 1.32712440018e11
MU_EARTH = 3.986004418e5
MU_MOON = 4.9048695e3
MU_MARS = 4.282837e4

# Planet Radii (km)
R_EARTH = 6378.137
R_MOON = 1737.4
R_MARS = 3389.5

# SOI Radii (km)
SOI_EARTH = 9.29e5
SOI_MARS = 5.77e5

# Orbital Elements (km, km/s)
EARTH_ORBIT = {
    "a": 1.496e8,
    "e": 0.0167,
    "i": 0.0,
    "radius": 1.496e8
}

MARS_ORBIT = {
    "a": 2.279e8,
    "e": 0.0934,
    "i": 1.85,
    "radius": 2.279e8
}

# Reference values
G0 = 9.80665          # m/s^2 (Earth surface gravity)
AU = 1.496e8          # km
C = 299792.458        # km/s (speed of light)

# Time conversions
DAY_S = 86400.0       # seconds per day
YEAR_S = 365.25 * DAY_S
