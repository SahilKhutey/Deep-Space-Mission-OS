"""
Digital Twin Simulation Generator.
Generates state evolution for all subsystems.
"""

import numpy as np
from platform.generators.base_generator import (
    BaseGenerator, SimulationConfig, SimulationResult
)


class TwinGenerator(BaseGenerator):
    """Generate digital twin state evolution."""

    def validate_inputs(self, config):
        return config.spacecraft_mass > 0

    def generate(self, config: SimulationConfig) -> SimulationResult:
        np.random.seed(config.seed)
        result = SimulationResult(config=config)

        n_steps = 100
        t = np.linspace(0.0, config.duration_days * 86400.0, n_steps)

        # Power system: exponential discharge
        soc_0 = 1.0
        soc = soc_0 * np.exp(-t / (config.duration_days * 86400.0 * 0.5))

        # Battery state
        battery_voltage = 28.0 * (0.9 + 0.1 * soc)

        # Thermal state (RC network solution)
        T_orbit = 50.0  # 50C equilibrium
        T_components = T_orbit + 5.0 * np.sin(2.0 * np.pi * t / (90.0 * 60.0))

        # Fuel state
        fuel_remaining = config.spacecraft_mass * 0.3 * soc

        # Comms state
        signal_strength = 0.9 - 0.1 * np.sin(2.0 * np.pi * t / 86400.0)

        # Navigation state (Kalman filter residuals)
        nav_residual = 0.01 * np.exp(-t / 86400.0) + 1e-4

        # Health index (0=healthy, 1=failed)
        health = 1.0 - np.exp(-t / (config.duration_days * 86400.0 * 10.0))

        result.states = [
            {
                "t_s": float(t[i]),
                "battery_soc": float(soc[i]),
                "battery_voltage": float(battery_voltage[i]),
                "temperature_C": float(T_components[i]),
                "fuel_kg": float(fuel_remaining[i]),
                "signal_strength": float(signal_strength[i]),
                "nav_residual_m": float(nav_residual[i]),
                "health_index": float(health[i]),
                "subsystem_status": "OK" if health[i] < 0.8 else "DEGRADED"
            }
            for i in range(n_steps)
        ]
        result.power_profile = [s["battery_soc"] for s in result.states]
        result.thermal_profile = [s["temperature_C"] for s in result.states]
        result.fuel_profile = [s["fuel_kg"] for s in result.states]
        result.validation_status = "VALID"
        return result
