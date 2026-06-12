"""
Thermal digital twin validation.
"""

import pytest
from deep_space_digital_twin.thermal import ThermalTwin

@pytest.mark.digital_twin
class TestThermalTwin:

    def test_thermal_transient(self):
        twin = ThermalTwin(mass_kg=100.0, specific_heat=900.0, surface_area=2.0, emissivity=0.85)
        res = twin.update(Q_internal_w=200.0, Q_solar_w=300.0, dt_sec=3600.0)
        assert res["temperature_k"] < 290.0
