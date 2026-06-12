"""
Unit tests for Algebra, Geometry, and Trigonometry.
"""

import unittest
import numpy as np
from algebra.equations import solve_quadratic, tsiolkovsky_dv, tsiolkovsky_mf
from algebra.geometry import distance_3d, line_plane_intersection, sphere_line_intersection
from algebra.trigonometry import spherical_distance, spherical_triangle_side

class TestAlgebra(unittest.TestCase):

    def test_solve_quadratic(self):
        roots = solve_quadratic(1, -5, 6)
        self.assertEqual(len(roots), 2)
        self.assertTrue(2.0 in roots and 3.0 in roots)

    def test_tsiolkovsky(self):
        dv = tsiolkovsky_dv(300.0, 1000.0, 500.0)
        self.assertAlmostEqual(dv, 300.0 * 9.80665 * np.log(2.0), places=4)
        mf = tsiolkovsky_mf(300.0, 1000.0, dv)
        self.assertAlmostEqual(mf, 500.0, places=4)

    def test_distance_3d(self):
        d = distance_3d([0,0,0], [1,1,1])
        self.assertAlmostEqual(d, np.sqrt(3.0), places=6)

    def test_line_plane_intersection(self):
        pt = line_plane_intersection([0,0,1], [0,0,-1], [0,0,0], [0,0,1])
        self.assertTrue(np.allclose(pt, [0,0,0]))

    def test_sphere_line_intersection(self):
        pts = sphere_line_intersection([-2,0,0], [1,0,0], [0,0,0], 1.0)
        self.assertEqual(len(pts), 2)
        # Check that both points are present, order-independent
        found_p1 = any(np.allclose(p, [-1,0,0]) for p in pts)
        found_p2 = any(np.allclose(p, [1,0,0]) for p in pts)
        self.assertTrue(found_p1)
        self.assertTrue(found_p2)

    def test_spherical_trig(self):
        dist = spherical_distance(0.0, 0.0, 0.0, np.pi/2, radius=1.0)
        self.assertAlmostEqual(dist, np.pi/2, places=6)

if __name__ == "__main__":
    unittest.main()
