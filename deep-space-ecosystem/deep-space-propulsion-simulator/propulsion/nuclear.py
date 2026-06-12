"""
Nuclear Propulsion Engine Models
Defines Nuclear Thermal Propulsion (NTP) and Nuclear Electric Propulsion (NEP) performance profiles.
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


class NuclearEngine:
    """
    Nuclear Space Propulsion (NTP / NEP) sizing and performance.
    """
    
    MODELS = {
        "NERVA": {
            "type": "NTP",
            "Isp": 850.0,         # specific impulse (s)
            "thrust_N": 333000.0,  # thrust (N)
            "propellant": "Liquid Hydrogen"
        },
        "Pewee": {
            "type": "NTP",
            "Isp": 925.0,         # specific impulse (s)
            "thrust_N": 111000.0,  # thrust (N)
            "propellant": "Liquid Hydrogen"
        },
        "NEP-500kW": {
            "type": "NEP",
            "Isp": 5000.0,         # specific impulse (s)
            "power_W": 500000.0,   # electrical power output of fission reactor (W)
            "efficiency": 0.65,    # thruster beam efficiency
            "specific_mass_kg_kW": 8.0, # alpha value for mass modeling (kg/kW)
            "propellant": "Xenon"
        }
    }
    
    def __init__(self, name="NERVA"):
        if name not in self.MODELS:
            raise ValueError(f"Unknown nuclear engine: {name}. Available: {list(self.MODELS.keys())}")
        self.name = name
        self.specs = self.MODELS[name]
        self.type = self.specs["type"]
        self.Isp = self.specs["Isp"]
        self.propellant = self.specs["propellant"]
        
        if self.type == "NTP":
            self.thrust = self.specs["thrust_N"]
            self.power = 0.0
            self.efficiency = 1.0
        else: # NEP
            self.power = self.specs["power_W"]
            self.efficiency = self.specs["efficiency"]
            self.specific_mass = self.specs["specific_mass_kg_kW"]
            # T = 2 * eta * P / (Isp * g0)
            self.thrust = (2.0 * self.efficiency * self.power) / (self.Isp * G0)
            
    def reactor_mass(self):
        """
        Computes the dry mass of the power conversion and reactor system for NEP (kg).
        """
        if self.type == "NTP":
            return 0.0
        # Specific mass is in kg/kW
        return self.specific_mass * (self.power / 1000.0)
        
    def compute_propellant_for_burn(self, m0_kg, target_dv_m_s):
        """
        Calculates the propellant mass required for a specific Delta-V burn.
        """
        res = propellant_mass(self.Isp, m0_kg, target_dv_m_s)
        res.update({
            "engine_name": self.name,
            "engine_type": self.type,
            "propellant_type": self.propellant,
            "thrust_N": self.thrust
        })
        if self.type == "NEP":
            res["reactor_mass_kg"] = self.reactor_mass()
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
