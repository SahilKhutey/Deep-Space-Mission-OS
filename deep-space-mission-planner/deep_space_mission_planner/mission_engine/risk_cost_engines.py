"""
Mission Risk and Cost Estimation engines.
"""

import numpy as np

class MissionRiskEngine:
    def compute_risk(self, mission_duration_days, solar_radiation_rads, component_count):
        """
        Calculates a baseline failure probability based on:
        - mission_duration_days
        - solar_radiation_rads (Total Ionizing Dose)
        - component_count (number of critical parts)
        """
        base_lambda = 1e-6
        rad_factor = 1.0 + (solar_radiation_rads / 1e5)
        
        effective_lambda = base_lambda * rad_factor * component_count
        reliability = np.exp(-effective_lambda * mission_duration_days)
        failure_prob = 1.0 - reliability
        return float(failure_prob)

class CostEstimationEngine:
    def estimate_cost(self, dry_mass_kg, propellant_mass_kg, launch_vehicle_cost_usd, mission_ops_months):
        """
        Computes total estimated mission cost.
        """
        dry_mass_cost = dry_mass_kg * 15000.0
        propellant_cost = propellant_mass_kg * 5.0
        ops_cost = mission_ops_months * 50000.0
        total_cost = launch_vehicle_cost_usd + dry_mass_cost + propellant_cost + ops_cost
        return {
            "dry_mass_cost_usd": dry_mass_cost,
            "propellant_cost_usd": propellant_cost,
            "ops_cost_usd": ops_cost,
            "total_cost_usd": total_cost
        }
