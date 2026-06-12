"""End-to-end mission planning integration tests."""

import pytest

@pytest.mark.integration
class TestMissionPipeline:

    def test_moon_mission_complete(self):
        from deep_space_mission_planner.mission_engine.planner import MissionEngine
        mission = {
            "origin": "Earth", "destination": "Moon",
            "spacecraft_mass": 1500, "propulsion_type": "Chemical",
            "payload_mass": 500, "launch_date": "2031-06-01"
        }
        result = MissionEngine().plan(mission)
        assert result["feasible"] is True
        assert 14 < result["total_delta_v_km_s"] < 17
        assert result["propellant_fraction"] < 0.9
        assert len(result["timeline"]) == 4

    def test_mars_mission_complete(self):
        from deep_space_mission_planner.mission_engine.planner import MissionEngine
        mission = {
            "origin": "Earth", "destination": "Mars",
            "spacecraft_mass": 2500, "propulsion_type": "Chemical",
            "payload_mass": 800, "launch_date": "2032-08-15"
        }
        result = MissionEngine().plan(mission)
        assert result["feasible"] is True
        assert 14 < result["total_delta_v_km_s"] < 18
        assert len(result["timeline"]) == 4

    def test_api_to_engine_integration(self):
        """Backend API → engine → result."""
        from fastapi.testclient import TestClient
        from deep_space_mission_planner.backend.api.main import app
        client = TestClient(app)
        r = client.get("/api/v1/presets/mars")
        assert r.status_code == 200
        data = r.json()
        assert "total_delta_v_km_s" in data
