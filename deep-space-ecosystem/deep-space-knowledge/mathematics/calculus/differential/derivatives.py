"""
Numerical derivatives, gradients, Jacobians, and Hessians.
"""

import numpy as np

def derivative_1d(f, x, h=1e-6):
    """Central difference derivative: f'(x)"""
    return (f(x + h) - f(x - h)) / (2.0 * h)

def gradient(f, x, h=1e-6):
    """Calculates numerical gradient of scalar function f w.r.t. vector x."""
    x = np.array(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = np.copy(x); x_plus[i] += h
        x_minus = np.copy(x); x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2.0 * h)
    return grad

def jacobian(f, x, h=1e-6):
    """Computes Jacobian matrix of vector function f w.r.t. vector x."""
    x = np.array(x, dtype=float)
    y0 = f(x)
    m = len(y0)
    n = len(x)
    J = np.zeros((m, n))
    for i in range(n):
        x_plus = np.copy(x); x_plus[i] += h
        x_minus = np.copy(x); x_minus[i] -= h
        J[:, i] = (f(x_plus) - f(x_minus)) / (2.0 * h)
    return J
