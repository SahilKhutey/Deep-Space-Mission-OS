"""Root-finding methods with validated tests."""
import numpy as np


def newton_raphson(f, fprime, x0, tol=1e-10, max_iter=100):
    x = x0
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        dfx = fprime(x)
        if abs(dfx) < 1e-30:
            break
        x = x - fx / dfx
    return x


def bisection(f, a, b, tol=1e-10, max_iter=200):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("No sign change in interval")
    for i in range(max_iter):
        c = (a + b) / 2.0
        fc = f(c)
        if abs(fc) < tol or (b - a)/2.0 < tol:
            return c
        if fa * fc < 0:
            b = c
        else:
            a, fa = c, fc
    return (a + b) / 2.0


def secant(f, x0, x1, tol=1e-10, max_iter=100):
    for i in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-30:
            break
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        if abs(x_new - x1) < tol:
            return x_new
        x0, x1 = x1, x_new
    return x1


def brent(f, a, b, tol=1e-10, max_iter=200):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("No sign change")
    if abs(fa) < abs(fb):
        a, b = b, a; fa, fb = fb, fa
    c, fc = a, fa
    d = b - a
    mflag = True
    for i in range(max_iter):
        if abs(fb) < tol or abs(b - a) < tol:
            return b
        if fa != fc and fb != fc:
            s = (a*fb*fc/((fa-fb)*(fa-fc)) +
                 b*fa*fc/((fb-fa)*(fb-fc)) +
                 c*fa*fb/((fc-fa)*(fc-fb)))
        else:
            s = b - fb*(b-a)/(fb-fa)
        cond1 = not (((3*a+b)/4.0 < s < b) or (b < s < (3*a+b)/4.0))
        cond2 = mflag and abs(s-b) >= abs(b-c)/2.0
        cond3 = (not mflag) and abs(s-b) >= abs(c-d)/2.0
        cond4 = mflag and abs(b-c) < tol
        cond5 = (not mflag) and abs(c-d) < tol
        if cond1 or cond2 or cond3 or cond4 or cond5:
            s = (a + b) / 2.0
            mflag = True
        else:
            mflag = False
        fs = f(s)
        d = c
        c, fc = b, fb
        if fa * fs < 0:
            b, fb = s, fs
        else:
            a, fa = s, fs
        if abs(fa) < abs(fb):
            a, b = b, a; fa, fb = fb, fa
    return b
