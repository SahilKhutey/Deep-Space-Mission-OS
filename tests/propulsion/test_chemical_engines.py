"""
Chemical propulsion validation against published engine data.
"""

import pytest

@pytest.mark.propulsion
class TestChemicalEngines:

    def test_RL10(self):
        """RL10: Isp=450s, thrust=110 kN."""
        from deep_space_propulsion_simulator.propulsion.chemical.bipropellant import BipropellantEngine
        e = BipropellantEngine("RL-10")
        assert e.Isp == 450.0
        assert e.thrust == 1.1e5
        mdot = e.mass_flow_rate()
        assert abs(mdot - 24.9) < 0.2

    def test_Raptor(self):
        """Raptor: Isp=380s, thrust=2.2 MN."""
        from deep_space_propulsion_simulator.propulsion.chemical.bipropellant import BipropellantEngine
        e = BipropellantEngine("Raptor")
        assert e.Isp == 380.0
        assert e.thrust == 2.2e6
        mdot = e.mass_flow_rate()
        assert abs(mdot - 590.0) < 10.0

    def test_Merlin(self):
        """Merlin 1D: Isp=311s, thrust=981 kN."""
        from deep_space_propulsion_simulator.propulsion.chemical.bipropellant import BipropellantEngine
        e = BipropellantEngine("Merlin")
        assert e.Isp == 311.0
        assert e.thrust == 9.81e5
        mdot = e.mass_flow_rate()
        assert abs(mdot - 321.6) < 2.0
