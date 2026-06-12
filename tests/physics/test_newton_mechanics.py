"""
Newton's laws verification.
F = ma, conservation of momentum, energy, angular momentum.
"""

import pytest
import numpy as np

@pytest.mark.physics
class TestNewtonSecondLaw:

    def test_constant_force(self):
        """F=10N, m=2kg → a=5 m/s²"""
        F = 10.0; m = 2.0
        a = F / m
        assert a == 5.0

    def test_zero_force(self):
        """F=0 → a=0, v constant."""
        F = 0.0; m = 2.0
        a = F / m
        v_initial = 10.0
        v_after = v_initial + a * 5
        assert v_after == 10.0

@pytest.mark.physics
class TestMomentumConservation:

    def test_elastic_collision_1d(self):
        """Two-body elastic collision conserves momentum and KE."""
        m1, m2 = 1.0, 1.0
        v1i, v2i = 1.0, 0.0
        v1f = v2i
        v2f = v1i
        p_i = m1*v1i + m2*v2i
        p_f = m1*v1f + m2*v2f
        assert abs(p_i - p_f) < 1e-10
        ke_i = 0.5*m1*v1i**2 + 0.5*m2*v2i**2
        ke_f = 0.5*m1*v1f**2 + 0.5*m2*v2f**2
        assert abs(ke_i - ke_f) < 1e-10

@pytest.mark.physics
class TestEnergyConservation:

    def test_free_fall(self):
        """Drop from h, final v = √(2gh)."""
        h = 100.0; g = 9.81
        v_final = np.sqrt(2*g*h)
        assert abs(v_final - 44.29) < 0.01
