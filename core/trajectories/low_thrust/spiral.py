"""
Low-Thrust Spiral Trajectory calculations
Averaged analytical model for continuous-thrust transfers between circular orbits.
"""

import numpy as np
from core.constants import MU_SUN, G0

def low_thrust_spiral(r1, r2, thrust_N, Isp_s, m0_kg, mu=MU_SUN):
    """
    Estimates time and propellant requirements for a continuous low-thrust spiral.
    
    Parameters
    ----------
    r1       : float - Radius of departure circular orbit (km)
    r2       : float - Radius of arrival circular orbit (km)
    thrust_N : float - Thruster thrust (Newtons)
    Isp_s    : float - Thruster specific impulse (seconds)
    m0_kg    : float - Spacecraft initial wet mass (kg)
    mu       : float - Central body gravitational parameter (km^3/s^2)
    
    Returns
    -------
    dict with:
        delta_v_km_s    : Equivalent delta-v (km/s)
        propellant_kg   : Consumed propellant mass (kg)
        burn_time_s     : Total engine burn time (seconds)
        burn_time_days  : Total engine burn time (days)
        final_mass_kg   : Final spacecraft dry mass (kg)
    """
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbital radii must be positive.")
    if thrust_N <= 0 or Isp_s <= 0 or m0_kg <= 0:
        raise ValueError("Thrust, specific impulse, and initial mass must be positive.")
        
    # Velocities in circular orbits (km/s)
    v1 = np.sqrt(mu / r1)
    v2 = np.sqrt(mu / r2)
    
    # Delta-v is the difference in circular orbital velocities (km/s)
    delta_v = abs(v2 - v1)
    delta_v_m_s = delta_v * 1000.0  # km/s to m/s
    
    # Mass ratio from Tsiolkovsky equation
    ve = Isp_s * G0  # Effective exhaust velocity (m/s)
    mass_ratio = np.exp(delta_v_m_s / ve)
    
    # Propellant mass consumed
    m_prop = m0_kg * (1.0 - 1.0 / mass_ratio)
    m_final = m0_kg - m_prop
    
    # Propellant mass flow rate (kg/s)
    m_dot = thrust_N / ve
    
    # Burn duration
    t_burn = m_prop / m_dot
    
    return {
        "delta_v_km_s": delta_v,
        "propellant_kg": m_prop,
        "burn_time_s": t_burn,
        "burn_time_days": t_burn / 86400.0,
        "final_mass_kg": m_final
    }
