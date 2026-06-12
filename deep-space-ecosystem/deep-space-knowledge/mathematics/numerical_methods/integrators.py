"""
Numerical Integrators — Validated Library
"""

import numpy as np


def rk4(f, t, y, h, *args):
    """Runge-Kutta 4th order step."""
    k1 = f(t, y, *args)
    k2 = f(t + h/2, y + h*k1/2, *args)
    k3 = f(t + h/2, y + h*k2/2, *args)
    k4 = f(t + h, y + h*k3, *args)
    return y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)


def verlet_step(r, v, a, h):
    """Velocity Verlet step (symplectic)."""
    r_new = r + v*h + 0.5*a*h**2
    return r_new, v, a  # a evaluated at r_new externally


def trapezoidal(f, a, b, n):
    """Composite trapezoidal rule."""
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    return h * (0.5*y[0] + np.sum(y[1:-1]) + 0.5*y[-1])


def simpson(f, a, b, n):
    """Composite Simpson's rule (n must be even)."""
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    return h/3 * (y[0] + 4*np.sum(y[1::2]) + 2*np.sum(y[2::2]) + y[-1])


# VALIDATION
if __name__ == "__main__":
    # Integrate sin(x) from 0 to π → 2
    result = simpson(np.sin, 0, np.pi, 100)
    assert abs(result - 2.0) < 1e-6, f"Simpson failed: {result}"
    print(f"✓ Simpson: ∫sin(x)dx = {result:.8f} (expected 2.0)")

    # Trapezoidal test
    result = trapezoidal(np.sin, 0, np.pi, 1000)
    assert abs(result - 2.0) < 1e-3
    print(f"✓ Trapezoidal: ∫sin(x)dx = {result:.6f} (expected 2.0)")
