"""
Astrodynamics validation — Earth orbits, Hohmann, Lambert.
"""

import pytest
import numpy as np
from deep_space_core.constants import MU_EARTH, R_EARTH
from deep_space_core.astrodynamics import vis_viva


@pytest.mark.astrodynamics
class TestEarthOrbits:

    def test_iss_velocity(self):
        """ISS at 408 km: 7.66 km/s."""
        r = R_EARTH + 408.0
        v = vis_viva(r, r, MU_EARTH)
        assert abs(v - 7.66) < 0.02

    def test_geo_velocity(self):
        """GEO: 3.07 km/s."""
        r = 42164.0
        v = vis_viva(r, r, MU_EARTH)
        assert abs(v - 3.07) < 0.02

    def test_escape_velocity_earth(self):
        """Earth surface escape velocity: 11.186 km/s."""
        v_esc = np.sqrt(2.0 * MU_EARTH / R_EARTH)
        assert abs(v_esc - 11.186) < 0.02


@pytest.mark.astrodynamics
class TestHohmann:

    def test_iss_to_geo(self):
        """LEO 400 km → GEO Hohmann."""
        from deep_space_core.trajectories.hohmann import hohmann_transfer
        r1 = R_EARTH + 400.0
        r2 = 42164.0
        result = hohmann_transfer(r1, r2, MU_EARTH)
        assert abs(result["dv1_km_s"] - 2.44) < 0.05
        assert abs(result["dv2_km_s"] - 1.47) < 0.05
        assert abs(result["total_dv_km_s"] - 3.91) < 0.1
        assert 5.0 < result["tof_hours"] < 5.5
