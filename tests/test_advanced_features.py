"""
Verification and Validation tests for advanced ecosystem Phase 0-4 additions.
"""

import pytest
import numpy as np
import os

@pytest.mark.numerical
def test_symplectic_integrators():
    from deep_space_core.numerical_methods import velocity_verlet_step, leapfrog_step
    
    a_func = lambda r: -r
    
    r_v, v_v = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    dt = 0.01
    initial_energy = 0.5 * (np.dot(r_v, r_v) + np.dot(v_v, v_v))
    
    for _ in range(100):
        r_v, v_v = velocity_verlet_step(r_v, v_v, a_func, dt)
        
    final_energy_v = 0.5 * (np.dot(r_v, r_v) + np.dot(v_v, v_v))
    assert abs(final_energy_v - initial_energy) < 1e-4

    r_l, v_l = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    for _ in range(100):
        r_l, v_l = leapfrog_step(r_l, v_l, a_func, dt)
        
    final_energy_l = 0.5 * (np.dot(r_l, r_l) + np.dot(v_l, v_l))
    assert abs(final_energy_l - initial_energy) < 1e-4

@pytest.mark.math
def test_advanced_math():
    from deep_space_core.mathematics.advanced_math import (
        metric_tensor_spherical, christoffel_symbols_spherical,
        euler_lagrange_error, shannon_entropy, kl_divergence,
        graph_laplacian, consensus_step
    )
    
    g = metric_tensor_spherical(2.0, np.pi/2, 0.0)
    assert g[0, 0] == 1.0
    assert g[1, 1] == 4.0
    assert abs(g[2, 2] - 4.0) < 1e-10

    ch = christoffel_symbols_spherical(2.0, np.pi/2)
    assert ch[("r", "theta", "theta")] == -2.0

    p = [0.25, 0.25, 0.25, 0.25]
    assert shannon_entropy(p) == 2.0
    
    assert kl_divergence([0.5, 0.5], [0.5, 0.5]) == 0.0

    adj = [[0, 1], [1, 0]]
    L = graph_laplacian(adj)
    assert np.allclose(L, [[1, -1], [-1, 1]])

@pytest.mark.mission
def test_mission_planner_additions():
    from deep_space_mission_planner.mission_engine.risk_cost_engines import (
        MissionRiskEngine, CostEstimationEngine
    )
    from deep_space_mission_planner.mission_engine.databases import (
        LAUNCH_VEHICLES, PAYLOAD_DATABASE
    )
    
    re = MissionRiskEngine()
    risk = re.compute_risk(100.0, 50000.0, 10)
    assert 0.0 < risk < 1.0
    
    ce = CostEstimationEngine()
    cost = ce.estimate_cost(1000.0, 500.0, 67e6, 12.0)
    assert cost["total_cost_usd"] == 67e6 + 1000.0*15000.0 + 500.0*5.0 + 12.0*50000.0
    
    assert LAUNCH_VEHICLES["Falcon 9"]["cost_usd"] == 67e6
    assert PAYLOAD_DATABASE["Star Tracker"]["mass_kg"] == 0.3

@pytest.mark.propulsion
def test_propulsion_simulator_additions():
    from deep_space_propulsion_simulator.propulsion.lifetime_materials import (
        MATERIALS, ThrusterLifetimeModel, VacuumChamberModel
    )
    
    assert MATERIALS["Rhenium"]["Tm_k"] == 3186.0
    
    lt = ThrusterLifetimeModel()
    erosion = lt.erosion_rate(200.0, 5.0)
    assert erosion > 0.0
    
    vc = VacuumChamberModel()
    history = vc.simulate_chamber(1.0, 0.01, 10.0, 100.0, 1.0, 0.1)
    assert len(history) > 1
    assert history[-1][1] < 1.0

@pytest.mark.digital_twin
def test_digital_twin_additions():
    from deep_space_digital_twin.state_estimation import ExtendedKalmanFilter
    from deep_space_digital_twin.telemetry_sensor import (
        TelemetryIngestor, SensorModels, FaultInjector
    )
    
    ekf = ExtendedKalmanFilter(2, 1)
    A = np.array([[1.0, 0.1], [0.0, 1.0]])
    C = np.array([[1.0, 0.0]])
    f_func = lambda x: A.dot(x)
    F_jac = lambda x: A
    h_func = lambda x: C.dot(x)
    H_jac = lambda x: C
    z = [1.0]
    
    x_next, P_next = ekf.step(f_func, F_jac, h_func, H_jac, z)
    assert len(x_next) == 2
    assert P_next.shape == (2, 2)
    
    ti = TelemetryIngestor()
    data_bytes = np.array([3.14], dtype=np.float64).tobytes()
    packet = (10).to_bytes(2, "big") + (1000).to_bytes(4, "big") + data_bytes
    parsed = ti.parse_ccsds_packet(packet)
    assert parsed["apid"] == 10
    assert parsed["timestamp"] == 1000
    assert abs(parsed["data_value"] - 3.14) < 1e-6
    
    sm = SensorModels()
    pos = sm.gps_position([100.0, 200.0, 300.0], 1.0)
    assert len(pos) == 3
    
    fi = FaultInjector()
    fi.inject_fault("IMU", "bias", 5.0)
    val = fi.process("IMU", 10.0, 1.0)
    assert val == 6.0

@pytest.mark.export
def test_advanced_exporters():
    from deep_space_core.exports.advanced_exporters import (
        export_parquet, export_netcdf, export_stk_scenario, export_orekit
    )
    
    base_dir = os.path.dirname(__file__)
    tmp_dir = os.path.join(base_dir, "tmp_exports_test")
    os.makedirs(tmp_dir, exist_ok=True)
    
    path_parquet = os.path.join(tmp_dir, "test.parquet")
    path_nc = os.path.join(tmp_dir, "test.nc")
    path_stk = os.path.join(tmp_dir, "test.sc")
    path_orekit = os.path.join(tmp_dir, "test_orekit.json")
    
    data = [{"time": 0.0, "x": 1.0}, {"time": 1.0, "x": 2.0}]
    
    try:
        assert export_parquet(data, path_parquet) in [True, False]
        assert os.path.exists(path_parquet)
        
        assert export_netcdf(data, path_nc) in [True, False]
        assert os.path.exists(path_nc)
        
        assert export_stk_scenario({"name": "TestMission"}, path_stk) is True
        assert os.path.exists(path_stk)
        
        assert export_orekit({"name": "TestMission"}, path_orekit) is True
        assert os.path.exists(path_orekit)
    finally:
        for p in [path_parquet, path_nc, path_stk, path_orekit]:
            if os.path.exists(p):
                os.remove(p)
        if os.path.exists(tmp_dir):
            os.rmdir(tmp_dir)

@pytest.mark.dashboard
def test_mock_dashboard_endpoints():
    from fastapi.testclient import TestClient
    from deep_space_mission_planner.backend.api.main import app
    
    client = TestClient(app)
    r_val = client.get("/api/v1/dashboards/validation")
    assert r_val.status_code == 200
    assert r_val.json()["status"] == "PASS"

    r_risk = client.get("/api/v1/dashboards/risk")
    assert r_risk.status_code == 200
    assert "failure_probability" in r_risk.json()

    r_health = client.get("/api/v1/dashboards/system-health")
    assert r_health.status_code == 200
    assert r_health.json()["power_status"] == "NOMINAL"

    r_opt = client.get("/api/v1/dashboards/optimization")
    assert r_opt.status_code == 200
    assert "pareto_front" in r_opt.json()
