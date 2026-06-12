import numpy as np


def check_trajectory_continuity(r1, r2, tol=1e-3):
    return np.linalg.norm(r1 - r2) < tol * 1e6


def check_energy_conservation(r_vec, v_vec, mu, tol=1e-6):
    r = np.linalg.norm(r_vec); v = np.linalg.norm(v_vec)
    energy = 0.5*v**2 - mu/r
    return -mu/(2.0*energy) > 0 if energy < 0 else False


def check_mass_monotonicity(mass_sequence):
    return all(mass_sequence[i] >= mass_sequence[i+1] for i in range(len(mass_sequence)-1))


def check_orbital_elements(a, e):
    return a > 0 and 0.0 <= e < 1.0


def check_fuel_mass(fuel_mass, dry_mass):
    return fuel_mass >= 0.0 and fuel_mass < fuel_mass + dry_mass


def check_feasibility(mission):
    if mission.get("spacecraft_mass", 0.0) <= mission.get("payload_mass", 0.0):
        return False, "SC mass <= payload"
    return True, "OK"
