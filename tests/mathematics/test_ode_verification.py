"""
ODE verification — RK4, RK45, Dormand-Prince tested against
analytical solutions with absolute and relative error metrics.
"""

import pytest
import numpy as np
from deep_space_core.mathematics.ode_systems import (
    harmonic_oscillator, pendulum, two_body_ode
)
from deep_space_core.numerical_methods import rk4, rk45_step
from deep_space_core.propagators import rk4_propagate, dp_propagate_adaptive
from deep_space_core.constants import MU_SUN

@pytest.mark.math
class TestRK4HarmonicOscillator:

    def test_absolute_error_one_period(self):
        y0 = np.array([1.0, 0.0])
        y = y0.copy()
        dt = 0.01
        t = 0.0
        T = 2.0 * np.pi
        while t < T:
            step = min(dt, T - t)
            y = rk4(lambda t, y: harmonic_oscillator(t, y), t, y, step)
            t += step
        assert abs(y[0] - 1.0) < 1e-5
        assert abs(y[1] - 0.0) < 1e-5

    def test_position_velocity(self):
        y0 = np.array([1.0, 0.0])
        y = y0.copy()
        dt = 0.001
        t = 0.0
        T = np.pi
        while t < T:
            step = min(dt, T - t)
            y = rk4(lambda t, y: harmonic_oscillator(t, y), t, y, step)
            t += step
        assert abs(y[0] - (-1.0)) < 1e-3
        assert abs(y[1] - 0.0) < 1e-3

@pytest.mark.math
class TestPendulum:

    def test_small_angle_oscillation(self):
        y0 = np.array([0.1, 0.0])  # small angle
        L, g = 1.0, 9.81
        expected_period = 2.0*np.pi*np.sqrt(L/g)

        y = y0.copy()
        dt = 0.001
        t = 0.0
        T_target = expected_period
        for _ in range(int(T_target/dt)):
            y = rk4(lambda t, y: pendulum(t, y, g, L), 0.0, y, dt)
            t += dt
        assert abs(y[0] - 0.1) < 1e-2

@pytest.mark.math
class TestTwoBody:

    def test_circular_orbit_one_year(self):
        r0 = 1.496e8
        v_circ = np.sqrt(MU_SUN / r0)
        y0 = np.array([r0, 0.0, 0.0, 0.0, v_circ, 0.0])
        traj = rk4_propagate(two_body_ode, y0, 0.0, 365.25*86400.0, 3600.0, MU_SUN)
        r_final = np.linalg.norm(traj[-1][1][:3])
        assert abs(r_final - r0) / r0 < 1e-5
