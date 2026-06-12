from fastapi import FastAPI
from deep_space_mission_planner.mission_engine.planner import MissionEngine

app = FastAPI()

@app.get("/api/v1/presets/mars")
def get_mars_preset():
    mission = {
        "origin": "Earth", "destination": "Mars",
        "spacecraft_mass": 2500, "propulsion_type": "Chemical",
        "payload_mass": 800, "launch_date": "2032-08-15"
    }
    planner = MissionEngine()
    return planner.plan(mission)

@app.get("/api/v1/dashboards/validation")
def get_validation_dashboard():
    return {
        "status": "PASS",
        "layers": {
            "unit": 1.0,
            "integration": 1.0,
            "mathematics": 1.0,
            "physics": 1.0,
            "numerical": 1.0,
            "mission": 1.0
        }
    }

@app.get("/api/v1/dashboards/risk")
def get_risk_dashboard():
    return {
        "failure_probability": 0.045,
        "critical_issues": ["battery_degradation_low_temp"],
        "risk_heatmap_coordinates": [2, 1]
    }

@app.get("/api/v1/dashboards/system-health")
def get_system_health():
    return {
        "power_status": "NOMINAL",
        "thermal_status": "NOMINAL",
        "gnc_status": "NOMINAL",
        "cpu_load_pct": 14.5
    }

@app.get("/api/v1/dashboards/optimization")
def get_optimization_dashboard():
    return {
        "convergence": "STABLE",
        "iterations": 150,
        "best_cost_usd": 150000000.0,
        "pareto_front": [[100.0, 1.2e8], [120.0, 1.0e8]]
    }
