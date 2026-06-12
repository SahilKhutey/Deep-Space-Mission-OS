"""
Mission Simulation Generator.
Converts mission definitions into executable simulations.
"""

import numpy as np
from datetime import datetime, timedelta
from platform.generators.base_generator import (
    BaseGenerator, SimulationConfig, SimulationResult
)
from core.constants import MU_SUN, AU
from core.astrodynamics.keplerian import solve_kepler, keplerian_to_cartesian
from core.astrodynamics.hohmann import hohmann_transfer


class MissionGenerator(BaseGenerator):
    """Generate end-to-end mission simulations."""

    MISSION_PROFILES = {
        "Earth-Moon": {
            "phases": ["Launch", "LEO", "TLI", "Cruise", "LOI", "Landing"],
            "default_dvs": [9400.0, 0.0, 3200.0, 0.0, 900.0, 1800.0]
        },
        "Earth-Mars": {
            "phases": ["Launch", "LEO", "TMI", "Cruise", "MOI", "Landing"],
            "default_dvs": [9400.0, 0.0, 3600.0, 0.0, 1500.0, 1600.0]
        },
        "Asteroid": {
            "phases": ["Launch", "Transfer", "Approach", "Rendezvous", "Science"],
            "default_dvs": [9400.0, 4500.0, 200.0, 800.0, 0.0]
        }
    }

    def validate_inputs(self, config: SimulationConfig) -> bool:
        if config.spacecraft_mass <= 0:
            return False
        if config.mission not in self.MISSION_PROFILES:
            return False
        return True

    def generate(self, config: SimulationConfig) -> SimulationResult:
        np.random.seed(config.seed)
        result = SimulationResult(config=config)

        profile = self.MISSION_PROFILES[config.mission]
        phases = profile["phases"]
        dvs = profile["default_dvs"]

        # Build timeline
        try:
            launch = datetime.strptime(config.launch_date, "%Y-%m-%d")
        except ValueError:
            launch = datetime.strptime("2035-05-01", "%Y-%m-%d")

        n_phases = len(phases)
        days_per_phase = config.duration_days / max(1, n_phases - 1)

        current_mass = config.spacecraft_mass
        cumulative_dv = 0.0
        states = []

        # Propulsion attributes (approximate mass flow calculations)
        # Assuming an Isp based on propulsion config
        isp = 3000.0 if "thruster" in config.propulsion.lower() or "hall" in config.propulsion.lower() else 320.0
        g0 = 9.80665

        for i, (phase, dv) in enumerate(zip(phases, dvs)):
            event_time = launch + timedelta(days=i * days_per_phase)
            cumulative_dv += dv

            # Mass calculation using Tsiolkovsky if dv > 0
            if dv > 0:
                mass_ratio = np.exp(dv / (isp * g0))
                final_mass = current_mass / mass_ratio
                fuel_used = current_mass - final_mass
                current_mass = final_mass
            else:
                fuel_used = 0.0

            # Power usage estimation (W)
            if "hall" in config.propulsion.lower() or "electric" in config.propulsion.lower():
                power = 1500.0 if dv > 0 else 200.0
            else:
                power = 150.0 if dv > 0 else 50.0

            # Thermal load (W)
            thermal = power * 0.4 if dv > 0 else power * 0.1

            entry = {
                "phase": phase,
                "timestamp": event_time.isoformat(),
                "delta_v_m_s": float(dv),
                "cumulative_dv_m_s": float(cumulative_dv),
                "spacecraft_mass_kg": float(current_mass),
                "fuel_used_kg": float(fuel_used),
                "position_km": self._phase_position(phase, config.mission, i),
                "velocity_km_s": self._phase_velocity(phase, dv),
                "power_W": float(power),
                "thermal_W": float(thermal),
                "t_s": float(i * days_per_phase * 86400.0)
            }
            result.timeline.append(entry)
            states.append(entry)

        result.states = states
        result.fuel_profile = [s["fuel_used_kg"] for s in states]
        result.power_profile = [s["power_W"] for s in states]
        result.thermal_profile = [s["thermal_W"] for s in states]
        result.trajectory = [s["position_km"] for s in states]
        result.validation_status = "VALID"
        return result

    def _phase_position(self, phase, mission, i):
        """Generate representative position for a phase."""
        if mission == "Earth-Mars":
            # Heliocentric transfer arc
            theta = np.pi * i / 5.0
            r = (1.496e8 + (2.279e8 - 1.496e8) * i / 5.0)
            return [float(r * np.cos(theta)), float(r * np.sin(theta)), 0.0]
        elif mission == "Earth-Moon":
            # Geocentric transfer
            r = 384400.0 * i / 5.0
            return [float(r), 0.0, 0.0]
        return [0.0, 0.0, 0.0]

    def _phase_velocity(self, phase, dv):
        """Representative velocity magnitude (km/s)."""
        return 0.0 if dv == 0 else float(dv / 1000.0)
