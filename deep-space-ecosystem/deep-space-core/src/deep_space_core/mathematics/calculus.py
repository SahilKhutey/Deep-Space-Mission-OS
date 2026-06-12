"""
Differential and integral calculus.
"""
import numpy as np


def numerical_derivative(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2*h)


def numerical_gradient(f, x, h=1e-6):
    x = np.asarray(x, dtype=float)
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_p = x.copy(); x_p[i] += h
        x_m = x.copy(); x_m[i] -= h
        grad[i] = (f(x_p) - f(x_m)) / (2*h)
    return grad


def numerical_jacobian(F, x, h=1e-6):
    x = np.asarray(x, dtype=float)
    n = len(x); m = len(F(x))
    J = np.zeros((m, n))
    for i in range(n):
        x_p = x.copy(); x_p[i] += h
        x_m = x.copy(); x_m[i] -= h
        J[:, i] = (F(x_p) - F(x_m)) / (2*h)
    return J


def numerical_hessian(f, x, h=1e-5):
    x = np.asarray(x, dtype=float)
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x_pp = x.copy(); x_pp[i] += h; x_pp[j] += h
            x_pm = x.copy(); x_pm[i] += h; x_pm[j] -= h
            x_mp = x.copy(); x_mp[i] -= h; x_mp[j] += h
            x_mm = x.copy(); x_mm[i] -= h; x_mm[j] -= h
            H[i, j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4*h**2)
    return H


def trapezoidal(f, a, b, n=1000):
    x = np.linspace(a, b, n+1); y = f(x)
    h = (b - a) / n
    return h * (0.5*y[0] + np.sum(y[1:-1]) + 0.5*y[-1])


def simpson(f, a, b, n=1000):
    if n % 2: n += 1
    x = np.linspace(a, b, n+1); y = f(x)
    h = (b - a) / n
    return h/3.0 * (y[0] + 4.0*np.sum(y[1::2]) + 2.0*np.sum(y[2::2]) + y[-1])
