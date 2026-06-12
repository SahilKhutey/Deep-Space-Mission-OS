"""
Bipropellant Chemical Propulsion Engine Models
Defines MMH/NTO and cryogenic LH2/LOX performance profiles and sizing equations.
"""

from core.fuel_models.tsiolkovsky import propellant_mass, delta_v
from core.constants import G0

class BipropellantEngine:
    """
    Chemical Bipropellant Rocket Engine sizing and performance.
    """
    
    # Engine database containing industry standard bipropellant profiles
    ENGINES = {
        "Raptor": {
            "Isp": 380.0,         # vacuum specific impulse (s)
            "thrust_N": 2.2e6,     # vacuum thrust (N)
            "propellants": "LOX/LCH4",
            "mixture_ratio": 3.6
        },
        "RL-10": {
            "Isp": 465.5,         # vacuum specific impulse (s)
            "thrust_N": 1.1e5,     # vacuum thrust (N)
            "propellants": "LOX/LH2",
            "mixture_ratio": 5.88
        },
        "Vulcain": {
            "Isp": 431.0,         # vacuum specific impulse (s)
            "thrust_N": 1.39e6,    # vacuum thrust (N)
            "propellants": "LOX/LH2",
            "mixture_ratio": 6.0
        },
        "Merlin": {
            "Isp": 348.0,         # vacuum specific impulse (s)
            "thrust_N": 9.81e5,    # vacuum thrust (N)
            "propellants": "LOX/RP-1",
            "mixture_ratio": 2.56
        },
        "Aerojet-R4D": {
            "Isp": 312.0,         # vacuum specific impulse (s)
            "thrust_N": 490.0,     # vacuum thrust (N)
            "propellants": "NTO/MMH",
            "mixture_ratio": 1.65
        }
    }
    
    def __init__(self, name="RL-10"):
        if name not in self.ENGINES:
            raise ValueError(f"Unknown chemical engine: {name}. Available: {list(self.ENGINES.keys())}")
        self.name = name
        self.specs = self.ENGINES[name]
        self.Isp = self.specs["Isp"]
        self.thrust = self.specs["thrust_N"]
        self.propellants = self.specs["propellants"]
        self.mixture_ratio = self.specs["mixture_ratio"]
        
    def compute_propellant_for_burn(self, m0_kg, target_dv_m_s):
        """
        Calculates the propellant mass required for a specific Delta-V burn.
        """
        res = propellant_mass(self.Isp, m0_kg, target_dv_m_s)
        # Add mixture-specific details
        m_prop = res["fuel_mass"]
        mr = self.mixture_ratio
        
        # m_oxidizer + m_fuel = m_prop
        # m_oxidizer / m_fuel = mr -> m_oxidizer = mr * m_fuel
        # m_fuel * (mr + 1) = m_prop
        m_fuel = m_prop / (mr + 1.0)
        m_oxidizer = mr * m_fuel
        
        res.update({
            "oxidizer_mass_kg": m_oxidizer,
            "fuel_mass_kg": m_fuel,
            "engine_name": self.name,
            "propellants": self.propellants
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
