"""Numerical integration of ODEs and quadratures."""
import numpy as np


def rk4(f, t, y, h, *args):
    """Runge-Kutta 4."""
    k1 = f(t, y, *args)
    k2 = f(t + h/2.0, y + h*k1/2.0, *args)
    k3 = f(t + h/2.0, y + h*k2/2.0, *args)
    k4 = f(t + h, y + h*k3, *args)
    return y + (h/6.0) * (k1 + 2.0*k2 + 2.0*k3 + k4)


def rk45_step(f, t, y, h, *args):
    """Dormand-Prince RK45 with embedded error estimate."""
    c = np.array([0, 1/5, 3/10, 4/5, 8/9, 1, 1])
    a = [
        [], [1/5], [3/40, 9/40], [44/45, -56/15, 32/9],
        [19372/6561, -25360/2187, 64448/6561, -212/729],
        [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656],
        [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84]
    ]
    b5 = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0])
    b4 = np.array([5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40])
    k = []
    for i in range(7):
        ti = t + c[i] * h
        yi = y if i == 0 else y + h * sum(a[i][j] * k[j] for j in range(i))
        k.append(f(ti, yi, *args))
    y5 = y + h * sum(b5[i] * k[i] for i in range(7))
    y4 = y + h * sum(b4[i] * k[i] for i in range(7))
    err = np.linalg.norm(y5 - y4)
    return y5, err


def trapezoidal(f, a, b, n=1000):
    x = np.linspace(a, b, n+1); y = f(x)
    h = (b - a) / n
    return h * (0.5*y[0] + np.sum(y[1:-1]) + 0.5*y[-1])


def simpson(f, a, b, n=1000):
    if n % 2: n += 1
    x = np.linspace(a, b, n+1); y = f(x)
    h = (b - a) / n
    return h/3.0 * (y[0] + 4.0*np.sum(y[1::2]) + 2.0*np.sum(y[2::2]) + y[-1])
