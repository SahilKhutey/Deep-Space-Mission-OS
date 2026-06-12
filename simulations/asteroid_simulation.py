"""
Asteroid Rendezvous Trajectory Simulation
Propagates spacecraft heliocentrically under Sun and planetary gravity to rendezvous with a target asteroid.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from core.constants import MU_SUN, MU_EARTH, DAY_S
from core.trajectories.earth_mars import get_planet_state, date_to_jd
from core.trajectories.asteroid import get_asteroid_state
from core.astrodynamics.lambert import lambert_solve
from core.propagators.dormand_prince import dormand_prince_propagate


def asteroid_n_body_dynamics(t, state, jd_start, asteroid_name):
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
        
    # 2. Acceleration from Earth (softened using Earth's radius to prevent departure singularity)
    try:
        r_earth, _ = get_planet_state("earth", jd_current)
        r_sc_earth = r_sc - r_earth
        r_sc_earth_norm = np.linalg.norm(r_sc_earth)
        a_earth = -MU_EARTH * r_sc_earth / (r_sc_earth_norm**2 + 6378.137**2)**1.5
    except Exception:
        a_earth = np.zeros(3)
        
    # 3. Acceleration from Asteroid (mass is negligible heliocentrically, softened using 10km radius)
    try:
        r_ast, _ = get_asteroid_state(asteroid_name, jd_current)
        r_sc_ast = r_sc - r_ast
        r_sc_ast_norm = np.linalg.norm(r_sc_ast)
        
        mu_ast = 4.89e-9 if asteroid_name.lower() == "bennu" else 2.5e-5
        a_ast = -mu_ast * r_sc_ast / (r_sc_ast_norm**2 + 10.0**2)**1.5
    except Exception:
        a_ast = np.zeros(3)
        
    a_total = a_sun + a_earth + a_ast
    return np.concatenate([v_sc, a_total])


def run_asteroid_simulation(asteroid_name="bennu", launch_date_str="2032-08-15", flight_days=350.0):
    """
    Run heliocentric asteroid transfer simulation.
    """
    dt_launch = datetime.strptime(launch_date_str, "%Y-%m-%d")
    jd_start = date_to_jd(dt_launch.year, dt_launch.month, dt_launch.day)
    jd_end = jd_start + flight_days
    
    # Earth at departure
    r_earth_start, v_earth_start = get_planet_state("earth", jd_start)
    # Asteroid at arrival
    r_ast_end, v_ast_end = get_asteroid_state(asteroid_name, jd_end)
    
    # Solve Lambert
    dt_s = flight_days * DAY_S
    v_trans_start, _ = lambert_solve(r_earth_start, r_ast_end, dt_s, MU_SUN, prograde=True)
    
    y0 = np.concatenate([r_earth_start, v_trans_start])
    
    t_hist, y_hist = dormand_prince_propagate(
        asteroid_n_body_dynamics, 0.0, dt_s, y0, 1e-8, 1e-8, 3600.0, jd_start, asteroid_name
    )
    
    # Generate planet/asteroid orbits over time
    time_steps = np.linspace(0.0, dt_s, 200)
    earth_traj = []
    ast_traj = []
    
    for ts in time_steps:
        jd_curr = jd_start + (ts / DAY_S)
        rE, _ = get_planet_state("earth", jd_curr)
        rA, _ = get_asteroid_state(asteroid_name, jd_curr)
        earth_traj.append(rE)
        ast_traj.append(rA)
        
    earth_traj = np.array(earth_traj)
    ast_traj = np.array(ast_traj)
    
    return {
        "t": t_hist.tolist(),
        "sc_position": y_hist[:, :3].tolist(),
        "sc_velocity": y_hist[:, 3:].tolist(),
        "earth_position": earth_traj.tolist(),
        "asteroid_position": ast_traj.tolist(),
        "departure_jd": jd_start,
        "arrival_jd": jd_end
    }


def plot_asteroid_simulation(sim_data, asteroid_name, save_path=None):
    """Plot heliocentric transfer in 3D."""
    sc_pos = np.array(sim_data["sc_position"])
    earth_pos = np.array(sim_data["earth_position"])
    ast_pos = np.array(sim_data["asteroid_position"])
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot trajectories
    ax.plot(earth_pos[:, 0], earth_pos[:, 1], earth_pos[:, 2], 'b-', label='Earth Orbit', alpha=0.6)
    ax.plot(ast_pos[:, 0], ast_pos[:, 1], ast_pos[:, 2], 'm-', label=f'{asteroid_name.capitalize()} Orbit', alpha=0.6)
    ax.plot(sc_pos[:, 0], sc_pos[:, 1], sc_pos[:, 2], 'g--', label='Spacecraft Trajectory', linewidth=2)
    
    # Plot Sun
    ax.scatter([0], [0], [0], color='yellow', s=200, label='Sun', edgecolors='orange')
    
    # Plot departure and arrival points
    ax.scatter([sc_pos[0, 0]], [sc_pos[0, 1]], [sc_pos[0, 2]], color='blue', s=80, label='Departure (Earth)')
    ax.scatter([sc_pos[-1, 0]], [sc_pos[-1, 1]], [sc_pos[-1, 2]], color='magenta', s=80, label=f'Rendezvous ({asteroid_name.capitalize()})')
    
    scale = 1e6
    ax.set_xlabel('X (million km)')
    ax.set_ylabel('Y (million km)')
    ax.set_zlabel('Z (million km)')
    
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda val, tick: f'{val/scale:.1f}'))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda val, tick: f'{val/scale:.1f}'))
    ax.zaxis.set_major_formatter(plt.FuncFormatter(lambda val, tick: f'{val/scale:.1f}'))
    
    ax.set_title(f'Heliocentric N-Body Transfer to Asteroid {asteroid_name.capitalize()}')
    ax.legend()
    
    ax.view_init(elev=40, azim=45)
    
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close()
    return fig


if __name__ == "__main__":
    name = "bennu"
    data = run_asteroid_simulation(name)
    plot_asteroid_simulation(data, name, f"simulations/outputs/{name}_transfer_3d.png")
    print("Asteroid simulation plot saved successfully.")
