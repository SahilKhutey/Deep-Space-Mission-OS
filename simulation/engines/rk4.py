"""
Runge-Kutta 4th Order Numerical Integrator
Suitable for standard fixed-step orbit propagation under single/multi-body dynamics.
"""

import numpy as np

def rk4_step(func, t, y, dt, *args):
    """
    Perform a single step of the classical 4th order Runge-Kutta method.
    y_{n+1} = y_n + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    """
    k1 = np.array(func(t, y, *args))
    k2 = np.array(func(t + 0.5 * dt, y + 0.5 * dt * k1, *args))
    k3 = np.array(func(t + 0.5 * dt, y + 0.5 * dt * k2, *args))
    k4 = np.array(func(t + dt, y + dt * k3, *args))
    return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

def rk4_propagate(func, t0, y0, dt, n_steps, *args):
    """
    Propagate the state vector y0 from t0 using RK4 with fixed step size.
    
    Returns
    -------
    t_arr : numpy array of times
    y_arr : numpy array of states
    """
    t = t0
    y = np.array(y0, dtype=float)
    
    t_hist = [t]
    y_hist = [y.copy()]
    
    for _ in range(int(n_steps)):
        y = rk4_step(func, t, y, dt, *args)
        t += dt
        t_hist.append(t)
        y_hist.append(y.copy())
        
    return np.array(t_hist), np.array(y_hist)

def two_body_dynamics(t, state, mu):
    """
    Standard two-body dynamics equations of motion.
    state = [x, y, z, vx, vy, vz]
    """
    r = state[:3]
    v = state[3:]
    r_norm = np.linalg.norm(r)
    
    if r_norm < 1e-6:
        a = np.zeros(3)
    else:
        a = -mu * r / r_norm**3
        
    return np.concatenate([v, a])
