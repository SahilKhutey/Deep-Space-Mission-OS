import numpy as np


def rk4_step(f, t, y, h, *args):
    k1 = f(t, y, *args)
    k2 = f(t + h/2.0, y + h*k1/2.0, *args)
    k3 = f(t + h/2.0, y + h*k2/2.0, *args)
    k4 = f(t + h, y + h*k3, *args)
    return y + (h/6.0)*(k1 + 2.0*k2 + 2.0*k3 + k4)


def rk4_propagate(f, y0, t0, tf, h, *args):
    n = int(np.ceil((tf - t0) / h))
    t = t0
    y = np.array(y0, dtype=float)
    traj = [(t, y.copy())]
    for _ in range(n):
        y = rk4_step(f, t, y, h, *args)
        t += h
        traj.append((t, y.copy()))
    return traj
