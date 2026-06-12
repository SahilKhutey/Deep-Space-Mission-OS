"""
Vector fields, gradients, curls, and divergences.
"""

import numpy as np

def divergence(F, pt, h=1e-6):
    """
    Computes numerical divergence of vector field F(pt) = [Fx, Fy, Fz] at pt = [x,y,z].
    """
    x, y, z = pt
    Fx = lambda val: F([val, y, z])[0]
    Fy = lambda val: F([x, val, z])[1]
    Fz = lambda val: F([x, y, val])[2]
    
    dfxdx = (Fx(x + h) - Fx(x - h)) / (2.0 * h)
    dfydy = (Fy(y + h) - Fy(y - h)) / (2.0 * h)
    dfzdz = (Fz(z + h) - Fz(z - h)) / (2.0 * h)
    return dfxdx + dfydy + dfzdz

def curl(F, pt, h=1e-6):
    """
    Computes numerical curl of vector field F(pt) = [Fx, Fy, Fz] at pt = [x,y,z].
    """
    x, y, z = pt
    
    Fz_y = lambda val: F([x, val, z])[2]
    Fy_z = lambda val: F([x, y, val])[1]
    
    Fx_z = lambda val: F([x, y, val])[0]
    Fz_x = lambda val: F([val, y, z])[2]
    
    Fy_x = lambda val: F([val, y, z])[1]
    Fx_y = lambda val: F([x, val, z])[0]
    
    cx = (Fz_y(y + h) - Fz_y(y - h)) / (2.0 * h) - (Fy_z(z + h) - Fy_z(z - h)) / (2.0 * h)
    cy = (Fx_z(z + h) - Fx_z(z - h)) / (2.0 * h) - (Fz_x(x + h) - Fz_x(x - h)) / (2.0 * h)
    cz = (Fy_x(x + h) - Fy_x(x - h)) / (2.0 * h) - (Fx_y(y + h) - Fx_y(y - h)) / (2.0 * h)
    
    return np.array([cx, cy, cz])
