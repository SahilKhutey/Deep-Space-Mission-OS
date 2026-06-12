"""
Floating-point precision tests — 32-bit, 64-bit, 128-bit.
"""

import pytest
import numpy as np

@pytest.mark.numerical
class TestPrecision:

    def test_double_precision_kepler(self):
        """64-bit: relative error < 1e-12."""
        from deep_space_core.astrodynamics import solve_kepler
        M = 1.5; e = 0.1
        E = solve_kepler(M, e)
        residual = E - e*np.sin(E) - M
        assert abs(residual) < 1e-12

    def test_kahan_compensation(self):
        """Kahan summation should preserve precision."""
        from deep_space_core.numerical_methods import kahan_sum
        summands = [1e-10] * 1000000
        
        s_kahan = kahan_sum(summands)
        assert abs(s_kahan - 1e-4) < 1e-15
