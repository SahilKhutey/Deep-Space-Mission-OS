"""
Dormand-Prince (RKDP54) Adaptive Step-Size Numerical Integrator
A state-of-the-art Runge-Kutta method with local error estimation,
highly suited for orbital propagation through high-eccentricity phases.
"""

import numpy as np

# Butcher Tableau for Dormand-Prince 5(4)
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

# 5th-order weights
b5 = np.array([35.0/384.0, 0.0, 500.0/1113.0, 125.0/192.0, -2187.0/6784.0, 11.0/84.0, 0.0])

# Error coefficients (b5 - b4)
d = np.array([
    71.0/57600.0, 
    0.0, 
    -71.0/16695.0, 
    71.0/1920.0, 
    -17253.0/339200.0, 
    22.0/525.0,  # Corrected from 22.0/1050.0 to match HNW tableau and prevent underflow
    -1.0/40.0
])

def dormand_prince_step(func, t, y, dt, *args):
    """
    Perform a single Dormand-Prince step.
    Returns:
        y_next   : State at t + dt (5th order)
        y_err    : Error vector (difference between 5th and 4th order)
    """
    k = []
    
    # k1
    k.append(np.array(func(t, y, *args)))
    
    # k2 to k7
    for i in range(1, 7):
        dy = np.zeros_like(y)
        for j in range(i):
            dy = dy + a[i][j] * k[j]
        k.append(np.array(func(t + c[i] * dt, y + dt * dy, *args)))
        
    k = np.array(k)
    
    # Compute 5th order update
    y_next = y + dt * np.dot(b5, k)
    
    # Compute error vector
    y_err = dt * np.dot(d, k)
    
    return y_next, y_err

def dormand_prince_propagate(func, t0, tf, y0, rtol=1e-8, atol=1e-8, dt_start=10.0, *args):
    """
    Propagate orbital state vector using adaptive step size Dormand-Prince method.
    """
    t = t0
    y = np.array(y0, dtype=float)
    dt = dt_start
    
    t_hist = [t]
    y_hist = [y.copy()]
    
    # Safety factors for step size adaptation
    safety = 0.9
    min_factor = 0.2
    max_factor = 5.0
    
    direction = np.sign(tf - t0)
    if direction == 0:
        return np.array(t_hist), np.array(y_hist)
        
    dt = direction * abs(dt)

    while direction * (tf - t) > 0:
        # Cap dt to land exactly on tf
        if direction * (t + dt - tf) > 0:
            dt = tf - t
            
        y_next, y_err = dormand_prince_step(func, t, y, dt, *args)
        
        # Calculate scale/norm for error evaluation
        err_scale = atol + np.maximum(np.abs(y), np.abs(y_next)) * rtol
        
        # Normalize error vector
        err_norm = np.sqrt(np.mean((y_err / err_scale)**2))
        
        if err_norm <= 1.0:
            # Step accepted
            t += dt
            y = y_next
            t_hist.append(t)
            y_hist.append(y.copy())
            
            # Prevent dividing by zero in step calculation
            if err_norm < 1e-15:
                scale_factor = max_factor
            else:
                scale_factor = safety * (1.0 / err_norm)**0.2
                
            scale_factor = np.clip(scale_factor, min_factor, max_factor)
            dt = dt * scale_factor
        else:
            # Step rejected, retry with smaller step
            scale_factor = safety * (1.0 / err_norm)**0.25
            scale_factor = np.clip(scale_factor, min_factor, 0.9)
            dt = dt * scale_factor
            
            # Avoid step size becoming infinitely small
            if abs(dt) < 1e-6:
                raise RuntimeError("Dormand-Prince integration step size underflow.")
                
    return np.array(t_hist), np.array(y_hist)
