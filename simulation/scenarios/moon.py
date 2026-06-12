"""
Earth-Moon Geocentric N-Body Transfer Scenario
Propagates a spacecraft relative to Earth, including Moon's gravitational pull.
"""

import os
import numpy as np
from datetime import datetime
from core.constants import MU_EARTH, MU_MOON, DAY_S
from core.trajectories.earth_moon import get_moon_state, get_moon_elements
from core.trajectories.earth_mars import date_to_jd
from core.astrodynamics.lambert.solver import lambert_solve
from simulation.engines.dormand_prince import dormand_prince_propagate

def moon_n_body_dynamics(t, state, jd_start):
    """
    State: [x, y, z, vx, vy, vz] geocentric spacecraft state (km, km/s).
    t: elapsed time in seconds since jd_start.
    """
    r_sc = state[:3]
    v_sc = state[3:]
    
    jd_current = jd_start + (t / DAY_S)
    
    # 1. Earth's central gravity (softened using Earth's radius to prevent singularity)
    r_earth_norm = np.linalg.norm(r_sc)
    a_earth = -MU_EARTH * r_sc / (r_earth_norm**2 + 6378.137**2)**1.5
        
    # 2. Moon's gravitational perturbation (softened using Moon's radius)
    try:
        r_moon, _ = get_moon_state(jd_current)
        r_sc_moon = r_sc - r_moon
        r_sc_moon_norm = np.linalg.norm(r_sc_moon)
        
        # Direct attraction of Moon minus indirect acceleration on Earth
        a_moon = -MU_MOON * r_sc_moon / (r_sc_moon_norm**2 + 1737.4**2)**1.5 - MU_MOON * r_moon / np.linalg.norm(r_moon)**3
    except Exception:
        a_moon = np.zeros(3)
        
    a_total = a_earth + a_moon
    return np.concatenate([v_sc, a_total])

def run_moon_scenario(launch_date_str="2032-08-15", flight_days=4.5):
    """
    Runs the Earth-Moon transfer scenario.
    """
    dt_launch = datetime.strptime(launch_date_str, "%Y-%m-%d")
    jd_start = date_to_jd(dt_launch.year, dt_launch.month, dt_launch.day)
    jd_end = jd_start + flight_days
    
    # Initial position at LEO altitude of 300km (geocentric) in lunar orbital plane
    elem_moon = get_moon_elements(jd_start)
    inc = elem_moon["i"]
    raan = elem_moon["raan"]
    
    r_leo_altitude = 6378.137 + 300.0
    r_sc_start = np.array([
        r_leo_altitude * np.cos(raan),
        r_leo_altitude * np.sin(raan) * np.cos(inc),
        r_leo_altitude * np.sin(raan) * np.sin(inc)
    ])
    
    # Get Moon position at arrival
    r_moon_end, v_moon_end = get_moon_state(jd_end)
    
    # Solve Lambert's problem geocentrically
    dt_s = flight_days * DAY_S
    v_trans_start, _ = lambert_solve(r_sc_start, r_moon_end, dt_s, MU_EARTH, prograde=True)
    
    # Initial state
    y0 = np.concatenate([r_sc_start, v_trans_start])
    
    t_hist, y_hist = dormand_prince_propagate(
        moon_n_body_dynamics, 0.0, dt_s, y0, 1e-8, 1e-8, 60.0, jd_start
    )
    
    # Trace Moon orbit
    time_steps = np.linspace(0.0, dt_s, 200)
    moon_traj = []
    for ts in time_steps:
        jd_curr = jd_start + (ts / DAY_S)
        rM, _ = get_moon_state(jd_curr)
        moon_traj.append(rM)
        
    return {
        "t": t_hist.tolist(),
        "sc_position": y_hist[:, :3].tolist(),
        "sc_velocity": y_hist[:, 3:].tolist(),
        "moon_position": moon_traj,
        "departure_jd": jd_start,
        "arrival_jd": jd_end
    }

if __name__ == "__main__":
    print("Running Earth-Moon TLI simulation...")
    res = run_moon_scenario()
    print(f"Simulation completed. Final position offset from Moon: {np.linalg.norm(np.array(res['sc_position'][-1]) - res['moon_position'][-1]):.2f} km")
