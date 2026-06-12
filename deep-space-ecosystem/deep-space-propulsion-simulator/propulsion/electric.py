"""
Electric Propulsion Thruster Models
Defines Ion thrusters and Hall thrusters, including specific power and sizing constraints.
"""

import numpy as np
from deep_space_core.constants import G0


def propellant_mass(Isp, m0, target_dv):
    """Compute required propellant mass for a target delta-V."""
    if m0 <= 0:
        raise ValueError("Initial mass must be positive.")
    if Isp <= 0:
        raise ValueError("Specific impulse Isp must be positive.")
    mass_ratio = np.exp(target_dv / (Isp * G0))
    m_prop = m0 * (1.0 - 1.0 / mass_ratio)
    m_dry = m0 - m_prop
    return {
        "fuel_mass": m_prop,
        "dry_mass": m_dry,
        "propellant_fraction": m_prop / m0,
        "mass_ratio": mass_ratio
    }


class IonThruster:
    """
    Electric Ion/Hall thruster sizing and performance.
    """
    
    MODELS = {
        "NSTAR": {
            "Isp": 3100.0,        # specific impulse (s)
            "thrust_N": 0.092,    # thrust (N)
            "power_W": 2300.0,    # electric power requirement (W)
            "propellant": "Xenon"
        },
        "NEXT": {
            "Isp": 4190.0,        # specific impulse (s)
            "thrust_N": 0.236,    # thrust (N)
            "power_W": 6900.0,    # electric power requirement (W)
            "propellant": "Xenon"
        },
        "BHT-600": {
            "Isp": 1500.0,        # specific impulse (s)
            "thrust_N": 0.040,    # thrust (N)
            "power_W": 600.0,     # electric power requirement (W)
            "propellant": "Xenon"  # Hall thruster
        },
        "PPS-1350": {
            "Isp": 1660.0,        # specific impulse (s)
            "thrust_N": 0.090,    # thrust (N)
            "power_W": 1500.0,    # electric power requirement (W)
            "propellant": "Xenon"  # Hall thruster
        }
    }
    
    def __init__(self, name="NSTAR"):
        if name not in self.MODELS:
            raise ValueError(f"Unknown electric thruster: {name}. Available: {list(self.MODELS.keys())}")
        self.name = name
        self.specs = self.MODELS[name]
        self.Isp = self.specs["Isp"]
        self.thrust = self.specs["thrust_N"]
        self.power = self.specs["power_W"]
        self.propellant = self.specs["propellant"]
        
    def specific_power(self):
        """
        Computes specific power (W/N), i.e. power required per Newton of thrust.
        """
        if self.thrust <= 0:
            return 0.0
        return self.power / self.thrust
        
    def jet_power(self):
        """
        Computes the kinetic jet power (W) of the exhaust beam: P_jet = 0.5 * thrust * v_exhaust
        """
        ve = self.Isp * G0
        return 0.5 * self.thrust * ve
        
    def efficiency(self):
        """
        Computes electrical efficiency of the thruster: P_jet / P_electrical
        """
        if self.power <= 0:
            return 0.0
        return self.jet_power() / self.power
        
    def compute_propellant_for_burn(self, m0_kg, target_dv_m_s):
        """
        Calculates the propellant mass required for a specific Delta-V burn.
        """
        res = propellant_mass(self.Isp, m0_kg, target_dv_m_s)
        res.update({
            "thruster_name": self.name,
            "propellant_type": self.propellant,
            "power_W": self.power
        })
        return res
        
    def burn_time(self, m0_kg, target_dv_m_s):
        """
        Computes the time required to complete the burn under constant thrust.
        """
        res = self.compute_propellant_for_burn(m0_kg, target_dv_m_s)
        m_prop = res["fuel_mass"]
        
        # Propellant mass flow rate (kg/s)
        m_dot = self.thrust / (self.Isp * G0)
        
        return m_prop / m_dot
