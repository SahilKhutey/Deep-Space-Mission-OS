"""
Rocket Propulsion Fuel Models
Implements Tsiolkovsky Rocket Equation and multi-stage mass budget scaling.
"""

import numpy as np
from core.constants import G0


def delta_v(Isp, m0, mf):
    """
    Tsiolkovsky rocket equation:
    ΔV = Isp * g0 * ln(m0 / mf)
    """
    if m0 <= 0 or mf <= 0:
        raise ValueError("Masses must be positive.")
    if m0 < mf:
        raise ValueError("Initial mass m0 must be greater than or equal to final mass mf.")
    return Isp * G0 * np.log(m0 / mf)


def propellant_mass(Isp, m0, target_dv):
    """
    Compute required propellant mass for a target delta-V.
    
    m_prop = m0 * (1 - e^(-ΔV / (Isp * g0)))
    """
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


def build_delta_v_budget(Isp, m0, m_payload, segments):
    """
    Build a detailed multi-burn delta-V budget.
    Propellant is consumed sequentially.
    
    segments: list of dicts with 'name' and 'dv' (m/s)
    """
    current_mass = m0
    budget_segments = []
    
    for seg in segments:
        dv_val = seg["dv"]
        # Propellant burned in this segment
        fuel = propellant_mass(Isp, current_mass, dv_val)
        m_prop = fuel["fuel_mass"]
        mass_start = current_mass
        mass_end = current_mass - m_prop
        
        budget_segments.append({
            "name": seg["name"],
            "delta_v_m_s": dv_val,
            "mass_start_kg": mass_start,
            "mass_end_kg": mass_end,
            "propellant_consumed_kg": m_prop
        })
        current_mass = mass_end
        
    total_dv = sum(s["dv"] for s in segments)
    total_fuel_mass = m0 - current_mass
    
    # Check if we run out of mass (i.e. final mass is less than payload mass)
    margin = current_mass - m_payload
    feasible = margin >= 0.0

    return {
        "initial_mass_kg": m0,
        "final_mass_kg": current_mass,
        "total_fuel_mass_kg": total_fuel_mass,
        "propellant_fraction": total_fuel_mass / m0,
        "payload_mass_kg": m_payload,
        "payload_margin_kg": margin,
        "feasible": feasible,
        "segments": budget_segments,
        "total_delta_v_m_s": total_dv,
        "total_delta_v_km_s": total_dv / 1000.0
    }


def multistage_sizing(payload_mass, total_dv, Isp_stages, structural_fractions):
    """
    Sizing calculation for a multi-stage rocket vehicle.
    Assumes serial staging, calculating required mass for each stage.
    
    Parameters
    ----------
    payload_mass         : float - Mass of final payload (kg)
    total_dv             : float - Total delta-V budget (m/s)
    Isp_stages           : list  - Isp of each stage (seconds) [Stage 1, Stage 2, ...]
    structural_fractions : list  - Structural mass coefficient epsilon of each stage [Stage 1, Stage 2, ...]
    
    Returns
    -------
    dict with mass distribution for each stage.
    """
    n_stages = len(Isp_stages)
    if n_stages != len(structural_fractions):
        raise ValueError("Isp and structural fractions lists must have the same length.")
        
    # Assume equal delta-v distribution across stages for initial sizing
    dv_per_stage = total_dv / n_stages
    
    stage_masses = []
    current_payload = payload_mass
    
    # Calculate starting from top stage to bottom stage (backwards)
    for idx in reversed(range(n_stages)):
        Isp = Isp_stages[idx]
        epsilon = structural_fractions[idx]
        
        # Rocket stage sizing equations:
        # R = exp(dv / (Isp * g0))
        # m_stage = m_payload * (R - 1) * (1 - epsilon) / (1 - epsilon * R)
        # Structural mass m_s = epsilon * m_stage
        # Propellant mass m_p = m_stage - m_s - payload
        R = np.exp(dv_per_stage / (Isp * G0))
        
        denom = 1.0 - epsilon * R
        if denom <= 0:
            raise ValueError(f"Stage {idx+1} is mathematically impossible to size with given structural fraction and delta-V.")
            
        m_stage_total = current_payload * (R - 1.0) * (1.0 - epsilon) / denom
        m_structural = epsilon * m_stage_total
        m_propellant = m_stage_total - m_structural
        
        stage_masses.append({
            "stage": idx + 1,
            "total_stage_mass_kg": m_stage_total,
            "structural_mass_kg": m_structural,
            "propellant_mass_kg": m_propellant,
            "payload_carried_kg": current_payload
        })
        
        # The payload carried by the next lower stage is the entire upper stage assembly
        current_payload = current_payload + m_stage_total

    # Reverse back to list from Stage 1 to N
    stage_masses.reverse()
    
    return {
        "total_vehicle_lift_off_mass_kg": current_payload,
        "payload_mass_kg": payload_mass,
        "stages": stage_masses
    }
