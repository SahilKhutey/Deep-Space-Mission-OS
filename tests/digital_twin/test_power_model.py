"""
Power digital twin validation.
"""

import pytest
from deep_space_digital_twin.power import PowerTwin

@pytest.mark.digital_twin
class TestPowerModel:

    def test_solar_output_vs_distance(self):
        """Solar panel output at 1 AU vs 2 AU."""
        twin_1au = PowerTwin(panel_area=10.0, panel_eff=0.30)
        res_1au = twin_1au.update(sun_distance_au=1.0)
        assert abs(res_1au["solar_output_w"] - 4083.0) < 1.0

        res_2au = twin_1au.update(sun_distance_au=2.0)
        assert abs(res_2au["solar_output_w"] - 1020.75) < 1.0

    def test_load_shedding(self):
        """Under low state of charge, load shedding active."""
        twin = PowerTwin(battery_capacity_wh=1000.0, initial_charge_wh=150.0)
        res = twin.update(sun_distance_au=5.0)
        assert res["load_shedding_active"] is True
        assert res["consumption_w"] == twin.essential_load
