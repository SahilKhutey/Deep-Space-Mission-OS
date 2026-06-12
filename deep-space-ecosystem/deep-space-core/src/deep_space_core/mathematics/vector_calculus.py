"""
Vector calculus — gradient, divergence, curl, Laplacian.
"""
import numpy as np


def gradient_scalar(f, point, h=1e-6):
    x, y, z = point
    dfdx = (f(x+h, y, z) - f(x-h, y, z))/(2*h)
    dfdy = (f(x, y+h, z) - f(x, y-h, z))/(2*h)
    dfdz = (f(x, y, z+h) - f(x, y, z-h))/(2*h)
    return np.array([dfdx, dfdy, dfdz])


def divergence(F, point, h=1e-6):
    x, y, z = point
    Fx, Fy, Fz = F
    return ((Fx(x+h,y,z) - Fx(x-h,y,z))/(2*h) +
            (Fy(x,y+h,z) - Fy(x,y-h,z))/(2*h) +
            (Fz(x,y,z+h) - Fz(x,y,z-h))/(2*h))


def curl(F, point, h=1e-6):
    x, y, z = point
    Fx, Fy, Fz = F
    return np.array([
        (Fz(x,y+h,z) - Fz(x,y-h,z))/(2*h) - (Fy(x,y,z+h) - Fy(x,y,z-h))/(2*h),
        (Fx(x,y,z+h) - Fx(x,y,z-h))/(2*h) - (Fz(x+h,y,z) - Fz(x-h,y,z))/(2*h),
        (Fy(x+h,y,z) - Fy(x-h,y,z))/(2*h) - (Fx(x,y+h,z) - Fx(x,y-h,z))/(2*h)
    ])


def laplacian_scalar(f, point, h=1e-5):
    x, y, z = point
    return ((f(x+h,y,z) - 2*f(x,y,z) + f(x-h,y,z))/h**2 +
            (f(x,y+h,z) - 2*f(x,y,z) + f(x,y-h,z))/h**2 +
            (f(x,y,z+h) - 2*f(x,y,z) + f(x,y,z-h))/h**2)
