"""
Unit tests for Keplerian Orbital Mechanics
"""

import unittest
import numpy as np
from core.constants import MU_EARTH
from core.astrodynamics.keplerian import solve_kepler, true_anomaly, eccentric_anomaly, \
    keplerian_to_cartesian, cartesian_to_keplerian


class TestKeplerian(unittest.TestCase):

    def test_kepler_solver(self):
        # M = E - e*sin(E)
        # For e = 0, E = M
        self.assertAlmostEqual(solve_kepler(1.0, 0.0), 1.0)
        
        # Test a known case
        # E = 1.0, e = 0.5 -> M = 1.0 - 0.5*sin(1.0) = 0.579264064
        M = 1.0 - 0.5 * np.sin(1.0)
        E_solved = solve_kepler(M, 0.5)
        self.assertAlmostEqual(E_solved, 1.0, places=9)

    def test_anomaly_conversions(self):
        e = 0.1
        E = 1.2
        nu = true_anomaly(E, e)
        E_back = eccentric_anomaly(nu, e)
        self.assertAlmostEqual(E, E_back, places=9)

    def test_coordinate_conversion_roundtrip(self):
        # Earth orbit elements
        a = 7000.0       # Semi-major axis (km)
        e = 0.05         # Eccentricity
        i = np.radians(28.5)  # Inclination (rad)
        raan = np.radians(45.0)  # RAAN (rad)
        arg_p = np.radians(30.0)  # Argument of periapsis (rad)
        nu = np.radians(60.0)  # True anomaly (rad)

        # Convert to Cartesian
        r, v = keplerian_to_cartesian(a, e, i, raan, arg_p, nu, mu=MU_EARTH)
        
        # Convert back to Keplerian
        a_rt, e_rt, i_rt, raan_rt, arg_p_rt, nu_rt = cartesian_to_keplerian(r, v, mu=MU_EARTH)
        
        self.assertAlmostEqual(a, a_rt, places=5)
        self.assertAlmostEqual(e, e_rt, places=6)
        self.assertAlmostEqual(i, i_rt, places=6)
        self.assertAlmostEqual(raan, raan_rt, places=6)
        self.assertAlmostEqual(arg_p, arg_p_rt, places=6)
        self.assertAlmostEqual(nu, nu_rt, places=6)


if __name__ == "__main__":
    unittest.main()

