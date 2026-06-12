"""
Unit tests for Linear Algebra.
"""

import unittest
import numpy as np
from linear_algebra.operations import euler_to_dcm, quaternion_to_dcm, dcm_to_quaternion
from linear_algebra.decomposition import singular_value_decomposition, cholesky_decomposition

class TestLinearAlgebra(unittest.TestCase):

    def test_euler_to_dcm(self):
        dcm = euler_to_dcm(0.1, 0.2, 0.3)
        self.assertAlmostEqual(np.linalg.det(dcm), 1.0, places=9)
        self.assertTrue(np.allclose(dcm @ dcm.T, np.eye(3), atol=1e-10))

    def test_quaternion_roundtrip(self):
        q = np.array([0.9689124, 0.047915, 0.09583, 0.239575])
        q /= np.linalg.norm(q)
        dcm = quaternion_to_dcm(q)
        q_rt = dcm_to_quaternion(dcm)
        self.assertTrue(np.allclose(q, q_rt, atol=1e-5) or np.allclose(q, -q_rt, atol=1e-5))

    def test_svd(self):
        A = np.array([[1.0, 2.0], [3.0, 4.0]])
        U, S, Vt = singular_value_decomposition(A)
        A_reconstructed = U @ np.diag(S) @ Vt
        self.assertTrue(np.allclose(A, A_reconstructed))

if __name__ == "__main__":
    unittest.main()
