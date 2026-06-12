"""
Verification and Validation tests for Phase 5 Autonomous AI modules.
"""

import pytest
import numpy as np

@pytest.mark.mission
def test_ai_mission_engineer():
    from deep_space_mission_planner.mission_engine.ai_engineer import AIMissionEngineer
    from deep_space_mission_planner.mission_engine.ai_engineer import GeneticTrajectoryOptimizer
    
    ae = AIMissionEngineer()
    res = ae.select_optimal_vehicle(1500.0, "Moon")
    assert res["optimal_launch_vehicle"] == "Falcon 9"
    assert res["cost_usd"] == 67e6

    go = GeneticTrajectoryOptimizer(population_size=10, generations=3)
    best_a, best_dv = go.optimize_orbit(3.986e5, 6778.0, 42164.0)
    assert best_a > 6778.0
    assert best_dv > 0.0

@pytest.mark.digital_twin
def test_ai_digital_twin_anomaly_prediction():
    from deep_space_digital_twin.ai_twin import AIDigitalTwin
    
    twin = AIDigitalTwin()
    for i in range(10):
        twin.log_state("radiator_temp", 280.0 + 2.0 * i)
        
    forecast = twin.forecast_state("radiator_temp", 5)
    assert abs(forecast - 308.0) < 0.5
    
    is_anomaly, val = twin.predict_anomaly("radiator_temp", 5, (200.0, 305.0))
    assert is_anomaly is True
    assert abs(val - 308.0) < 0.5

@pytest.mark.physics
def test_autonomous_gnc():
    from deep_space_core.astrodynamics.autonomous_gnc import OrbitCorrectionLoop, CollisionAvoidance
    
    loop = OrbitCorrectionLoop(kp=1e-3, ki=1e-5, kd=1e-4)
    burn = loop.compute_correction_burn(7000.0, 6990.0, 1.0)
    assert burn > 0.0

    avoid = CollisionAvoidance()
    satellite_r = [7000.0, 0.0, 0.0]
    satellite_v = [0.0, 7.5, 0.0]
    
    debris_r_far = [7005.0, 0.0, 0.0]
    dv_far = avoid.compute_avoidance_maneuver(satellite_r, satellite_v, debris_r_far, safety_threshold_m=100.0)
    assert np.allclose(dv_far, 0.0)
    
    debris_r_close = [7000.03, 0.0, 0.0]
    dv_close = avoid.compute_avoidance_maneuver(satellite_r, satellite_v, debris_r_close, safety_threshold_m=100.0)
    assert np.linalg.norm(dv_close) > 0.0
    assert np.allclose(dv_close, [0.01, 0.0, 0.0])
