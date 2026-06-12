"""
Deep Space SDK Client library.
"""

from deep_space_core.astrodynamics import vis_viva, solve_kepler
from deep_space_core.trajectories.hohmann import hohmann_transfer
from deep_space_core.astrodynamics.lambert import lambert_universal
from deep_space_mission_planner.mission_engine.planner import MissionEngine
from deep_space_mission_planner.mission_engine.risk_cost_engines import MissionRiskEngine, CostEstimationEngine
from deep_space_digital_twin.ai_twin import AIDigitalTwin

class DeepSpaceClient:
    def __init__(self):
        self.planner = MissionEngine()
        self.risk_engine = MissionRiskEngine()
        self.cost_engine = CostEstimationEngine()
        self.twin = AIDigitalTwin()

    def get_orbit_velocity(self, r, a, mu):
        return vis_viva(r, a, mu)

    def plan_mission(self, origin, destination, payload_mass_kg):
        mission = {
            "origin": origin,
            "destination": destination,
            "spacecraft_mass": payload_mass_kg * 3.0,
            "payload_mass": payload_mass_kg
        }
        return self.planner.plan(mission)

    def estimate_mission_cost(self, dry_mass, propellant_mass, launch_cost, ops_months):
        return self.cost_engine.estimate_cost(dry_mass, propellant_mass, launch_cost, ops_months)

    def compute_mission_risk(self, duration_days, radiation_rads, components):
        return self.risk_engine.compute_risk(duration_days, radiation_rads, components)

    def log_twin_state(self, param_name, val):
        self.twin.log_state(param_name, val)

    def forecast_twin_state(self, param_name, steps_future):
        return self.twin.forecast_state(param_name, steps_future)

    def predict_twin_anomaly(self, param_name, steps_future, safety_bounds):
        return self.twin.predict_anomaly(param_name, steps_future, safety_bounds)
