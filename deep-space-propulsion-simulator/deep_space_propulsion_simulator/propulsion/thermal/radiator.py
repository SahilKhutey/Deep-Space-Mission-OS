"""
Spacecraft thermal radiator models.
"""

import numpy as np

# Stefan-Boltzmann constant in W/(m^2 K^4)
SIGMA = 5.670374419e-8

class ThermalRadiator:
    def __init__(self, area, emissivity):
        self.area = area
        self.emissivity = emissivity
        
    def steady_state_temp(self, Q_in):
        """
        Computes the steady-state temperature (K) of the radiator for a given heat input Q_in (W).
        Q_in = sigma * emissivity * area * T^4
        T = (Q_in / (sigma * emissivity * area))^(1/4)
        """
        if Q_in < 0:
            raise ValueError("Heat input must be non-negative.")
        denom = SIGMA * self.emissivity * self.area
        if denom == 0:
            return float('inf')
        return (Q_in / denom) ** 0.25
        
    def heat_rejected(self, T):
        """
        Computes heat rejected (W) at temperature T (K).
        Q = sigma * emissivity * area * T^4
        """
        return SIGMA * self.emissivity * self.area * (T ** 4)
