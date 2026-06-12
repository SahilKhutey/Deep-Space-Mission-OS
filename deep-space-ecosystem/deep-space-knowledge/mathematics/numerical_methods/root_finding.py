"""
Root-finding algorithms: Newton-Raphson, Bisection, Secant, and Brent's method.
"""

import numpy as np

def newton_raphson(f, df, x0, tol=1e-10, max_iter=100):
    """Newton-Raphson root finder."""
    x = float(x0)
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x, i
        dfx = df(x)
        if abs(dfx) < 1e-30:
            break
        x = x - fx / dfx
    return x, max_iter

def bisection(f, a, b, tol=1e-10, max_iter=200):
    """Bisection root finder (requires sign change)."""
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("Root must be bracketed by sign change.")
    for i in range(max_iter):
        c = (a + b) / 2.0
        fc = f(c)
        if abs(fc) < tol or (b - a) / 2.0 < tol:
            return c, i
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return (a + b) / 2.0, max_iter

def secant(f, x0, x1, tol=1e-10, max_iter=100):
    """Secant root finder."""
    for i in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-30:
            break
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(x_new - x1) < tol:
            return x_new, i
        x0, x1 = x1, x_new
    return x1, max_iter

def brent(f, a, b, tol=1e-10, max_iter=200):
    """Brent's method combines bisection, secant, and inverse quadratic interpolation."""
    fa = f(a)
    fb = f(b)
    if fa * fb > 0:
        raise ValueError("Root must be bracketed by sign change.")
    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa
    c = a
    fc = fa
    d = b - a
    mflag = True
    for i in range(max_iter):
        if abs(fb) < tol or abs(b - a) < tol:
            return b, i
        if fa != fc and fb != fc:
            s = (a * fb * fc / ((fa - fb) * (fa - fc)) +
                 b * fa * fc / ((fb - fa) * (fb - fc)) +
                 c * fa * fb / ((fc - fa) * (fc - fb)))
        else:
            s = b - fb * (b - a) / (fb - fa)
        cond1 = not ((3*a + b)/4 < s < b or b < s < (3*a + b)/4)
        cond2 = mflag and abs(s - b) >= abs(b - c) / 2
        cond3 = (not mflag) and abs(s - b) >= abs(c - d) / 2
        cond4 = mflag and abs(b - c) < tol
        cond5 = (not mflag) and abs(c - d) < tol
        if cond1 or cond2 or cond3 or cond4 or cond5:
            s = (a + b) / 2
            mflag = True
        else:
            mflag = False
        fs = f(s)
        d = c
        c = b
        fc = fb
        if fa * fs < 0:
            b = s
            fb = fs
        else:
            a = s
            fa = fs
        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa
    return b, max_iter
