"""
Numerical stability tests — long-term integration, no divergence.
"""

import pytest
import numpy as np
from deep_space_core.mathematics.ode_systems import two_body_ode, harmonic_oscillator
from deep_space_core.numerical_methods import rk4
from deep_space_core.constants import MU_SUN

@pytest.mark.numerical
class TestStability:

    def test_harmonic_oscillator_1000_periods(self):
        """Integrate 1,000 periods, verify bounded."""
        y = np.array([1.0, 0.0])
        dt = 0.05
        n = int(1000.0 * 2.0 * np.pi / dt)
        for _ in range(n):
            y = rk4(lambda t, y: harmonic_oscillator(t, y), 0.0, y, dt)
        amp = np.sqrt(y[0]**2 + y[1]**2)
        assert amp < 1.05

    def test_two_body_10_orbits(self):
        """10 Earth orbits."""
        r0 = 1.496e8
        v = np.sqrt(MU_SUN / r0)
        y0 = np.array([r0, 0.0, 0.0, 0.0, v, 0.0])
        dt = 3600.0 * 24.0
        n = int(10.0 * 365.25)
        y = y0.copy()
        for _ in range(n):
            y = rk4(two_body_ode, 0.0, y, dt, MU_SUN)
        r_final = np.linalg.norm(y[:3])
        assert abs(r_final - r0) / r0 < 0.02
