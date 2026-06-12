"""
Spherical Trigonometry and coordinate conversions.
"""

import numpy as np

def spherical_distance(lat1, lon1, lat2, lon2, radius=6371.01):
    """
    Great-circle distance on a sphere of specified radius using Haversine formula.
    Angles in radians.
    """
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return radius * c

def spherical_triangle_side(a_side, b_side, gamma_angle):
    """
    Spherical Law of Cosines for sides:
    cos(c) = cos(a)*cos(b) + sin(a)*sin(b)*cos(C)
    All inputs and outputs in radians.
    """
    cos_c = np.cos(a_side) * np.cos(b_side) + np.sin(a_side) * np.sin(b_side) * np.cos(gamma_angle)
    return np.arccos(np.clip(cos_c, -1.0, 1.0))
