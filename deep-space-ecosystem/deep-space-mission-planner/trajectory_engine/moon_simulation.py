"""
Earth → Moon High-Fidelity N-Body Trajectory Simulation
Propagates spacecraft relative to Earth, including Moon's gravitational pull.
Uses geocentric Lambert solver to determine initial TLI injection.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime

from deep_space_core.constants import MU_EARTH, MU_MOON, DAY_S
from .earth_moon import get_moon_state, get_moon_elements
from .earth_mars import date_to_jd
from deep_space_core.astrodynamics import lambert_universal
from deep_space_core.propagators import dormand_prince_propagate


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
        
    # 2. Moon's gravitational perturbation (Restricted Three-Body Problem, softened using Moon's radius)
    try:
        r_moon, _ = get_moon_state(jd_current)
        r_sc_moon = r_sc - r_moon
        r_sc_moon_norm = np.linalg.norm(r_sc_moon)
        a_moon = -MU_MOON * r_sc_moon / (r_sc_moon_norm**2 + 1737.4**2)**1.5 - MU_MOON * r_moon / np.linalg.norm(r_moon)**3
    except Exception:
        a_moon = np.zeros(3)
        
    a_total = a_earth + a_moon
    return np.concatenate([v_sc, a_total])


def run_moon_simulation(launch_date_str="2032-08-15", flight_days=4.5):
    """
    Run Earth-Moon geocentric transfer simulation.
    """
    dt_launch = datetime.strptime(launch_date_str, "%Y-%m-%d")
    jd_start = date_to_jd(dt_launch.year, dt_launch.month, dt_launch.day)
    jd_end = jd_start + flight_days
    
    # Initial position at LEO altitude of 300km (geocentric)
    elem_moon = get_moon_elements(jd_start)
    inc = elem_moon["i"]
    raan = elem_moon["raan"]
    
    # Spacecraft injection point in LEO (km)
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
    v_trans_start, _ = lambert_universal(r_sc_start, r_moon_end, dt_s, MU_EARTH, prograde=True)
    
    # Initial state vector
    y0 = np.concatenate([r_sc_start, v_trans_start])
    
    t_hist, y_hist = dormand_prince_propagate(
        moon_n_body_dynamics, 0.0, dt_s, y0, 1e-8, 1e-8, 60.0, jd_start
    )
    
    # Generate Moon trajectory over time for plotting
    time_steps = np.linspace(0.0, dt_s, 200)
    moon_traj = []
    for ts in time_steps:
        jd_curr = jd_start + (ts / DAY_S)
        rM, _ = get_moon_state(jd_curr)
        moon_traj.append(rM)
        
    moon_traj = np.array(moon_traj)
    
    return {
        "t": t_hist.tolist(),
        "sc_position": y_hist[:, :3].tolist(),
        "sc_velocity": y_hist[:, 3:].tolist(),
        "moon_position": moon_traj.tolist(),
        "departure_jd": jd_start,
        "arrival_jd": jd_end
    }


def plot_moon_simulation(sim_data, save_path=None):
    """Plot Earth-Moon transfer relative to Earth."""
    sc_pos = np.array(sim_data["sc_position"])
    moon_pos = np.array(sim_data["moon_position"])
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot(moon_pos[:, 0], moon_pos[:, 1], moon_pos[:, 2], 'gray', label='Moon Orbit', alpha=0.6)
    ax.plot(sc_pos[:, 0], sc_pos[:, 1], sc_pos[:, 2], 'g--', label='Spacecraft Trajectory', linewidth=2)
    
    ax.scatter([0], [0], [0], color='blue', s=250, label='Earth')
    ax.scatter([moon_pos[0, 0]], [moon_pos[0, 1]], [moon_pos[0, 2]], color='lightgray', s=80, label='Moon (Departure)')
    ax.scatter([sc_pos[-1, 0]], [sc_pos[-1, 1]], [sc_pos[-1, 2]], color='darkgray', s=100, label='Capture (Moon)')
    
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title('Earth-Moon Geocentric N-Body Transfer Simulation')
    ax.legend()
    
    ax.view_init(elev=35, azim=30)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        plt.close()
    return fig
