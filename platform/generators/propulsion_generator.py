"""
Propulsion Simulation Generator.
"""

import numpy as np
from platform.generators.base_generator import (
    BaseGenerator, SimulationConfig, SimulationResult
)


class PropulsionGenerator(BaseGenerator):
    """Generate thrust, Isp, mass flow, power, and thermal profiles."""

    ENGINE_DATABASE = {
        "Chemical": {"Isp": 320.0, "thrust_N": 1e5, "efficiency": 0.95},
        "Hall Thruster": {"Isp": 1500.0, "thrust_N": 0.1, "efficiency": 0.60},
        "Ion Thruster": {"Isp": 3000.0, "thrust_N": 0.05, "efficiency": 0.70},
        "Nuclear": {"Isp": 900.0, "thrust_N": 5e5, "efficiency": 0.40}
    }

    def validate_inputs(self, config):
        return config.propulsion in self.ENGINE_DATABASE

    def generate(self, config: SimulationConfig) -> SimulationResult:
        np.random.seed(config.seed)
        result = SimulationResult(config=config)

        engine = self.ENGINE_DATABASE[config.propulsion]
        Isp = engine["Isp"]
        thrust = engine["thrust_N"]
        eff = engine["efficiency"]

        # Time resolution
        n_steps = 100
        t = np.linspace(0.0, config.duration_days * 86400.0, n_steps)
        thrust_curve = np.full(n_steps, thrust)
        isp_curve = np.full(n_steps, Isp)

        # Mass flow: ṁ = F / (Isp · g₀)
        g0 = 9.80665
        mass_flow = thrust / (Isp * g0)
        mass_flow_curve = np.full(n_steps, mass_flow)

        # Power: P = F² / (2·ṁ·η)  (for electric); for chemical use stagnation
        if config.propulsion in ["Hall Thruster", "Ion Thruster"]:
            power = thrust**2 / (2.0 * mass_flow * eff)
            power_curve = np.full(n_steps, power)
        else:
            power_curve = np.full(n_steps, 0.0)

        # Thermal: Q_rad = η · P (waste heat)
        thermal_curve = power_curve * (1.0 - eff)

        result.states = [
            {
                "t_s": float(t[i]),
                "thrust_N": float(thrust_curve[i]),
                "Isp_s": float(isp_curve[i]),
                "mass_flow_kg_s": float(mass_flow_curve[i]),
                "power_W": float(power_curve[i]),
                "thermal_W": float(thermal_curve[i])
            }
            for i in range(n_steps)
        ]
        result.fuel_profile = [s["mass_flow_kg_s"] for s in result.states]
        result.power_profile = [s["power_W"] for s in result.states]
        result.thermal_profile = [s["thermal_W"] for s in result.states]
        result.validation_status = "VALID"
        return result
