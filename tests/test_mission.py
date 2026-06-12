"""
Unit tests for Mission Planner Orchestrator
"""

import unittest
from core.mission_engine import MissionEngine


class TestMission(unittest.TestCase):

    def test_mars_mission_planning(self):
        config = {
            "origin": "Earth",
            "destination": "Mars",
            "spacecraft_mass": 2500.0,
            "propulsion_type": "Chemical",
            "payload_mass": 800.0,
            "launch_date": "2032-08-15"
        }
        engine = MissionEngine(config)
        results = engine.plan_mission()
        
        self.assertTrue(results["feasibility"]["feasible"])
        self.assertIn("delta_v_budget", results)
        self.assertIn("fuel", results)
        self.assertIn("timeline", results)
        self.assertIn("risk_score", results)
        
        # Mars delta-V varies depending on launch date (typically 14-26 km/s including LEO launch)
        total_dv_km = results["delta_v_budget"]["total_delta_v_km_s"]
        self.assertGreater(total_dv_km, 14.0)
        self.assertLess(total_dv_km, 26.0)

    def test_moon_mission_planning(self):
        config = {
            "origin": "Earth",
            "destination": "Moon",
            "spacecraft_mass": 1500.0,
            "propulsion_type": "Chemical",
            "payload_mass": 500.0,
            "launch_date": "2031-06-01"
        }
        engine = MissionEngine(config)
        results = engine.plan_mission()
        
        self.assertTrue(results["feasibility"]["feasible"])
        self.assertIn("lunar_arrival", results["timeline"])


if __name__ == "__main__":
    unittest.main()
