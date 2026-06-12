"""
Numerical ODE Integrators (Euler, RK4, Dormand-Prince, Trapezoidal, Simpson).
"""

import numpy as np

def euler(f, t, y, h, *args):
    """Simple Euler integrator step."""
    return y + h * f(t, y, *args)

def rk4(f, t, y, h, *args):
    """Runge-Kutta 4th order integrator step."""
    k1 = f(t, y, *args)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1, *args)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2, *args)
    k4 = f(t + h, y + h * k3, *args)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

def rk45_step(f, t, y, h, *args):
    """Dormand-Prince (RK45) single step with embedded error estimate."""
    c = np.array([0.0, 1.5/5.0, 3.0/10.0, 4.0/5.0, 8.0/9.0, 1.0, 1.0])
    a = [
        [],
        [1.0/5.0],
        [3.0/40.0, 9.0/40.0],
        [44.0/45.0, -56.0/15.0, 32.0/9.0],
        [19372.0/6561.0, -25360.0/2187.0, 64448.0/6561.0, -212.0/729.0],
        [9017.0/3168.0, -355.0/33.0, 46732.0/5247.0, 49.0/176.0, -5103.0/18656.0],
        [35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0]
    ]
    b5 = np.array([35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0, 0.0])
    b4 = np.array([5179.0/57600.0, 0.0, 7571.0/16695.0, 393.0/640.0, -92097.0/339200.0, 187.0/2100.0, 1.0/40.0])
    
    k = []
    for i in range(7):
        ti = t + c[i] * h
        yi = y if i == 0 else y + h * sum(a[i][j] * k[j] for j in range(i))
        k.append(f(ti, yi, *args))
    
    y5 = y + h * sum(b5[i] * k[i] for i in range(7))
    y4 = y + h * sum(b4[i] * k[i] for i in range(7))
    err = np.linalg.norm(y5 - y4)
    return y5, err

def trapezoidal_int(f, a, b, n=1000):
    """∫f(x)dx via composite trapezoidal rule."""
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    return h * (0.5*y[0] + np.sum(y[1:-1]) + 0.5*y[-1])

def simpson_int(f, a, b, n=1000):
    """∫f(x)dx via composite Simpson's rule."""
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    return h/3.0 * (y[0] + 4.0*np.sum(y[1::2]) + 2.0*np.sum(y[2::2]) + y[-1])
