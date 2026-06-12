"""
Convergence tests — verify solution converges as timestep decreases.
"""

import pytest
import numpy as np
from deep_space_core.mathematics.ode_systems import harmonic_oscillator
from deep_space_core.numerical_methods import rk4

@pytest.mark.numerical
class TestConvergence:

    def test_rk4_order_4(self):
        """Halving dt should reduce error by 16× (order 4)."""
        e1 = self._err(0.02)
        e2 = self._err(0.01)
        ratio = e1 / e2
        assert 14.0 < ratio < 18.0  # should be ~16

    def _err(self, dt):
        y = np.array([1.0, 0.0])
        t = 0.0
        T = 6.4
        n_steps = int(round(T / dt))
        for _ in range(n_steps):
            y = rk4(lambda t, y: harmonic_oscillator(t, y), t, y, dt)
            t += dt
        return abs(y[0] - np.cos(T))

    def test_trapezoidal_order_2(self):
        """Trapezoidal: halving dt halves the squared error (order 2)."""
        from deep_space_core.mathematics.calculus import trapezoidal
        e1 = abs(trapezoidal(np.sin, 0.0, np.pi, 10) - 2.0)
        e2 = abs(trapezoidal(np.sin, 0.0, np.pi, 20) - 2.0)
        assert e1 / e2 > 3.5  # should be ~4
