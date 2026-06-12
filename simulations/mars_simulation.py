"""
Earth → Mars High-Fidelity N-Body Trajectory Simulation
Propagates spacecraft under the combined gravitational pull of the Sun, Earth, and Mars.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from core.constants import MU_SUN, MU_EARTH, MU_MARS, DAY_S
from core.trajectories.earth_mars import get_planet_state, date_to_jd
from core.astrodynamics.lambert import lambert_solve
from core.propagators.dormand_prince import dormand_prince_propagate


def mars_n_body_dynamics(t, state, jd_start):
    """
    State: [x, y, z, vx, vy, vz] heliocentric spacecraft state (km, km/s).
    t: elapsed time in seconds since jd_start.
    """
    r_sc = state[:3]
    v_sc = state[3:]
    
    # Current Julian Date
    jd_current = jd_start + (t / DAY_S)
    
    # 1. Acceleration from Sun
    r_sun_norm = np.linalg.norm(r_sc)
    if r_sun_norm < 1e-3:
        a_sun = np.zeros(3)
    else:
        a_sun = -MU_SUN * r_sc / r_sun_norm**3
        
    # 2. Acceleration from Earth (softened using Earth's radius to prevent singularity at departure)
    try:
        r_earth, _ = get_planet_state("earth", jd_current)
        r_sc_earth = r_sc - r_earth
        r_sc_earth_norm = np.linalg.norm(r_sc_earth)
        a_earth = -MU_EARTH * r_sc_earth / (r_sc_earth_norm**2 + 6378.137**2)**1.5
    except Exception:
        a_earth = np.zeros(3)
        
    # 3. Acceleration from Mars (softened using Mars's radius to prevent singularity at arrival)
    try:
        r_mars, _ = get_planet_state("mars", jd_current)
        r_sc_mars = r_sc - r_mars
        r_sc_mars_norm = np.linalg.norm(r_sc_mars)
        a_mars = -MU_MARS * r_sc_mars / (r_sc_mars_norm**2 + 3389.5**2)**1.5
    except Exception:
        a_mars = np.zeros(3)
        
    a_total = a_sun + a_earth + a_mars
    return np.concatenate([v_sc, a_total])


def run_mars_simulation(launch_date_str="2032-08-15", flight_days=258.0):
    """
    Run Earth-Mars heliocentric transfer simulation.
    """
    dt_launch = datetime.strptime(launch_date_str, "%Y-%m-%d")
    jd_start = date_to_jd(dt_launch.year, dt_launch.month, dt_launch.day)
    jd_end = jd_start + flight_days
    
    # Get initial and final planetary positions
    r_earth_start, v_earth_start = get_planet_state("earth", jd_start)
    r_mars_end, v_mars_end = get_planet_state("mars", jd_end)
    
    # Solve Lambert's problem for initial velocity vector
    dt_s = flight_days * DAY_S
    v_trans_start, _ = lambert_solve(r_earth_start, r_mars_end, dt_s, MU_SUN, prograde=True)
    
    # Spacecraft initial state (starts at Earth's center-of-mass, moving at Lambert transfer velocity)
    y0 = np.concatenate([r_earth_start, v_trans_start])
    
    t_hist, y_hist = dormand_prince_propagate(
        mars_n_body_dynamics, 0.0, dt_s, y0, 1e-8, 1e-8, 3600.0, jd_start
    )
    
    # Generate planetary trajectories for plotting
    time_steps = np.linspace(0.0, dt_s, 200)
    earth_traj = []
    mars_traj = []
    
    for ts in time_steps:
        jd_curr = jd_start + (ts / DAY_S)
        rE, _ = get_planet_state("earth", jd_curr)
        rM, _ = get_planet_state("mars", jd_curr)
        earth_traj.append(rE)
        mars_traj.append(rM)
        
    earth_traj = np.array(earth_traj)
    mars_traj = np.array(mars_traj)
    
    # Prepare results
    sc_pos = y_hist[:, :3]
    sc_vel = y_hist[:, 3:]
    
    return {
        "t": t_hist.tolist(),
        "sc_position": sc_pos.tolist(),
        "sc_velocity": sc_vel.tolist(),
        "earth_position": earth_traj.tolist(),
        "mars_position": mars_traj.tolist(),
        "departure_jd": jd_start,
        "arrival_jd": jd_end
    }


def plot_mars_simulation(sim_data, save_path=None):
    """Plot Earth-Mars transfer in 3D."""
    sc_pos = np.array(sim_data["sc_position"])
    earth_pos = np.array(sim_data["earth_position"])
    mars_pos = np.array(sim_data["mars_position"])
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot orbits/trajectories
    ax.plot(earth_pos[:, 0], earth_pos[:, 1], earth_pos[:, 2], 'b-', label='Earth Orbit', alpha=0.6)
    ax.plot(mars_pos[:, 0], mars_pos[:, 1], mars_pos[:, 2], 'r-', label='Mars Orbit', alpha=0.6)
    ax.plot(sc_pos[:, 0], sc_pos[:, 1], sc_pos[:, 2], 'g--', label='Spacecraft Trajectory', linewidth=2)
    
    # Plot Sun
    ax.scatter([0], [0], [0], color='yellow', s=200, label='Sun', edgecolors='orange')
    
    # Plot start and end points
    ax.scatter([sc_pos[0, 0]], [sc_pos[0, 1]], [sc_pos[0, 2]], color='blue', s=80, label='Departure (Earth)')
    ax.scatter([sc_pos[-1, 0]], [sc_pos[-1, 1]], [sc_pos[-1, 2]], color='red', s=80, label='Arrival (Mars)')
    
    # Equal aspect ratio scaling (simplified representation in millions of km)
    scale = 1e6
    ax.set_xlabel('X (million km)')
    ax.set_ylabel('Y (million km)')
    ax.set_zlabel('Z (million km)')
    
    # Set labels scaled by 1e6
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, tick: f'{val/scale:.1f}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, tick: f'{val/scale:.1f}'))
    ax.zaxis.set_major_formatter(plt.FuncFormatter(lambda val, tick: f'{val/scale:.1f}'))
    
    ax.set_title('Earth-Mars Heliocentric N-Body Transfer Simulation')
    ax.legend()
    
    # Adjust views
    ax.view_init(elev=45, azim=45)
    
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close()
    return fig


if __name__ == "__main__":
    data = run_mars_simulation()
    plot_mars_simulation(data, "simulations/outputs/mars_transfer_3d.png")
    print("Mars simulation plot saved successfully.")
