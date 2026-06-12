"""
Unit tests for Numerical Methods.
"""

import unittest
import numpy as np
from numerical_methods.root_finding import newton_raphson, bisection, brent
from numerical_methods.integration import rk4, rk45_step
from numerical_methods.interpolation import cubic_spline

class TestNumerical(unittest.TestCase):

    def test_root_finding(self):
        f = lambda x: x**2 - 2.0
        df = lambda x: 2.0 * x
        root_nr, _ = newton_raphson(f, df, 1.5)
        self.assertAlmostEqual(root_nr, np.sqrt(2.0), places=6)
        
        root_bi, _ = bisection(f, 1.0, 2.0)
        self.assertAlmostEqual(root_bi, np.sqrt(2.0), places=6)
        
        root_br, _ = brent(f, 1.0, 2.0)
        self.assertAlmostEqual(root_br, np.sqrt(2.0), places=6)

    def test_interpolation(self):
        x = np.array([0, 1, 2, 3, 4])
        y = x**2
        self.assertAlmostEqual(cubic_spline(1.5, x, y), 2.23214, places=4)

if __name__ == "__main__":
    unittest.main()
