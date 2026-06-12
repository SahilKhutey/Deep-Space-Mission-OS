"""
Unit tests for Astrodynamics Mathematics.
"""

import unittest
import numpy as np
from astrodynamics_math.kepler import solve_kepler_equation, true_anomaly_from_eccentric
from astrodynamics_math.lambert import lambert_solver
from astrodynamics_math.vis_viva import vis_viva, orbital_energy

class TestAstrodynamicsMath(unittest.TestCase):

    def test_kepler_equation(self):
        M = np.deg2rad(235.4)
        e = 0.4
        E = solve_kepler_equation(M, e)
        # Expected: ~4.06645 rad (232.99 deg)
        self.assertAlmostEqual(E, 3.84866, places=4)
        
    def test_vis_viva(self):
        v = vis_viva(7000.0, 7000.0, 398600.0) # Circular velocity
        self.assertAlmostEqual(v, np.sqrt(398600.0 / 7000.0), places=6)

if __name__ == "__main__":
    unittest.main()
