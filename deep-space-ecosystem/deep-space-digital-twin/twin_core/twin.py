"""
Spacecraft Digital Twin Core Orchestrator
Manages state propagation across all subsystems and runs anomaly detection.
"""

import numpy as np
from spacecraft.subsystems import (
    PowerSubsystem, ThermalSubsystem, AvionicsSubsystem, GNCSubsystem, CommsSubsystem
)
from deep_space_core.constants import AU


class SpacecraftTwin:
    """Central orchestrator for the Spacecraft Digital Twin."""

    def __init__(self, spacecraft_mass=1500.0, payload_mass=300.0):
        self.mass = spacecraft_mass
        self.payload_mass = payload_mass
        self.total_mass = spacecraft_mass + payload_mass
        
        # Initialize subsystem models
        self.power = PowerSubsystem()
        self.thermal = ThermalSubsystem()
        self.avionics = AvionicsSubsystem()
        self.gnc = GNCSubsystem()
        self.comms = CommsSubsystem()

    def propagate_state(self, duration_days=5.0, dt_s=3600.0,
                        trajectory_distance_sun_km=None,
                        trajectory_distance_earth_km=None,
                        is_thrusting=False):
        """
        Propagate states of all subsystems over time.
        """
        n_steps = int((duration_days * 86400.0) / dt_s)
        telemetry = []
        
        # Default transit path (dynamic distancing)
        curr_dist_sun = 1.0 * AU
        curr_dist_earth = 0.01 * AU
        
        for step in range(n_steps):
            t_elapsed_s = step * dt_s
            
            # Update physical distances
            if trajectory_distance_sun_km is not None:
                if isinstance(trajectory_distance_sun_km, list):
                    curr_dist_sun = trajectory_distance_sun_km[min(step, len(trajectory_distance_sun_km)-1)]
                else:
                    curr_dist_sun = trajectory_distance_sun_km
            else:
                # Approximate Earth-Mars transit distance increase
                curr_dist_sun += 0.05 * AU * (dt_s / 86400.0)
                
            if trajectory_distance_earth_km is not None:
                if isinstance(trajectory_distance_earth_km, list):
                    curr_dist_earth = trajectory_distance_earth_km[min(step, len(trajectory_distance_earth_km)-1)]
                else:
                    curr_dist_earth = trajectory_distance_earth_km
            else:
                curr_dist_earth += 0.04 * AU * (dt_s / 86400.0)

            # 1. Power generation calculations
            solar_power_w = self.power.compute_solar_power(curr_dist_sun)
            
            # Components power consumption
            avionics_load = 150.0 # W
            gnc_load = 200.0 if is_thrusting else 80.0
            comms_load = 120.0
            heater_load = 0.0
            
            # Activate heater if temperature drops below 5 C
            current_temp = self.thermal.temperature_K - 273.15
            if current_temp < 5.0:
                heater_load = 150.0
                
            total_load_w = avionics_load + gnc_load + comms_load + heater_load
            
            # Evolve Power states
            soc, voltage = self.power.evolve(dt_s, solar_power_w, total_load_w)
            
            # 2. Evolve Thermal states
            temp_c = self.thermal.evolve(dt_s, self.total_mass, curr_dist_sun, total_load_w, heater_load)
            
            # 3. Evolve Avionics states
            cpu, mem, buf = self.avionics.evolve(dt_s, active_comms=True, processing_burn=is_thrusting)
            
            # 4. Evolve GNC states
            att_err, wheels, kalman_res = self.gnc.evolve(dt_s, is_thrusting=is_thrusting)
            
            # 5. Evolve Comms states
            link_q, path_loss, signal_dbm = self.comms.compute_link_quality(curr_dist_earth, att_err)
            
            # Construct Telemetry Frame
            telemetry.append({
                "timestamp_s": t_elapsed_s,
                "solar_power_w": solar_power_w,
                "electrical_load_w": total_load_w,
                "battery_soc": soc,
                "battery_voltage": voltage,
                "temperature_C": temp_c,
                "cpu_load": cpu,
                "memory_used": mem,
                "buffer_occupancy_MB": buf,
                "attitude_error_deg": att_err,
                "wheel_speeds_rpm": wheels,
                "kalman_residual": kalman_res,
                "link_quality": link_q,
                "path_loss_db": path_loss,
                "signal_dbm": signal_dbm,
                "distance_to_sun_km": curr_dist_sun,
                "distance_to_earth_km": curr_dist_earth
            })
            
        return telemetry

    def detect_anomalies(self, telemetry):
        """
        Scan telemetry sequence and return a list of detected anomalies.
        """
        anomalies = []
        for frame in telemetry:
            t = frame["timestamp_s"]
            
            # Battery check
            if frame["battery_soc"] < 0.15:
                anomalies.append({
                    "timestamp_s": t,
                    "subsystem": "Power",
                    "severity": "CRITICAL",
                    "code": "LOW_BATTERY_SOC",
                    "message": f"Battery SoC fell to {frame['battery_soc']:.3f}"
                })
                
            # Thermal check
            if frame["temperature_C"] > 75.0:
                anomalies.append({
                    "timestamp_s": t,
                    "subsystem": "Thermal",
                    "severity": "CRITICAL",
                    "code": "OVERHEATING",
                    "message": f"Spacecraft temperature exceeded threshold: {frame['temperature_C']:.2f} C"
                })
            elif frame["temperature_C"] < -30.0:
                anomalies.append({
                    "timestamp_s": t,
                    "subsystem": "Thermal",
                    "severity": "WARNING",
                    "code": "UNDERCOOLING",
                    "message": f"Spacecraft temperature below limit: {frame['temperature_C']:.2f} C"
                })
                
            # GNC check
            if frame["attitude_error_deg"] > 1.5:
                anomalies.append({
                    "timestamp_s": t,
                    "subsystem": "GNC",
                    "severity": "WARNING",
                    "code": "POINTING_ERROR",
                    "message": f"Attitude error exceeded limit: {frame['attitude_error_deg']:.3f} deg"
                })
                
            # Comms check
            if frame["link_quality"] < 0.05:
                anomalies.append({
                    "timestamp_s": t,
                    "subsystem": "Comms",
                    "severity": "WARNING",
                    "code": "LOW_SIGNAL_STRENGTH",
                    "message": f"Comms link quality degraded: {frame['link_quality']:.3f}"
                })
                
            # Navigation filter check
            if frame["kalman_residual"] > 0.2:
                anomalies.append({
                    "timestamp_s": t,
                    "subsystem": "GNC",
                    "severity": "WARNING",
                    "code": "NAVIGATION_FILTER_DRIFT",
                    "message": f"Kalman filter residuals exceeded limit: {frame['kalman_residual']:.4f}"
                })
                
        return anomalies
