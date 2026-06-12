"""
Unit conversion helper functions for deep space calculations.
"""

import numpy as np
from deep_space_core.constants import AU

def km_to_m(km):
    return km * 1000.0

def m_to_km(m):
    return m / 1000.0

def deg_to_rad(deg):
    return np.deg2rad(deg)

def rad_to_deg(rad):
    return np.rad2deg(rad)

def day_to_s(days):
    return days * 86400.0

def s_to_day(s):
    return s / 86400.0

def au_to_km(au):
    return au * AU

def km_to_au(km):
    return km / AU
