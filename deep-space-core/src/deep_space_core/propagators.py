"""
Trajectory propagators using fixed and adaptive step solvers.
"""

import numpy as np
from deep_space_core.numerical_methods import rk4, rk45_step

def rk4_propagate(f, y0, t0, tf, dt, *args):
    """
    Fixed-step propagator using RK4.
    Returns:
        list of tuples (t, y)
    """
    t = t0
    y = np.array(y0, dtype=float)
    trajectory = [(t, y.copy())]
    
    direction = np.sign(tf - t0)
    if direction == 0:
        return trajectory
        
    dt = direction * abs(dt)
    
    while direction * (tf - t) > 1e-9:
        if direction * (t + dt - tf) > 0:
            dt_step = tf - t
        else:
            dt_step = dt
        y = rk4(f, t, y, dt_step, *args)
        t += dt_step
        trajectory.append((t, y.copy()))
        
    return trajectory

def dp_propagate_adaptive(f, y0, t0, tf, dt_init=1.0, tol=1e-6, *args):
    """
    Adaptive step propagator using RKF45/Dormand-Prince algorithm.
    Returns:
        list of tuples (t, y)
    """
    t = t0
    y = np.array(y0, dtype=float)
    trajectory = [(t, y.copy())]
    
    direction = np.sign(tf - t0)
    if direction == 0:
        return trajectory
        
    dt = direction * abs(dt_init)
    
    while direction * (tf - t) > 1e-9:
        if direction * (t + dt - tf) > 0:
            dt_step = tf - t
            last_step = True
        else:
            dt_step = dt
            last_step = False
            
        y_next, err, dt_suggest = rk45_step(f, t, y, dt_step, tol, *args)
        
        # Accept or reject step
        if err <= tol or abs(dt_step) < 1e-5:
            # Step accepted
            t += dt_step
            y = y_next
            trajectory.append((t, y.copy()))
            dt = dt_suggest
        else:
            # Step rejected, retry with smaller step
            dt = dt_suggest
            if abs(dt) < 1e-5:
                # Force take step to prevent infinite loop
                t += dt_step
                y = y_next
                trajectory.append((t, y.copy()))
                
    return trajectory
