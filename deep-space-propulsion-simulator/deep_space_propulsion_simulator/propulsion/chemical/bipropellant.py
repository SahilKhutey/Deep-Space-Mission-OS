"""
Bipropellant chemical rocket engine models.
"""

from deep_space_core.constants import G0

class BipropellantEngine:
    def __init__(self, name):
        self.name = name
        if name == "RL-10":
            self.Isp = 450.0
            self.thrust = 1.1e5
        elif name == "Raptor":
            self.Isp = 380.0
            self.thrust = 2.2e6
        elif name == "Merlin":
            self.Isp = 311.0
            self.thrust = 9.81e5
        else:
            self.Isp = 300.0
            self.thrust = 1.0e5
            
    def mass_flow_rate(self):
        return self.thrust / (self.Isp * G0)
