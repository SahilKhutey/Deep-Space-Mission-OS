"""
Orbital mechanics verification — known orbits, periods, velocities.
"""

import pytest
import numpy as np
from deep_space_core.constants import MU_EARTH, MU_SUN, AU, R_EARTH
from deep_space_core.astrodynamics import vis_viva, specific_energy, solve_kepler
from deep_space_core.astrodynamics.orbital_elements import (
    keplerian_to_cartesian, cartesian_to_keplerian
)

@pytest.mark.physics
class TestLEO:

    def test_400km_circular_velocity(self):
        """ISS-like 400km LEO: v ≈ 7.67 km/s."""
        r = R_EARTH + 400.0
        v = vis_viva(r, r, MU_EARTH)
        assert abs(v - 7.67) < 0.05

    def test_400km_period(self):
        """ISS period ≈ 92.7 minutes."""
        r = R_EARTH + 400.0
        T = 2.0*np.pi*np.sqrt(r**3 / MU_EARTH)
        T_min = T / 60.0
        assert abs(T_min - 92.7) < 0.5

    def test_geo_period(self):
        """GEO: r = 42164 km, T = 1436 min (sidereal day)."""
        r = 42164.0
        T = 2.0*np.pi*np.sqrt(r**3 / MU_EARTH)
        T_min = T / 60.0
        assert abs(T_min - 1436.0) < 5.0

@pytest.mark.physics
class TestKeplerianRoundtrip:

    def test_keplerian_to_cartesian_roundtrip(self):
        """Convert Keplerian → Cartesian → Keplerian."""
        a, e, i, raan, arg_p, nu = 7000.0, 0.1, 0.5, 0.3, 0.7, 1.2
        mu = MU_EARTH
        r, v = keplerian_to_cartesian(a, e, i, raan, arg_p, nu, mu)
        a2, e2, i2, raan2, arg_p2, nu2 = cartesian_to_keplerian(r, v, mu)
        assert abs(a - a2) < 1e-6
        assert abs(e - e2) < 1e-9
        assert abs(i - i2) < 1e-9
