"""
Unit tests for Calculus.
"""

import unittest
import numpy as np
from calculus.differential.derivatives import derivative_1d, gradient, jacobian
from calculus.integral.integrals import trapezoidal, simpson
from calculus.vector.vector_calculus import divergence, curl

class TestCalculus(unittest.TestCase):

    def test_derivatives(self):
        f = lambda x: x**3
        df = derivative_1d(f, 2.0)
        self.assertAlmostEqual(df, 12.0, places=4)

    def test_gradient(self):
        f = lambda v: v[0]**2 + v[1]**2
        g = gradient(f, [1.0, 2.0])
        self.assertTrue(np.allclose(g, [2.0, 4.0]))

    def test_integrals(self):
        val = simpson(np.sin, 0, np.pi, n=200)
        self.assertAlmostEqual(val, 2.0, places=5)

    def test_vector_calculus(self):
        # F = [-y, x, 0] -> curl = [0, 0, 2]
        F = lambda pt: np.array([-pt[1], pt[0], 0.0])
        c = curl(F, [0.0, 0.0, 0.0])
        self.assertTrue(np.allclose(c, [0.0, 0.0, 2.0]))

if __name__ == "__main__":
    unittest.main()
