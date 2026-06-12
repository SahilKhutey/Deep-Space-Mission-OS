"""
Electric propulsion validation against published Hall and Ion thruster specs.
"""

import pytest

@pytest.mark.propulsion
class TestElectricPropulsion:

    def test_NEXT(self):
        from deep_space_propulsion_simulator.propulsion.electrical.electric import ElectricThruster
        t = ElectricThruster("NEXT")
        assert t.power == 6900.0
        assert t.thrust == 0.236
        assert t.efficiency == 0.70

    def test_NSTAR(self):
        from deep_space_propulsion_simulator.propulsion.electrical.electric import ElectricThruster
        t = ElectricThruster("NSTAR")
        assert t.power == 2300.0
        assert t.thrust == 0.092
        assert t.efficiency == 0.61
