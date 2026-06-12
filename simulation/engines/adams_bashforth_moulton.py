"""
Adams-Bashforth-Moulton 4th Order Predictor-Corrector Integrator
A multi-step numerical method. Uses RK4 for bootstrapping the initial steps.
Highly efficient since it only requires 2 derivative evaluations per step.
"""

import numpy as np
from simulation.engines.rk4 import rk4_step, rk4_propagate

def adams_bashforth_moulton_propagate(func, t0, y0, dt, n_steps, *args):
    """
    Propagate orbital state vector using 4th-order Adams-Bashforth-Moulton method.
    """
    n_steps = int(n_steps)
    if n_steps < 4:
        # Fall back to pure RK4 if too few steps
        return rk4_propagate(func, t0, y0, dt, n_steps, *args)
        
    t = t0
    y = np.array(y0, dtype=float)
    
    t_hist = [t]
    y_hist = [y.copy()]
    
    # Bootstrap the first 3 steps using RK4
    for _ in range(3):
        y = rk4_step(func, t, y, dt, *args)
        t += dt
        t_hist.append(t)
        y_hist.append(y.copy())
        
    # Evaluate derivatives at the first 4 points (t0, t1, t2, t3)
    f = [
        np.array(func(t_hist[0], y_hist[0], *args)),
        np.array(func(t_hist[1], y_hist[1], *args)),
        np.array(func(t_hist[2], y_hist[2], *args)),
        np.array(func(t_hist[3], y_hist[3], *args))
    ]
    
    y_current = y_hist[3].copy()
    t_current = t_hist[3]
    
    # Main Adams-Bashforth-Moulton loop
    for _ in range(3, n_steps):
        t_next = t_current + dt
        
        # Predictor (Adams-Bashforth 4th order)
        y_pred = y_current + (dt / 24.0) * (
            55.0 * f[3] - 59.0 * f[2] + 37.0 * f[1] - 9.0 * f[0]
        )
        
        # Evaluate derivative at predicted state
        f_pred = np.array(func(t_next, y_pred, *args))
        
        # Corrector (Adams-Moulton 4th order)
        y_corr = y_current + (dt / 24.0) * (
            9.0 * f_pred + 19.0 * f[3] - 5.0 * f[2] + f[1]
        )
        
        # Update state and time
        t_current = t_next
        y_current = y_corr.copy()
        
        t_hist.append(t_current)
        y_hist.append(y_current.copy())
        
        # Shift derivatives history window: remove oldest, add new derivative
        f[0] = f[1]
        f[1] = f[2]
        f[2] = f[3]
        f[3] = np.array(func(t_current, y_current, *args))
        
    return np.array(t_hist), np.array(y_hist)
