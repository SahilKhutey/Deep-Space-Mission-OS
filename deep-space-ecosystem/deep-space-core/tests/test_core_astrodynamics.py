import unittest
import numpy as np
from deep_space_core.astrodynamics import solve_kepler, vis_viva, lambert_universal
from deep_space_core.constants import MU_SUN


class TestAstrodynamics(unittest.TestCase):

    def test_kepler_vallado(self):
        """Vallado Ex. 2-3."""
        M = np.deg2rad(235.4); e = 0.4
        E = solve_kepler(M, e)
        expected = 3.848661745
        self.assertAlmostEqual(E, expected, places=5)

    def test_vis_viva_circular(self):
        r = 1.496e8
        v = vis_viva(r, r, MU_SUN)
        expected = np.sqrt(MU_SUN / r)
        self.assertAlmostEqual(v, expected, places=6)

    def test_lambert_runs(self):
        r1 = np.array([1.496e8, 0, 0])
        r2 = np.array([2.279e8*np.cos(np.deg2rad(44)), 2.279e8*np.sin(np.deg2rad(44)), 0])
        dt = 258.8 * 86400.0
        v1, v2 = lambert_universal(r1, r2, dt, MU_SUN)
        self.assertGreater(np.linalg.norm(v1), 0.0)
        self.assertGreater(np.linalg.norm(v2), 0.0)


if __name__ == "__main__":
    unittest.main()
