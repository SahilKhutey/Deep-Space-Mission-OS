"""
Unit tests for Lambert Solver
Verifies solver accuracy by propagating computed velocities and checking arrival position.
"""

import unittest
import numpy as np
from core.constants import MU_EARTH
from core.astrodynamics.lambert import lambert_solve
from core.propagators.rk4 import rk4_propagate, two_body_dynamics


class TestLambert(unittest.TestCase):

    def test_lambert_solver_accuracy(self):
        # 90-degree coplanar transfer around Earth
        r1_vec = np.array([7000.0, 0.0, 0.0])  # km
        r2_vec = np.array([0.0, 8000.0, 0.0])  # km
        dt = 4000.0  # seconds
        
        # Solve Lambert's boundary value problem
        v1, v2 = lambert_solve(r1_vec, r2_vec, dt, MU_EARTH, prograde=True)
        
        # Propagate initial state r1_vec, v1 using RK4
        # Since it's a two-body system, the final position should match r2_vec
        # Using a small step size for integration accuracy
        n_steps = 2000
        step_size = dt / n_steps
        y0 = np.concatenate([r1_vec, v1])
        
        t_hist, y_hist = rk4_propagate(two_body_dynamics, 0.0, y0, step_size, n_steps, MU_EARTH)
        
        r_final = y_hist[-1, :3]
        
        # Check if propagated position matches arrival position target
        np.testing.assert_array_almost_equal(r_final, r2_vec, decimal=2)


if __name__ == "__main__":
    unittest.main()
