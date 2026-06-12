"""
Numerical ODE solvers and precision arithmetic helpers.
"""

import numpy as np

def rk4(f, t, y, dt, *args):
    """
    Classic 4th-order Runge-Kutta step.
    """
    y = np.array(y, dtype=float)
    k1 = f(t, y, *args)
    k2 = f(t + 0.5 * dt, y + 0.5 * dt * k1, *args)
    k3 = f(t + 0.5 * dt, y + 0.5 * dt * k2, *args)
    k4 = f(t + dt, y + dt * k3, *args)
    return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

def rk45_step(f, t, y, dt, tol=1e-6, *args):
    """
    Single Runge-Kutta-Fehlberg 4(5) step.
    Returns:
        y_next: state at t + dt (4th order)
        error: local truncation error estimate
        dt_suggest: suggested next time step
    """
    y = np.array(y, dtype=float)
    # RKF45 Coefficients
    c2, a21 = 1/4, 1/4
    c3, a31, a32 = 3/8, 3/32, 9/32
    c4, a41, a42, a43 = 12/13, 1932/2197, -7200/2197, 7296/2197
    c5, a51, a52, a53, a54 = 1, 439/216, -8, 3680/513, -845/4100
    c6, a61, a62, a63, a64, a65 = 1/2, -8/27, 2, -3544/2565, 1859/4104, -11/40

    # 4th and 5th order coefficients
    b41, b42, b43, b44, b45, b46 = 25/216, 0, 1408/2565, 2197/4104, -1/5, 0
    b51, b52, b53, b54, b55, b56 = 16/135, 0, 6656/12825, 28561/56430, -9/50, 2/55

    k1 = f(t, y, *args)
    k2 = f(t + c2*dt, y + dt*(a21*k1), *args)
    k3 = f(t + c3*dt, y + dt*(a31*k1 + a32*k2), *args)
    k4 = f(t + c4*dt, y + dt*(a41*k1 + a42*k2 + a43*k3), *args)
    k5 = f(t + c5*dt, y + dt*(a51*k1 + a52*k2 + a53*k3 + a54*k4), *args)
    k6 = f(t + c6*dt, y + dt*(a61*k1 + a62*k2 + a63*k3 + a64*k4 + a65*k5), *args)

    y4 = y + dt * (b41*k1 + b42*k2 + b43*k3 + b44*k4 + b45*k5 + b46*k6)
    y5 = y + dt * (b51*k1 + b52*k2 + b53*k3 + b54*k4 + b55*k5 + b56*k6)

    err = np.linalg.norm(y5 - y4)
    if err == 0:
        factor = 2.0
    else:
        factor = 0.84 * (tol / err) ** 0.25
        factor = min(max(factor, 0.1), 4.0)

    return y4, err, dt * factor

def kahan_sum(summands):
    """
    Kahan summation algorithm to reduce numerical precision loss.
    """
    sum_val = 0.0
    c = 0.0
    for s in summands:
        y = s - c
        t = sum_val + y
        c = (t - sum_val) - y
        sum_val = t
    return sum_val

def velocity_verlet_step(r, v, a_func, dt, *args):
    """
    Single step of Velocity Verlet integration.
    a_func: acceleration function a = a_func(r, *args).
    Returns: r_next, v_next
    """
    r = np.array(r, dtype=float)
    v = np.array(v, dtype=float)
    a = a_func(r, *args)
    r_next = r + v * dt + 0.5 * a * (dt ** 2)
    a_next = a_func(r_next, *args)
    v_next = v + 0.5 * (a + a_next) * dt
    return r_next, v_next

def leapfrog_step(r, v, a_func, dt, *args):
    """
    Single step of Leapfrog integration.
    a_func: acceleration function a = a_func(r, *args).
    Returns: r_next, v_next
    """
    r = np.array(r, dtype=float)
    v = np.array(v, dtype=float)
    a = a_func(r, *args)
    v_half = v + 0.5 * a * dt
    r_next = r + v_half * dt
    a_next = a_func(r_next, *args)
    v_next = v_half + 0.5 * a_next * dt
    return r_next, v_next
