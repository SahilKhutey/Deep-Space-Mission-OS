"""
Electric propulsion models (Hall and Gridded Ion thrusters).
"""

from deep_space_core.constants import G0

class ElectricThruster:
    def __init__(self, name):
        self.name = name
        if name == "NEXT":
            self.power = 6900.0  # Watts
            self.thrust = 0.236  # Newtons
            self.efficiency = 0.70
            self.Isp = 4190.0
        elif name == "NSTAR":
            self.power = 2300.0
            self.thrust = 0.092
            self.efficiency = 0.61
            self.Isp = 3100.0
        elif name == "SPT-100":
            self.power = 1350.0
            self.thrust = 0.083
            self.efficiency = 0.50
            self.Isp = 1600.0
        elif name == "PPS-1350":
            self.power = 1500.0
            self.thrust = 0.090
            self.efficiency = 0.50
            self.Isp = 1660.0
        else:
            self.power = 1000.0
            self.thrust = 0.05
            self.efficiency = 0.50
            self.Isp = 2000.0

    def mass_flow_rate(self):
        return self.thrust / (self.Isp * G0)
