"""
Propellant sizing calculations based on Tsiolkovsky's rocket equation.
"""
import numpy as np
from deep_space_core.constants import G0


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
    """
    current_mass = m0
    budget_segments = []
    
    for seg in segments:
        dv_val = seg["dv"]
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
    """Sizing calculation for a multi-stage rocket vehicle."""
    n_stages = len(Isp_stages)
    if n_stages != len(structural_fractions):
        raise ValueError("Isp and structural fractions lists must have the same length.")
        
    dv_per_stage = total_dv / n_stages
    
    stage_masses = []
    current_payload = payload_mass
    
    for idx in reversed(range(n_stages)):
        Isp = Isp_stages[idx]
        epsilon = structural_fractions[idx]
        
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
        
        current_payload = current_payload + m_stage_total

    stage_masses.reverse()
    
    return {
        "total_vehicle_lift_off_mass_kg": current_payload,
        "payload_mass_kg": payload_mass,
        "stages": stage_masses
    }
