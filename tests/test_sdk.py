"""
Verification and Validation tests for the Deep Space SDK, CLI, and Datasets.
"""

import os
import json
import pytest
from unittest.mock import patch
import io
import contextlib
import numpy as np

from deep_space_sdk.client import DeepSpaceClient
from deep_space_sdk.cli import main

@pytest.mark.sdk
def test_client_orbital_mechanics():
    client = DeepSpaceClient()
    # Test orbit velocity (vis-viva) wrapper
    # r = 7000 km, a = 7000 km, mu = 3.986004418e5
    v = client.get_orbit_velocity(7000.0, 7000.0, 3.986004418e5)
    assert abs(v - np.sqrt(3.986004418e5 / 7000.0)) < 1e-5

@pytest.mark.sdk
def test_client_mission_planning():
    client = DeepSpaceClient()
    # Test Moon mission plan
    plan_moon = client.plan_mission("Earth", "Moon", 1000.0)
    assert plan_moon["feasible"] is True
    assert plan_moon["total_delta_v_km_s"] == 15.5
    
    # Test Mars mission plan
    plan_mars = client.plan_mission("Earth", "Mars", 1500.0)
    assert plan_mars["feasible"] is True
    assert plan_mars["total_delta_v_km_s"] == 16.0

@pytest.mark.sdk
def test_client_cost_and_risk():
    client = DeepSpaceClient()
    # Test cost estimation
    cost = client.estimate_mission_cost(1000.0, 500.0, 67e6, 12.0)
    assert cost["total_cost_usd"] == 67e6 + 1000.0*15000.0 + 500.0*5.0 + 12.0*50000.0
    
    # Test risk assessment
    risk = client.compute_mission_risk(100.0, 50000.0, 10)
    assert 0.0 < risk < 1.0

@pytest.mark.sdk
def test_client_digital_twin_diagnostics():
    client = DeepSpaceClient()
    # Log some dummy telemetry values (linear trend)
    for i in range(10):
        client.log_twin_state("radiator_temp", 280.0 + 2.0 * i)
        
    forecast = client.forecast_twin_state("radiator_temp", 5)
    assert abs(forecast - 308.0) < 0.5
    
    is_anomaly, val = client.predict_twin_anomaly("radiator_temp", 5, (200.0, 305.0))
    assert is_anomaly is True
    assert abs(val - 308.0) < 0.5

@pytest.mark.cli
def test_cli_mission_plan():
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        with patch("sys.argv", ["cli.py", "plan", "--destination", "Moon", "--payload-mass", "1000"]):
            main()
    output = f.getvalue()
    assert "Mission Planning: Earth -> Moon" in output
    assert "Feasibility: True" in output
    assert "Total Delta-V Required: 15.50 km/s" in output

@pytest.mark.cli
def test_cli_mission_plan_json():
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        with patch("sys.argv", ["cli.py", "plan", "--destination", "Mars", "--payload-mass", "1500", "--json"]):
            main()
    output = json.loads(f.getvalue())
    assert output["feasible"] is True
    assert output["total_delta_v_km_s"] == 16.0
    assert len(output["timeline"]) > 0

@pytest.mark.cli
def test_cli_cost():
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        with patch("sys.argv", ["cli.py", "cost", "--dry-mass", "1000", "--propellant-mass", "500", "--launch-cost", "67000000", "--ops-months", "12"]):
            main()
    output = f.getvalue()
    assert "Mission Cost Estimation" in output
    assert "Total Estimated Cost: $82,602,500.00" in output

@pytest.mark.cli
def test_cli_risk():
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        with patch("sys.argv", ["cli.py", "risk", "--duration", "100", "--radiation", "50000", "--components", "10"]):
            main()
    output = f.getvalue()
    assert "Mission Risk & Reliability Assessment" in output
    assert "Failure Probability:" in output

@pytest.mark.cli
def test_cli_twin():
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        with patch("sys.argv", ["cli.py", "twin", "--state-name", "radiator_temp", "--values", "280", "282", "284", "286", "288", "290", "292", "294", "296", "298", "--min-val", "200", "--max-val", "305"]):
            main()
    output = f.getvalue()
    assert "Digital Twin Diagnostics: radiator_temp" in output
    assert "WARNING: ANOMALY PREDICTED" in output
    assert "Forecast Value" in output

@pytest.mark.dataset
def test_dataset_manifest_and_catalog():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manifest_path = os.path.join(workspace, "deep-space-datasets", "dataset_v1", "manifest.json")
    catalog_path = os.path.join(workspace, "deep-space-datasets", "dataset_v1", "ephemeris", "de421_catalog.json")
    
    assert os.path.exists(manifest_path)
    assert os.path.exists(catalog_path)
    
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    assert manifest["version"] == "1.0.0"
    assert manifest["name"] == "de421_planetary_constants"
    assert "ephemeris/de421_catalog.json" in manifest["contents"]
    
    with open(catalog_path, "r") as f:
        catalog = json.load(f)
    assert "Earth" in catalog
    assert "Mars" in catalog
    assert "Moon" in catalog
    
    earth = catalog["Earth"]
    assert earth["a"] == 1.495978875e8
    assert earth["mu"] == 3.986004418e5
