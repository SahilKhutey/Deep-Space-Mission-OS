"""Unit tests for physical constants and unit conversions."""

import pytest
import numpy as np
from deep_space_core.constants import MU_SUN, MU_EARTH, AU, G0, G
from deep_space_core.units import (
    km_to_m, m_to_km, deg_to_rad, rad_to_deg,
    day_to_s, s_to_day, au_to_km
)

@pytest.mark.unit
class TestConstants:

    def test_mu_sun(self):
        """NASA/JPL DE421 value."""
        assert abs(MU_SUN - 1.32712440018e11) < 1e3

    def test_mu_earth(self):
        assert abs(MU_EARTH - 3.986004418e5) < 0.01

    def test_AU(self):
        assert abs(AU - 1.495978707e8) < 1e2

    def test_G0_exact(self):
        """G0 is defined as exactly 9.80665 m/s²."""
        assert G0 == 9.80665

@pytest.mark.unit
class TestUnitConversions:

    def test_km_m_roundtrip(self):
        assert m_to_km(km_to_m(1.0)) == 1.0

    def test_deg_rad(self):
        assert abs(deg_to_rad(180) - np.pi) < 1e-15
        assert abs(rad_to_deg(np.pi) - 180) < 1e-13

    def test_day_seconds(self):
        assert day_to_s(1) == 86400
        assert s_to_day(86400) == 1.0

    def test_au_km(self):
        assert au_to_km(1.0) == AU
