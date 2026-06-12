"""
Standard ODE systems for physical simulations.
"""

import numpy as np

def harmonic_oscillator(t, y):
    """
    Simple harmonic oscillator: x'' + x = 0.
    y = [x, v]
    dy/dt = [v, -x]
    """
    return np.array([y[1], -y[0]])

def pendulum(t, y, g=9.81, L=1.0):
    """
    Non-linear pendulum equation: theta'' + (g/L)*sin(theta) = 0.
    y = [theta, omega]
    dy/dt = [omega, -(g/L)*sin(theta)]
    """
    return np.array([y[1], -(g / L) * np.sin(y[0])])

def two_body_ode(t, y, mu):
    """
    Two-body gravitational motion.
    y = [x, y, z, vx, vy, vz]
    dy/dt = [vx, vy, vz, -mu*x/r^3, -mu*y/r^3, -mu*z/r^3]
    """
    r_vec = y[:3]
    v_vec = y[3:]
    r_mag = np.linalg.norm(r_vec)
    if r_mag == 0:
        return np.zeros_like(y)
    a_vec = -mu * r_vec / (r_mag ** 3)
    return np.concatenate([v_vec, a_vec])
