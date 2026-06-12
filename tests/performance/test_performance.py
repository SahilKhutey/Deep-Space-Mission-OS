"""
Performance testing to assert execution speed limits.
"""

import pytest
import time
from deep_space_mission_planner.mission_engine.planner import MissionEngine
from deep_space_propulsion_simulator.propulsion.chemical.bipropellant import BipropellantEngine

@pytest.mark.performance
class TestPerformance:

    def test_mission_planner_performance_moon(self):
        planner = MissionEngine()
        mission = {"origin": "Earth", "destination": "Moon"}
        
        t0 = time.perf_counter()
        res = planner.plan(mission)
        t_elapsed = time.perf_counter() - t0
        
        assert res is not None
        assert t_elapsed < 1.0

    def test_mission_planner_performance_mars(self):
        planner = MissionEngine()
        mission = {"origin": "Earth", "destination": "Mars"}
        
        t0 = time.perf_counter()
        res = planner.plan(mission)
        t_elapsed = time.perf_counter() - t0
        
        assert res is not None
        assert t_elapsed < 5.0

    def test_propulsion_simulator_steps_performance(self):
        engine = BipropellantEngine("Raptor")
        
        t0 = time.perf_counter()
        for _ in range(10000):
            engine.mass_flow_rate()
        t_elapsed = time.perf_counter() - t0
        
        assert t_elapsed < 2.0

    def test_digital_twin_frequency(self):
        from deep_space_digital_twin.power import PowerTwin
        twin = PowerTwin()
        
        t0 = time.perf_counter()
        for _ in range(1000):
            twin.update(1.0)
        t_elapsed = time.perf_counter() - t0
        
        avg_time = t_elapsed / 1000.0
        assert avg_time < 0.001
