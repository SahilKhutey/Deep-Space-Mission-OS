"""
Unit conversion functions.
All explicit, no auto-conversion to prevent silent bugs.
"""
from ..constants import G0


def km_to_m(x):   return x * 1000.0
def m_to_km(x):   return x / 1000.0
def deg_to_rad(x): return x * 3.141592653589793 / 180.0
def rad_to_deg(x): return x * 180.0 / 3.141592653589793
def km_s_to_m_s(x): return x * 1000.0
def m_s_to_km_s(x): return x / 1000.0
def day_to_s(x):  return x * 86400.0
def s_to_day(x):  return x / 86400.0
def year_to_s(x): return x * 365.25 * 86400.0
def au_to_km(x):  return x * 1.495978707e8
def km_to_au(x):  return x / 1.495978707e8
