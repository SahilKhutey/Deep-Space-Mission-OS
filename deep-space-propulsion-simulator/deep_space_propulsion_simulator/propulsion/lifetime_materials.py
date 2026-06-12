"""
Materials databases, thruster wear lifetime models, and vacuum testing chamber simulators.
"""

import numpy as np

MATERIALS = {
    "Rhenium": {
        "Tm_k": 3186.0,
        "density_kg_m3": 21020.0,
        "use": "Ion thruster grids"
    },
    "Carbon-Carbon": {
        "Tm_k": 2500.0,
        "density_kg_m3": 1800.0,
        "use": "Nozzle throats"
    },
    "Inconel 718": {
        "Tm_k": 1330.0,
        "density_kg_m3": 8190.0,
        "use": "Combustion chambers"
    },
    "Tungsten": {
        "Tm_k": 3422.0,
        "density_kg_m3": 19300.0,
        "use": "Cathodes"
    }
}

class ThrusterLifetimeModel:
    def erosion_rate(self, ion_energy_eV, current_density_a_m2, sputter_yield_coeff=1.2):
        """
        Estimates the ion grid erosion rate in micrometers per hour.
        Erosion = J * Y * M / (e * rho)
        """
        # Simplistic empirical wear model
        if ion_energy_eV < 50.0:
            # Below sputtering threshold
            return 0.0
        return float(current_density_a_m2 * (ion_energy_eV - 50.0) * sputter_yield_coeff * 1e-4)

class VacuumChamberModel:
    def simulate_chamber(self, p_init_torr, leak_rate_torr_l_s, pump_speed_l_s, volume_l, duration_s, dt=0.1):
        """
        Simulates the vacuum chamber pressure curve during testing.
        dp/dt = (leak_rate - pump_speed * p) / volume
        """
        t = 0.0
        p = p_init_torr
        pressure_log = [(t, p)]
        
        while t < duration_s:
            dp = ((leak_rate_torr_l_s - pump_speed_l_s * p) / volume_l) * dt
            p += dp
            p = max(p, 1e-9)  # limit to absolute vacuum limit
            t += dt
            pressure_log.append((t, p))
            
        return pressure_log
