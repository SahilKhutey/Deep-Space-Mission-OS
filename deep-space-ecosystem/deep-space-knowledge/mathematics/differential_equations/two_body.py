"""
Two-Body Problem — Canonical ODE for spacecraft motion.
"""

import numpy as np
from deep_space_core.constants import MU_SUN


def two_body_ode(t, state, mu):
    """
    Two-body equation of motion.

    state = [x, y, z, vx, vy, vz]
    dstate/dt = [vx, vy, vz, ax, ay, az]
    where a = -mu * r / |r|^3
    """
    r = state[:3]
    v = state[3:]
    r_norm = np.linalg.norm(r)
    a = -mu * r / r_norm**3
    return np.concatenate([v, a])


def hill_equations(t, state, n):
    """
    Hill-Clohessy-Wiltshire equations for relative motion in circular orbit.
    n: mean motion (rad/s)
    """
    x, y, z, vx, vy, vz = state
    ax = 3*n**2*x + 2*n*vy
    ay = -2*n*vx
    az = -n**2*z
    return np.array([vx, vy, vz, ax, ay, vz*0 + az])


# VALIDATION
if __name__ == "__main__":
    # Circular orbit test: at 1 AU, period = 1 year
    from mathematics.numerical_methods.integrators import rk4
    r0 = np.array([1.496e8, 0, 0, 0, np.sqrt(MU_SUN/1.496e8), 0])
    y = r0.copy()
    t = 0
    h = 3600
    r_init = np.linalg.norm(y[:3])
    for _ in range(int(365.25 * 24)):
        y = rk4(two_body_ode, t, y, h, MU_SUN)
        t += h
    r_final = np.linalg.norm(y[:3])
    assert abs(r_final - r_init) < 1e-3, f"Energy drift: {abs(r_final - r_init):.3e}"
    print(f"✓ Two-body integration: r drift = {abs(r_final - r_init):.3e} km")
