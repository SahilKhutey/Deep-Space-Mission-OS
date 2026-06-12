"""
Standard ODE systems for testing and reference.
"""
import numpy as np


def two_body_ode(t, state, mu):
    """d²r/dt² = -μ·r/r³"""
    r = state[:3]; v = state[3:]
    r_norm = np.linalg.norm(r)
    return np.concatenate([v, -mu * r / r_norm**3])


def harmonic_oscillator(t, y, k=1.0, m=1.0):
    return np.array([y[1], -(k/m) * y[0]])


def pendulum(t, y, g=9.81, L=1.0):
    return np.array([y[1], -(g/L) * np.sin(y[0])])


def hill_equations(t, state, n):
    """HCW relative motion."""
    x, y, z, vx, vy, vz = state
    return np.array([vx, vy, vz,
                     3.0*n**2*x + 2.0*n*vy,
                     -2.0*n*vx,
                     -n**2*z])


def restricted_three_body_ode(t, state, mu):
    """CR3BP in rotating frame. state = [x, y, z, vx, vy, vz]."""
    x, y, z, vx, vy, vz = state
    mu1 = 1.0 - mu
    mu2 = mu
    r1 = np.sqrt((x + mu)**2 + y**2 + z**2)
    r2 = np.sqrt((x - mu1)**2 + y**2 + z**2)
    ax = 2.0*vy + x - mu1*(x+mu)/r1**3 - mu2*(x-mu1)/r2**3
    ay = -2.0*vx + y - mu1*y/r1**3 - mu2*y/r2**3
    az = -mu1*z/r1**3 - mu2*z/r2**3
    return np.array([vx, vy, vz, ax, ay, az])
