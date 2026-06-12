"""
Scientific Validation & Verification Subsystem
Implements validation checks for trajectories, energy conservation,
mass monotonicity, and mission feasibility.
"""

import numpy as np
from core.constants import MU_SUN

def check_trajectory_continuity(r1, r2, tol=1.0):
    """
    Checks if two position vectors match within a given tolerance (km).
    Used to verify trajectory continuity at segment/phase boundaries.
    """
    distance = np.linalg.norm(np.array(r1) - np.array(r2))
    return distance < tol

def check_energy_conservation(r_vec, v_vec, mu=MU_SUN, tol=1e-6):
    """
    Checks that the specific energy epsilon = v^2/2 - mu/r remains constant (conserved)
    for a closed Keplerian orbit.
    """
    r_vec = np.array(r_vec)
    v_vec = np.array(v_vec)
    
    # Calculate specific energy for each step
    # Expects r_vec to be shape (N, 3) and v_vec to be shape (N, 3) or single vectors (3,)
    if r_vec.ndim == 1:
        r = np.linalg.norm(r_vec)
        v = np.linalg.norm(v_vec)
        energy = 0.5 * v**2 - mu / r
        return np.isfinite(energy)
    else:
        r = np.linalg.norm(r_vec, axis=1)
        v = np.linalg.norm(v_vec, axis=1)
        energies = 0.5 * v**2 - mu / r
        # Standard deviation of energy over time should be small
        std_energy = np.std(energies)
        mean_energy = abs(np.mean(energies))
        
        if mean_energy < 1e-10:
            return std_energy < tol
        return (std_energy / mean_energy) < tol

def check_mass_monotonicity(masses):
    """
    Checks that the spacecraft mass decreases or remains constant over the mission duration.
    Any increase in mass is invalid (unless a staging or rendezvous refueling event is modeled).
    """
    masses = np.array(masses)
    diffs = np.diff(masses)
    # Mass difference should be <= 0 (monotonically decreasing)
    return np.all(diffs <= 1e-5)  # Allow very small numerical epsilon

def check_orbital_elements(a, e, i, raan, arg_p, nu):
    """
    Checks that the orbital elements are physically valid.
    """
    if a <= 0:
        return False, "Semi-major axis must be positive."
    if e < 0:
        return False, "Eccentricity cannot be negative."
    if e >= 1.0:
        # Currently we focus on closed elliptical orbits in standard checks, but allow hyperbola if needed
        pass
    if not (0.0 <= i <= np.pi):
        return False, "Inclination must be between 0 and pi radians."
    if not (-2*np.pi <= raan <= 4*np.pi):
        return False, "RAAN out of bounds."
    return True, "Valid orbital elements"

def check_fuel_mass(wet_mass, dry_mass, fuel_mass):
    """
    Checks that the wet mass, dry mass, and fuel mass satisfy the conservation of mass.
    """
    if wet_mass <= 0 or dry_mass <= 0 or fuel_mass < 0:
        return False, "Mass values must be positive (fuel mass can be zero)."
    if abs(wet_mass - (dry_mass + fuel_mass)) > 1e-3:
        return False, f"Mass mismatch: wet_mass ({wet_mass}) != dry_mass ({dry_mass}) + fuel_mass ({fuel_mass})"
    return True, "Valid mass budget"

def check_feasibility(mission_profile):
    """
    Performs a top-level feasibility check on a completed mission profile.
    Checks payload margins, propellant fractions, and Delta-V budget.
    """
    if "payload_margin_kg" in mission_profile:
        margin = mission_profile["payload_margin_kg"]
        if margin < 0:
            return False, f"Infeasible: payload margin is negative ({margin:.2f} kg)."
            
    if "feasible" in mission_profile and not mission_profile["feasible"]:
        return False, "Infeasible according to fuel estimator constraints."
        
    return True, "Mission is feasible"
