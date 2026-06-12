"""
Numerical integrations for energy and fuel consumption.
"""

import numpy as np

def trapezoidal(f, a, b, n=1000):
    """Trapezoidal integration rule over interval [a, b] with n subdivisions."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h * (0.5 * y[0] + np.sum(y[1:-1]) + 0.5 * y[-1])

def simpson(f, a, b, n=1000):
    """Simpson's integration rule over interval [a, b] with n subdivisions."""
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return (h / 3.0) * (y[0] + 4.0 * np.sum(y[1::2]) + 2.0 * np.sum(y[2::2]) + y[-1])
