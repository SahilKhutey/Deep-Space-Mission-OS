"""
Thermal radiator balance validation.
"""

import pytest
from deep_space_propulsion_simulator.propulsion.thermal.radiator import ThermalRadiator

@pytest.mark.propulsion
class TestThermalRadiator:

    def test_steady_state_temp(self):
        """Radiator with area=2.0 m^2, emissivity=0.85, Q_in=500 W."""
        r = ThermalRadiator(area=2.0, emissivity=0.85)
        T_eq = r.steady_state_temp(Q_in=500.0)
        assert abs(T_eq - 268.3) < 0.5
        
    def test_heat_rejected_matches(self):
        r = ThermalRadiator(area=2.0, emissivity=0.85)
        Q = r.heat_rejected(268.3)
        assert abs(Q - 500.0) < 5.0
