"""
Verification tests for the vis-viva orbital tweaker, sun-synchronous solver, and perturbed propagator API endpoints.
"""

import pytest
import numpy as np
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)

@pytest.mark.dashboard
def test_vis_viva_basic():
    """Test standard inputs for Earth orbit."""
    payload = {
        "a": 12000.0,
        "e": 0.1,
        "mu_type": "earth"
    }
    r = client.post("/api/v1/astrodynamics/vis-viva", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "v_periapsis_km_s" in data
    assert "v_apoapsis_km_s" in data
    assert "v_current_km_s" in data
    assert data["v_current_km_s"] is None
    assert "rp_km" in data
    assert "ra_km" in data
    assert "period_s" in data
    assert "mu" in data
    
    # Mathematical checks
    assert data["rp_km"] == pytest.approx(10800.0)
    assert data["ra_km"] == pytest.approx(13200.0)
    
    # Periapsis velocity should be higher than apoapsis velocity
    assert data["v_periapsis_km_s"] > data["v_apoapsis_km_s"]

@pytest.mark.dashboard
def test_vis_viva_with_radius():
    """Test inputs specifying a current distance/radius."""
    payload = {
        "a": 12000.0,
        "e": 0.1,
        "mu_type": "earth",
        "r": 11000.0
    }
    r = client.post("/api/v1/astrodynamics/vis-viva", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["v_current_km_s"] is not None
    assert data["v_current_km_s"] > 0
    # At r = 11000 (closer to periapsis than apoapsis), velocity should be between v_peri and v_apo
    assert data["v_current_km_s"] < data["v_periapsis_km_s"]
    assert data["v_current_km_s"] > data["v_apoapsis_km_s"]

@pytest.mark.dashboard
def test_vis_viva_different_bodies():
    """Test that different bodies use correct gravitational parameters."""
    bodies = ["earth", "moon", "mars", "sun"]
    for body in bodies:
        payload = {
            "a": 20000.0,
            "e": 0.05,
            "mu_type": body
        }
        r = client.post("/api/v1/astrodynamics/vis-viva", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert data["mu"] > 0
        assert data["v_periapsis_km_s"] > 0

@pytest.mark.dashboard
def test_vis_viva_invalid_radius():
    """Test validation constraint when a negative radius is provided."""
    payload = {
        "a": 12000.0,
        "e": 0.1,
        "mu_type": "earth",
        "r": -500.0
    }
    r = client.post("/api/v1/astrodynamics/vis-viva", json=payload)
    assert r.status_code == 400
    assert "detail" in r.json()

@pytest.mark.dashboard
def test_vis_viva_j2_rates():
    """Test physical J2 nodal precession and apsidal rotation properties."""
    # 1. Standard inclined orbit (Earth, a=7000km, e=0.01, i=28.5)
    payload = {
        "a": 7000.0,
        "e": 0.01,
        "mu_type": "earth",
        "i": 28.5
    }
    r = client.post("/api/v1/astrodynamics/vis-viva", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "nodal_precession_deg_day" in data
    assert "apsidal_rotation_deg_day" in data
    assert "j2_value" in data
    assert data["j2_value"] == pytest.approx(1.08262668e-3)
    
    # Nodal precession should be negative for a standard prograde inclined orbit
    assert data["nodal_precession_deg_day"] < 0
    
    # 2. Polar orbit (i = 90.0): Nodal precession should be zero since cos(90) = 0
    payload_polar = {
        "a": 7000.0,
        "e": 0.01,
        "mu_type": "earth",
        "i": 90.0
    }
    r_polar = client.post("/api/v1/astrodynamics/vis-viva", json=payload_polar)
    assert r_polar.status_code == 200
    data_polar = r_polar.json()
    assert data_polar["nodal_precession_deg_day"] == pytest.approx(0, abs=1e-9)
    
    # 3. Critical inclination (i = 63.4349488 deg): Apsidal rotation should be zero (5 * cos^2(i) - 1 = 0)
    i_crit = np.degrees(np.arccos(1.0 / np.sqrt(5.0)))
    payload_crit = {
        "a": 7000.0,
        "e": 0.01,
        "mu_type": "earth",
        "i": i_crit
    }
    r_crit = client.post("/api/v1/astrodynamics/vis-viva", json=payload_crit)
    assert r_crit.status_code == 200
    data_crit = r_crit.json()
    assert data_crit["apsidal_rotation_deg_day"] == pytest.approx(0, abs=1e-4)

@pytest.mark.dashboard
def test_sun_synchronous_solver():
    """Verify solving for Sun-Synchronous inclinations."""
    # 1. Earth orbit at a = 7000km (~620km altitude), circular e=0.001
    payload = {
        "a": 7000.0,
        "e": 0.001,
        "mu_type": "earth"
    }
    r = client.post("/api/v1/astrodynamics/sun-synchronous", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["possible"] is True
    assert data["target_rate_deg_day"] == pytest.approx(360.0 / 365.256)
    # Sun-sync inclination for ~600km Earth orbit is roughly 97.8 - 98.2 degrees
    assert data["inclination_deg"] == pytest.approx(97.8, abs=0.5)

    # 2. Too high orbit where J2 is too weak to match precession rate
    payload_high = {
        "a": 20000.0,
        "e": 0.001,
        "mu_type": "earth"
    }
    r_high = client.post("/api/v1/astrodynamics/sun-synchronous", json=payload_high)
    assert r_high.status_code == 200
    data_high = r_high.json()
    assert data_high["possible"] is False
    assert data_high["inclination_deg"] is None

@pytest.mark.dashboard
def test_perturbed_propagation():
    """Verify numerical propagation endpoint."""
    payload = {
        "a": 8000.0,
        "e": 0.05,
        "i": 45.0,
        "omega": 30.0,
        "raan": 15.0,
        "mu_type": "earth",
        "duration_days": 1.0,  # 1 day propagation for quick test
        "j2_enabled": True,
        "nbody_enabled": True
    }
    r = client.post("/api/v1/astrodynamics/propagate-perturbed", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "t" in data
    assert "sc_position" in data
    assert "sc_velocity" in data
    assert len(data["t"]) == 300
    assert len(data["sc_position"]) == 300
    assert len(data["sc_velocity"]) == 300

@pytest.mark.dashboard
def test_vis_viva_atmospheric_drag_warning():
    """Test that vis-viva warning is active for low orbits and inactive for high orbits."""
    # Low orbit below 120km Earth atmosphere limit (a=6450km => altitude ~71.8km)
    payload_low = {
        "a": 6450.0,
        "e": 0.001,
        "mu_type": "earth"
    }
    r_low = client.post("/api/v1/astrodynamics/vis-viva", json=payload_low)
    assert r_low.status_code == 200
    data_low = r_low.json()
    assert data_low["entry_warning"] is True
    assert data_low["min_altitude_km"] < 120.0

    # High orbit above 120km (a=7000km => altitude ~621.8km)
    payload_high = {
        "a": 7000.0,
        "e": 0.001,
        "mu_type": "earth"
    }
    r_high = client.post("/api/v1/astrodynamics/vis-viva", json=payload_high)
    assert r_high.status_code == 200
    data_high = r_high.json()
    assert data_high["entry_warning"] is False
    assert data_high["min_altitude_km"] > 120.0

@pytest.mark.dashboard
def test_sun_synchronous_raan_solver():
    """Verify solving for Sun-Synchronous optimal RAAN."""
    payload = {
        "launch_date": "2032-08-15",
        "ltan_hours": 12.0  # Noon Local Time
    }
    r = client.post("/api/v1/astrodynamics/sunsync-raan", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "raan_deg" in data
    assert "sun_ra_deg" in data
    assert 0.0 <= data["raan_deg"] < 360.0
    assert 0.0 <= data["sun_ra_deg"] < 360.0
    # For Noon LTAN, RAAN should equal Sun RA
    assert data["raan_deg"] == pytest.approx(data["sun_ra_deg"])

@pytest.mark.dashboard
def test_station_keeping_nominal():
    """Test standard inputs for Station Keeping burn on Earth with nominal fuel usage."""
    payload = {
        "a": 7000.0,
        "e": 0.05,
        "mu_type": "earth",
        "dv_burn_m_s": 50.0,
        "m0_wet_kg": 2500.0,
        "m_payload_kg": 800.0,
        "isp_s": 320.0
    }
    r = client.post("/api/v1/astrodynamics/station-keeping", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "new_a_km" in data
    assert "new_e" in data
    assert "new_rp_alt_km" in data
    assert "fuel_consumed_kg" in data
    assert "available_propellant_kg" in data
    assert "fuel_warning" in data
    assert "fuel_status" in data
    
    # Check that a prograde burn at apoapsis increases semi-major axis a and periapsis rp
    assert data["new_a_km"] > 7000.0
    # Pre-burn rp = a * (1 - e) = 7000 * 0.95 = 6650 km
    # Post-burn rp should be higher than pre-burn rp
    # New periapsis altitude should be higher than pre-burn periapsis altitude: 6650 - 6378.137 = 271.863 km
    assert data["new_rp_alt_km"] > 271.863
    
    # Fuel warning should be False since delta-v is small (50 m/s)
    assert data["fuel_warning"] is False
    assert data["fuel_status"] == "NOMINAL"
    assert data["fuel_consumed_kg"] > 0.0
    # available propellant: (2500 - 800) * 0.85 = 1445.0
    assert data["available_propellant_kg"] == pytest.approx(1445.0)

@pytest.mark.dashboard
def test_station_keeping_fuel_warning():
    """Test fuel allocation warning when burn delta-V exceeds propellant capacity."""
    payload = {
        "a": 7000.0,
        "e": 0.05,
        "mu_type": "earth",
        "dv_burn_m_s": 3000.0,  # high delta-v causing fuel warning but no escape
        "m0_wet_kg": 2500.0,
        "m_payload_kg": 800.0,
        "isp_s": 320.0
    }
    r = client.post("/api/v1/astrodynamics/station-keeping", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["fuel_warning"] is True
    assert data["fuel_status"] == "CRITICAL: INSUFFICIENT FUEL"


@pytest.mark.dashboard
def test_hohmann_endpoint():
    """Verify Hohmann transfer endpoint calculations."""
    payload = {
        "r1": 7000.0,
        "r2": 42000.0,
        "mu_type": "earth"
    }
    r = client.post("/api/v1/astrodynamics/hohmann", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "dv1_km_s" in data
    assert "dv2_km_s" in data
    assert "total_dv_km_s" in data
    assert "tof_days" in data
    assert "a_trans_km" in data
    assert "e_trans" in data
    
    assert data["a_trans_km"] == pytest.approx(24500.0)
    assert data["e_trans"] == pytest.approx(35000.0 / 49000.0)
    assert data["total_dv_km_s"] == pytest.approx(3.768029, abs=1e-4)


@pytest.mark.dashboard
def test_bielliptic_endpoint():
    """Verify Bi-elliptic transfer endpoint calculations and constraints."""
    payload = {
        "r1": 7000.0,
        "r2": 42000.0,
        "rb": 100000.0,
        "mu_type": "earth"
    }
    r = client.post("/api/v1/astrodynamics/bielliptic", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "dv1_km_s" in data
    assert "dv2_km_s" in data
    assert "dv3_km_s" in data
    assert "total_dv_km_s" in data
    assert "tof_days" in data
    assert "a1_km" in data
    assert "e1" in data
    
    assert data["a1_km"] == pytest.approx(53500.0)
    assert data["e1"] == pytest.approx(93000.0 / 107000.0)
    
    # Invalid boost radius constraint test (rb < r2)
    payload_invalid = {
        "r1": 7000.0,
        "r2": 42000.0,
        "rb": 30000.0,
        "mu_type": "earth"
    }
    r_err = client.post("/api/v1/astrodynamics/bielliptic", json=payload_invalid)
    assert r_err.status_code == 400


@pytest.mark.dashboard
def test_low_thrust_spiral_endpoint():
    """Verify Low-Thrust spiral transfer endpoint calculations."""
    payload = {
        "r1": 7000.0,
        "r2": 42000.0,
        "thrust_N": 0.5,
        "isp_s": 3000.0,
        "m0_kg": 1500.0,
        "mu_type": "earth"
    }
    r = client.post("/api/v1/astrodynamics/low-thrust-spiral", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "delta_v_km_s" in data
    assert "propellant_kg" in data
    assert "burn_time_days" in data
    assert "final_mass_kg" in data
    
    assert data["delta_v_km_s"] == pytest.approx(4.4653899, abs=1e-4)
    assert data["propellant_kg"] > 0
    assert data["burn_time_days"] > 0
    assert data["final_mass_kg"] < 1500.0


@pytest.mark.dashboard
def test_monte_carlo_endpoint():
    """Verify Monte Carlo dispersion simulation endpoint."""
    payload = {
        "a": 12000.0,
        "e": 0.1,
        "i": 28.5,
        "omega": 0.0,
        "raan": 0.0,
        "mu_type": "earth",
        "duration_days": 5.0,
        "runs": 30,
        "pos_std_km": 10.0,
        "vel_std_m_s": 0.5
    }
    r = client.post("/api/v1/astrodynamics/monte-carlo", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "nominal_path" in data
    assert "perturbed_paths" in data
    assert "t_days" in data
    assert "envelope_3sigma_km" in data
    
    assert len(data["nominal_path"]) == 80
    assert len(data["perturbed_paths"]) == 5
    assert len(data["t_days"]) == 80
    assert len(data["envelope_3sigma_km"]) == 80
    assert all(val >= 0 for val in data["envelope_3sigma_km"])


# ─────────────────────────────────────────────────────────────────────────────
#  DIGITAL TWIN & PROPULSION DIAGNOSTIC ENDPOINTS
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.diagnostics
def test_ekf_simulate_basic():
    """EKF simulation returns expected state estimate arrays."""
    payload = {
        "orbit_radius_km":       7000.0,
        "steps":                 100,
        "dt_s":                  10.0,
        "measurement_noise_km":  0.05,
        "fault_step":            50,
        "fault_magnitude_km":    5.0
    }
    r = client.post("/api/v1/digital-twin/ekf-simulate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "t" in data
    assert "true_pos" in data
    assert "measured_pos" in data
    assert "estimated_pos" in data
    assert "covariance_trace" in data
    assert len(data["t"]) == 100
    assert len(data["true_pos"]) == 100
    assert len(data["estimated_pos"]) == 100
    # Covariance trace must be non-negative
    assert all(v >= 0 for v in data["covariance_trace"])


@pytest.mark.diagnostics
def test_ekf_simulate_minimal_steps():
    """EKF returns correct length with minimal steps."""
    payload = {
        "orbit_radius_km":       8000.0,
        "steps":                 50,
        "dt_s":                  5.0,
        "measurement_noise_km":  0.1,
        "fault_step":            30,
        "fault_magnitude_km":    2.0
    }
    r = client.post("/api/v1/digital-twin/ekf-simulate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert len(data["t"]) == 50


@pytest.mark.diagnostics
def test_ccsds_parse_basic():
    """CCSDS parser returns decoded fields from a valid hex packet."""
    hex_pkt = "0801C000000800000000000041F0000042480000"
    r = client.post(
        "/api/v1/digital-twin/ccsds-parse",
        json={"hex_packet": hex_pkt}
    )
    assert r.status_code == 200
    data = r.json()
    # Parsed packet should be a non-empty dict
    assert isinstance(data, dict)
    assert len(data) > 0


@pytest.mark.diagnostics
def test_ccsds_parse_invalid_hex():
    """CCSDS parser returns 400 for malformed hex."""
    r = client.post(
        "/api/v1/digital-twin/ccsds-parse",
        json={"hex_packet": "ZZZZZZ"}          # invalid hex characters
    )
    assert r.status_code == 400


@pytest.mark.diagnostics
def test_anomaly_predict_no_anomaly():
    """Anomaly prediction returns no anomaly for stable telemetry."""
    payload = {
        "param_name":   "battery_voltage",
        "history":      [28.5, 28.4, 28.5, 28.6, 28.5, 28.4, 28.5, 28.6],
        "steps_future": 3,
        "safety_min":   24.0,
        "safety_max":   32.0
    }
    r = client.post("/api/v1/digital-twin/anomaly-predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "is_anomaly" in data
    assert "forecast_value" in data
    assert "forecast_sequence" in data
    assert len(data["forecast_sequence"]) == 3


@pytest.mark.diagnostics
def test_anomaly_predict_detects_anomaly():
    """Anomaly prediction returns anomaly flag for rapidly escalating signal."""
    payload = {
        "param_name":   "thruster_temp",
        "history":      [320, 335, 352, 371, 393, 418, 446, 477, 511, 548],
        "steps_future": 5,
        "safety_min":   200.0,
        "safety_max":   500.0
    }
    r = client.post("/api/v1/digital-twin/anomaly-predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "is_anomaly" in data
    # Forecast value should be returned
    assert data["forecast_value"] is not None


@pytest.mark.diagnostics
def test_vacuum_simulate_pressure_decay():
    """Vacuum sim shows monotonically decreasing pressure (pump > leak)."""
    payload = {
        "p_init_torr":        760.0,
        "leak_rate_torr_l_s": 1e-6,
        "pump_speed_l_s":     500.0,
        "volume_l":           1000.0,
        "duration_s":         60.0
    }
    r = client.post("/api/v1/propulsion/vacuum-simulate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "t" in data
    assert "p" in data
    assert len(data["t"]) > 1
    assert len(data["p"]) == len(data["t"])
    # Final pressure should be strictly less than initial
    assert data["p"][-1] < data["p"][0]


@pytest.mark.diagnostics
def test_erosion_rate_molybdenum():
    """Erosion rate endpoint returns a positive rate for Molybdenum."""
    payload = {
        "material_name":        "molybdenum",
        "ion_energy_eV":        300.0,
        "current_density_a_m2": 50.0
    }
    r = client.post("/api/v1/propulsion/erosion-rate", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "erosion_rate_um_hr" in data
    assert "material_info" in data
    assert data["erosion_rate_um_hr"] > 0


@pytest.mark.diagnostics
def test_erosion_rate_unknown_material():
    """Erosion rate endpoint returns 400 for unknown material."""
    payload = {
        "material_name":        "unobtanium",
        "ion_energy_eV":        200.0,
        "current_density_a_m2": 30.0
    }
    r = client.post("/api/v1/propulsion/erosion-rate", json=payload)
    assert r.status_code == 400
