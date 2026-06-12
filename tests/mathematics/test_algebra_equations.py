"""
Mathematics verification: every equation verified against
known analytical result with tolerance < 0.001%.
"""

import pytest
import numpy as np
from deep_space_core.mathematics.algebra import (
    rocket_equation_delta_v, mass_ratio, propellant_mass
)
from deep_space_core.constants import G0

@pytest.mark.math
class TestRocketEquation:

    def test_apollo_lm(self):
        """Apollo LM: Isp=311, m0=15000, mf=2000"""
        dv = rocket_equation_delta_v(311, 15000, 2000)
        expected = 311 * G0 * np.log(15000/2000)
        assert abs(dv - expected) / expected < 1e-8

    def test_saturn_v(self):
        """Saturn V: Isp=263, m0=2970000, mf=120000"""
        dv = rocket_equation_delta_v(263, 2970000, 120000)
        expected = 263 * G0 * np.log(2970000/120000)
        assert abs(dv - expected) / expected < 1e-8

    def test_falcon9_first_stage(self):
        """Falcon 9 first stage: Isp=282, MR ~ 20"""
        dv = rocket_equation_delta_v(282, 433000, 22000)
        expected = 282 * G0 * np.log(433000/22000)
        assert abs(dv - expected) / expected < 1e-8

    def test_ion_thruster(self):
        """NSTAR: Isp=3100, dv=4000 m/s"""
        mr = mass_ratio(3100, 4000)
        expected = np.exp(4000 / (3100 * G0))
        assert abs(mr - expected) / expected < 1e-8

    @pytest.mark.parametrize("Isp,m0,mf", [
        (320, 2500, 1700),
        (450, 20000, 5000),
        (300, 5000, 1500),
        (900, 100000, 20000),
    ])
    def test_parametric(self, Isp, m0, mf):
        dv = rocket_equation_delta_v(Isp, m0, mf)
        expected = Isp * G0 * np.log(m0/mf)
        rel_err = abs(dv - expected) / expected
        assert rel_err < 1e-8, f"Rel error {rel_err*100:.6f}%"
