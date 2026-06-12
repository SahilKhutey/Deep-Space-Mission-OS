"""
Spacecraft Subsystems Performance and Sizing Models
Includes mathematical formulations for Power, Thermal, Avionics, GNC, and Comms states.
"""

import numpy as np
from deep_space_core.constants import AU


class PowerSubsystem:
    """Power subsystem modeling battery charge and solar panel output."""

    def __init__(self, panel_area=15.0, efficiency=0.3, battery_capacity_Wh=5000.0):
        self.panel_area = panel_area
        self.efficiency = efficiency
        self.battery_capacity_Wh = battery_capacity_Wh
        self.soc = 1.0  # State of Charge [0.0 - 1.0]

    def compute_solar_power(self, distance_to_sun_km):
        """Compute solar array power generation using 1/d^2 scaling."""
        dist_AU = distance_to_sun_km / AU
        # Solar constant at 1 AU is ~1361 W/m^2
        flux = 1361.0 / (dist_AU ** 2)
        power_w = flux * self.panel_area * self.efficiency
        return max(0.0, power_w)

    def evolve(self, dt_s, solar_power_w, load_w):
        """Evolve battery state of charge."""
        net_power_W = solar_power_w - load_w
        # Convert net power to Watt-hours change
        dWh = net_power_W * (dt_s / 3600.0)
        
        # New capacity in Wh
        current_Wh = self.soc * self.battery_capacity_Wh + dWh
        self.soc = np.clip(current_Wh / self.battery_capacity_Wh, 0.0, 1.0)
        
        # Nominal 28V bus voltage varies with SoC
        voltage = 28.0 * (0.85 + 0.15 * self.soc)
        return self.soc, voltage


class ThermalSubsystem:
    """Thermal subsystem modeling spacecraft radiative balance."""

    def __init__(self, emissivity=0.85, absorptivity=0.9, radiator_area=4.0, cp_j_kg_k=900.0):
        self.emissivity = emissivity
        self.absorptivity = absorptivity
        self.radiator_area = radiator_area
        self.cp = cp_j_kg_k  # Specific heat capacity
        self.temperature_K = 293.15  # Nominal 20 C in Kelvin

    def evolve(self, dt_s, mass_kg, distance_to_sun_km, electrical_load_w, heater_power_w):
        """Evolve temperature based on solar absorption, internal dissipation, and radiator emission."""
        dist_AU = distance_to_sun_km / AU
        solar_flux = 1361.0 / (dist_AU ** 2)
        
        # Stefan-Boltzmann constant
        sigma = 5.670374e-8
        
        # Heat inputs
        Q_solar = solar_flux * self.absorptivity * (self.radiator_area * 0.25) # simplified projected area
        Q_internal = electrical_load_w # power dissipated as heat
        Q_heater = heater_power_w
        
        # Heat output via radiator
        T_space = 2.7
        Q_out = sigma * self.emissivity * self.radiator_area * (self.temperature_K**4 - T_space**4)
        
        # Net thermal energy
        Q_net = Q_solar + Q_internal + Q_heater - Q_out
        
        # Thermal mass (mass * cp)
        thermal_mass = mass_kg * self.cp
        dT = (Q_net / thermal_mass) * dt_s
        
        self.temperature_K = np.clip(self.temperature_K + dT, 50.0, 500.0)
        return self.temperature_K - 273.15  # Celsius


class AvionicsSubsystem:
    """Avionics processor and memory state evolution."""

    def __init__(self):
        self.cpu_load = 15.0  # percentage
        self.memory_used = 10.0  # percentage
        self.buffer_occupancy = 0.0  # MBytes

    def evolve(self, dt_s, active_comms=False, processing_burn=False):
        """Evolve cpu load and memory usage."""
        base_cpu = 10.0
        if processing_burn:
            base_cpu += 45.0
        if active_comms:
            base_cpu += 20.0
            
        noise = np.random.normal(0.0, 2.0)
        self.cpu_load = np.clip(base_cpu + noise, 0.0, 100.0)
        
        # Memory slowly fills, or flushes during comms
        if active_comms:
            self.buffer_occupancy = max(0.0, self.buffer_occupancy - 1.5 * (dt_s / 60.0))
        else:
            self.buffer_occupancy += 0.05 * (dt_s / 60.0)  # Telemetry collection
            
        self.memory_used = np.clip(15.0 + self.buffer_occupancy / 10.0, 0.0, 100.0)
        return self.cpu_load, self.memory_used, self.buffer_occupancy


class GNCSubsystem:
    """Guidance, Navigation, and Control state tracking."""

    def __init__(self):
        self.attitude_error_deg = 0.05
        self.wheel_speed_rpm = np.array([500.0, -500.0, 200.0])
        self.kalman_residual = 0.01

    def evolve(self, dt_s, is_thrusting=False):
        """Evolve GNC error vectors and filter residual states."""
        if is_thrusting:
            # Thrusting increases attitude error due to misalignment
            self.attitude_error_deg = np.clip(self.attitude_error_deg + np.random.normal(0.05, 0.01), 0.0, 5.0)
            self.wheel_speed_rpm += np.random.normal(5.0, 2.0, 3) * dt_s
        else:
            # Normal wheel control maintains pointing
            self.attitude_error_deg = np.clip(self.attitude_error_deg * 0.9 + np.random.normal(0.0, 0.005), 0.0, 1.0)
            self.wheel_speed_rpm += np.random.normal(0.0, 0.1, 3) * dt_s
            
        # Desaturate wheels if they get close to 5000 RPM
        for idx in range(3):
            if abs(self.wheel_speed_rpm[idx]) > 4500.0:
                self.wheel_speed_rpm[idx] *= 0.1  # desaturate using thruster momentum dump
                
        # Kalman filter navigation residual decay
        self.kalman_residual = np.clip(self.kalman_residual * 0.98 + np.random.normal(0.0, 0.0005), 1e-5, 0.5)
        return self.attitude_error_deg, self.wheel_speed_rpm.tolist(), self.kalman_residual


class CommsSubsystem:
    """Communications link budget and status tracking."""

    def __init__(self, transmit_power_w=20.0, carrier_freq_ghz=8.4):
        self.transmit_power_w = transmit_power_w
        self.carrier_freq = carrier_freq_ghz

    def compute_link_quality(self, distance_to_earth_km, pointing_error_deg):
        """Compute path loss and approximate signal-to-noise ratio."""
        # Free-space path loss formula: FSPL = (4 * pi * d / lambda)^2
        # speed of light c = 299792458 m/s, frequency in Hz
        c_speed = 299792458.0
        freq_hz = self.carrier_freq * 1e9
        wavelength = c_speed / freq_hz
        
        dist_m = distance_to_earth_km * 1000.0
        
        # Logarithmic path loss in dB
        fspl_db = 20.0 * np.log10(4.0 * np.pi * dist_m / wavelength)
        
        # Transmit power in dBW
        p_tx_dbw = 10.0 * np.log10(self.transmit_power_w)
        
        # Pointing loss estimation: 12 * (error / beamwidth)^2
        beamwidth_deg = 1.5
        pointing_loss_db = 12.0 * (pointing_error_deg / beamwidth_deg) ** 2
        
        # Received signal strength representation
        signal_dbm = p_tx_dbw + 30.0 - fspl_db - pointing_loss_db
        
        # Normalized quality factor [0.0 - 1.0]
        quality = np.clip(1.0 - (abs(signal_dbm) - 50.0) / 150.0, 0.0, 1.0)
        return quality, fspl_db, signal_dbm
