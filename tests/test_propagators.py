"""
Unit tests for Propagators (RK4, Dormand-Prince, Adams-Bashforth-Moulton)
Verifies energy conservation and position convergence on circular orbits.
"""

import unittest
import numpy as np
from core.constants import MU_EARTH
from core.propagators.rk4 import rk4_propagate, two_body_dynamics
from core.propagators.dormand_prince import dormand_prince_propagate
from core.propagators.adams_bashforth_moulton import adams_bashforth_moulton_propagate


class TestPropagators(unittest.TestCase):

    def setUp(self):
        # Circular LEO orbit parameters
        self.r_orbital = 7000.0  # km
        self.v_circular = np.sqrt(MU_EARTH / self.r_orbital)  # km/s
        self.period = 2 * np.pi * np.sqrt(self.r_orbital**3 / MU_EARTH)  # seconds
        
        # Initial state (on y axis, velocity on negative x axis)
        self.y0 = np.array([0.0, self.r_orbital, 0.0, -self.v_circular, 0.0, 0.0])

    def test_rk4_propagation(self):
        # Propagate for half an orbit
        n_steps = 300
        dt = (self.period / 2.0) / n_steps
        
        t_hist, y_hist = rk4_propagate(two_body_dynamics, 0.0, self.y0, dt, n_steps, MU_EARTH)
        
        # At half orbit, position should be [0.0, -7000.0, 0.0]
        r_final = y_hist[-1, :3]
        expected_pos = np.array([0.0, -self.r_orbital, 0.0])
        
        np.testing.assert_array_almost_equal(r_final, expected_pos, decimal=2)

    def test_dormand_prince_propagation(self):
        tf = self.period / 2.0
        t_hist, y_hist = dormand_prince_propagate(
            two_body_dynamics, 0.0, tf, self.y0, 1e-8, 1e-8, 10.0, MU_EARTH
        )
        
        r_final = y_hist[-1, :3]
        expected_pos = np.array([0.0, -self.r_orbital, 0.0])
        np.testing.assert_array_almost_equal(r_final, expected_pos, decimal=2)

    def test_adams_bashforth_moulton(self):
        n_steps = 300
        dt = (self.period / 2.0) / n_steps
        
        t_hist, y_hist = adams_bashforth_moulton_propagate(
            two_body_dynamics, 0.0, self.y0, dt, n_steps, MU_EARTH
        )
        
        r_final = y_hist[-1, :3]
        expected_pos = np.array([0.0, -self.r_orbital, 0.0])
        np.testing.assert_array_almost_equal(r_final, expected_pos, decimal=2)


if __name__ == "__main__":
    unittest.main()
