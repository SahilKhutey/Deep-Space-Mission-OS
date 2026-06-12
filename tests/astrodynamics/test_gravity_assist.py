"""
Gravity assist validation — against published flyby data.
"""

import pytest
import numpy as np
from deep_space_core.constants import MU_EARTH
from deep_space_core.astrodynamics import gravity_assist_delta_v

@pytest.mark.astrodynamics
class TestGravityAssist:

    def test_unpowered_flyby_preserves_v_inf(self):
        """For unpowered flyby, v_inf magnitude is preserved."""
        v_inf_in = np.array([5.0, 0.0, 0.0])
        v_inf_out = np.array([5.0, 0.0, 0.0])  # no turn
        dv, turn = gravity_assist_delta_v(v_inf_in, v_inf_out, MU_EARTH, 7000.0)
        assert abs(dv) < 1e-10
        assert abs(turn) < 1e-10
