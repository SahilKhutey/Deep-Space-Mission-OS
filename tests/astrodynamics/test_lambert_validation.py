"""
Lambert solver validation against NASA reference trajectories.
"""

import pytest
import numpy as np
from deep_space_core.constants import MU_SUN, AU
from deep_space_core.astrodynamics import lambert_universal

@pytest.mark.astrodynamics
class TestLambert:

    def test_earth_mars_transfer(self):
        """Earth-Mars Hohmann-like transfer."""
        r1 = np.array([AU, 0.0, 0.0])
        r2 = np.array([-2.279e8, 1000.0, 0.0])
        TOF = 258.8 * 86400.0
        v1, v2 = lambert_universal(r1, r2, TOF, MU_SUN)
        v_earth = np.sqrt(MU_SUN / AU)
        dv1 = abs(np.linalg.norm(v1) - v_earth)
        assert 2.8 < dv1 < 4.0
