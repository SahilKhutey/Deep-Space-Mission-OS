"""
Thermal digital twin simulating heating, cooling, and radiation in space.
"""

import numpy as np

SIGMA = 5.670374419e-8

class ThermalTwin:
    def __init__(self, mass_kg=100.0, specific_heat=900.0, surface_area=6.0, emissivity=0.8, initial_temp_k=290.0):
        self.mass = mass_kg
        self.cp = specific_heat
        self.area = surface_area
        self.emissivity = emissivity
        self.temp = initial_temp_k

    def update(self, Q_internal_w, Q_solar_w, heater_power_w=0.0, cooler_power_w=0.0, dt_sec=60.0):
        # Radiative heat rejection: Q = sigma * epsilon * A * T^4
        Q_rad = SIGMA * self.emissivity * self.area * (self.temp ** 4)

        # Net heat rate
        Q_net = Q_internal_w + Q_solar_w + heater_power_w - cooler_power_w - Q_rad

        # dT = Q_net * dt / (m * cp)
        dT = Q_net * dt_sec / (self.mass * self.cp)
        self.temp += dT

        return {
            "temperature_k": self.temp,
            "q_rad_w": Q_rad,
            "q_net_w": Q_net
        }
