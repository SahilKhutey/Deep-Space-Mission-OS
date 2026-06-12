"""
Verification tests for the main backend API.
"""

import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

@pytest.mark.dashboard
def test_root_endpoint():
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]

@pytest.mark.dashboard
def test_mission_plan_preset_mars():
    r = client.get("/api/v1/presets/mars")
    assert r.status_code == 200
    data = r.json()
    assert "delta_v_budget" in data
    assert "fuel" in data
    assert "feasibility" in data

@pytest.mark.dashboard
def test_mission_plan_preset_moon():
    r = client.get("/api/v1/presets/moon")
    assert r.status_code == 200
    data = r.json()
    assert "delta_v_budget" in data
    assert "fuel" in data
    assert "feasibility" in data

@pytest.mark.dashboard
def test_post_mission_plan():
    payload = {
        "origin": "Earth",
        "destination": "Mars",
        "spacecraft_mass": 2500.0,
        "propulsion_type": "Chemical",
        "payload_mass": 800.0,
        "launch_date": "2032-08-15"
    }
    r = client.post("/api/v1/mission/plan", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "delta_v_budget" in data
    assert "fuel" in data

@pytest.mark.dashboard
def test_compute_fuel():
    payload = {
        "Isp": 300.0,
        "m0": 1000.0,
        "target_dv": 1.5
    }
    r = client.post("/api/v1/fuel/compute", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "fuel_mass" in data
    assert "dry_mass" in data

@pytest.mark.dashboard
def test_deltav_budget():
    payload = {
        "Isp": 310.0,
        "m0": 1200.0,
        "m_payload": 400.0,
        "segments": [
            {"name": "LEO Insertion", "dv": 9.2},
            {"name": "TLI", "dv": 3.1}
        ]
    }
    r = client.post("/api/v1/deltav/budget", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "total_delta_v_km_s" in data
    assert "final_mass_kg" in data

@pytest.mark.dashboard
def test_staging_size():
    payload = {
        "payload_mass": 500.0,
        "total_dv": 6.5,
        "Isp_stages": [310.0, 340.0],
        "structural_fractions": [0.1, 0.08]
    }
    r = client.post("/api/v1/staging/size", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "stages" in data
    assert "total_vehicle_lift_off_mass_kg" in data

@pytest.mark.dashboard
def test_trajectory_optimization():
    # Keep population/generations minimal for fast test execution
    payload = {
        "destination": "mars",
        "algorithm": "ga",
        "min_departure_date": "2032-08-01",
        "max_departure_date": "2032-08-31",
        "min_duration_days": 180.0,
        "max_duration_days": 220.0,
        "population_size": 10,
        "generations": 3
    }
    r = client.post("/api/v1/optimization/optimize", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "best_departure_jd" in data
    assert "best_departure_calendar" in data
    assert "best_arrival_calendar" in data

@pytest.mark.dashboard
def test_porkchop_generation():
    payload = {
        "destination": "mars",
        "start_departure_date": "2032-08-01",
        "end_departure_date": "2032-08-10",
        "start_arrival_date": "2033-02-01",
        "end_arrival_date": "2033-02-10",
        "steps": 5
    }
    r = client.post("/api/v1/porkchop/generate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "departure_jds" in data
    assert "arrival_jds" in data
    assert "c3" in data
    assert "total_dv" in data

@pytest.mark.dashboard
def test_simulation_run_moon():
    payload = {
        "destination": "moon",
        "launch_date": "2031-06-01",
        "flight_days": 10.0
    }
    r = client.post("/api/v1/simulations/run", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "t" in data
    assert "sc_position" in data

@pytest.mark.dashboard
def test_simulation_run_mars():
    payload = {
        "destination": "mars",
        "launch_date": "2032-08-15",
        "flight_days": 50.0
    }
    r = client.post("/api/v1/simulations/run", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "t" in data
    assert "sc_position" in data
