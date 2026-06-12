"""
Numerical calculus helper functions including derivatives, gradients,
integrations (trapezoidal, simpson rules).
"""

import numpy as np

def numerical_derivative(f, x, h=1e-5):
    """Computes df/dx using central difference."""
    return (f(x + h) - f(x - h)) / (2.0 * h)

def numerical_gradient(f, x, h=1e-5):
    """Computes gradient of scalar function f at vector x."""
    x = np.array(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (f(x_plus) - f(x_minus)) / (2.0 * h)
    return grad

def numerical_jacobian(f, x, h=1e-5):
    """Computes Jacobian matrix of vector function f at vector x."""
    x = np.array(x, dtype=float)
    fx = f(x)
    # Handle scalar function output
    if np.isscalar(fx):
        m = 1
    else:
        m = len(fx)
    n = len(x)
    J = np.zeros((m, n))
    for i in range(n):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        fx_plus = f(x_plus)
        fx_minus = f(x_minus)
        if m == 1:
            J[0, i] = (fx_plus - fx_minus) / (2.0 * h)
        else:
            J[:, i] = (fx_plus - fx_minus) / (2.0 * h)
    return J

def numerical_hessian(f, x, h=1e-4):
    """Computes Hessian matrix of scalar function f at vector x."""
    x = np.array(x, dtype=float)
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                x_plus = x.copy()
                x_minus = x.copy()
                x_plus[i] += h
                x_minus[i] -= h
                H[i, i] = (f(x_plus) - 2.0*f(x) + f(x_minus)) / (h**2)
            else:
                x_pp = x.copy(); x_pp[i] += h; x_pp[j] += h
                x_pm = x.copy(); x_pm[i] += h; x_pm[j] -= h
                x_mp = x.copy(); x_mp[i] -= h; x_mp[j] += h
                x_mm = x.copy(); x_mm[i] -= h; x_mm[j] -= h
                H[i, j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4.0 * h**2)
    return H

def trapezoidal(f, a, b, n=1000):
    """Integrates f from a to b using trapezoidal rule with n intervals."""
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])
    h = (b - a) / n
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])

def simpson(f, a, b, n=1000):
    """Integrates f from a to b using Simpson's 1/3 rule. n must be even."""
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = np.array([f(xi) for xi in x])
    h = (b - a) / n
    return h / 3.0 * (y[0] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-2:2]) + y[-1])
