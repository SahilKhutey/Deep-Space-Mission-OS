"""
Asteroid Rendezvous Trajectory Scenario
Propagates a spacecraft under Sun, Earth, and Asteroid gravity fields.
"""

import numpy as np
from datetime import datetime
from core.constants import MU_SUN, DAY_S
from core.astrodynamics.ephemeris.analytical import planet_state
from core.trajectories.earth_mars import date_to_jd
from core.trajectories.asteroid import get_asteroid_state
from core.astrodynamics.lambert.solver import lambert_solve
from simulation.engines.dormand_prince import dormand_prince_propagate
from simulation.engines.nbody import nbody_dynamics

def run_asteroid_scenario(asteroid_name="bennu", launch_date_str="2032-08-15", flight_days=350.0):
    """
    Runs the asteroid transfer scenario.
    """
    dt_launch = datetime.strptime(launch_date_str, "%Y-%m-%d")
    jd_start = date_to_jd(dt_launch.year, dt_launch.month, dt_launch.day)
    jd_end = jd_start + flight_days
    
    # Departure Earth state
    r_earth_start, _ = planet_state("earth", jd_start)
    # Arrival asteroid state
    r_ast_end, _ = get_asteroid_state(asteroid_name, jd_end)
    
    # Solve Lambert
    dt_s = flight_days * DAY_S
    v_trans_start, _ = lambert_solve(r_earth_start, r_ast_end, dt_s, MU_SUN, prograde=True)
    
    # State propagation
    y0 = np.concatenate([r_earth_start, v_trans_start])
    
    # Perturbing bodies list includes earth and target asteroid
    bodies_list = ["earth", asteroid_name]
    
    t_hist, y_hist = dormand_prince_propagate(
        nbody_dynamics, 0.0, dt_s, y0, 1e-8, 1e-8, 3600.0, jd_start, bodies_list
    )
    
    # Background orbit traces
    time_steps = np.linspace(0.0, dt_s, 200)
    earth_traj = []
    ast_traj = []
    
    for ts in time_steps:
        jd_curr = jd_start + (ts / DAY_S)
        rE, _ = planet_state("earth", jd_curr)
        rA, _ = get_asteroid_state(asteroid_name, jd_curr)
        earth_traj.append(rE)
        ast_traj.append(rA)
        
    return {
        "t": t_hist.tolist(),
        "sc_position": y_hist[:, :3].tolist(),
        "sc_velocity": y_hist[:, 3:].tolist(),
        "earth_position": earth_traj,
        "asteroid_position": ast_traj,
        "departure_jd": jd_start,
        "arrival_jd": jd_end
    }

if __name__ == "__main__":
    print("Running Bennu asteroid transfer scenario...")
    res = run_asteroid_scenario("bennu")
    print(f"Simulation completed. Final position offset from Bennu: {np.linalg.norm(np.array(res['sc_position'][-1]) - res['asteroid_position'][-1]):.2f} km")
