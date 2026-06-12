"""
Earth-Mars Heliocentric N-Body Transfer Scenario
Propagates a spacecraft from Earth's orbital position to Mars's orbital position.
"""

import os
import numpy as np
from datetime import datetime
from core.constants import MU_SUN, MU_EARTH, MU_MARS, DAY_S
from core.astrodynamics.ephemeris.analytical import planet_state
from core.trajectories.earth_mars import date_to_jd
from core.astrodynamics.lambert.solver import lambert_solve
from simulation.engines.dormand_prince import dormand_prince_propagate
from simulation.engines.nbody import nbody_dynamics

def run_mars_scenario(launch_date_str="2032-08-15", flight_days=258.0):
    """
    Runs the Earth-Mars transfer simulation scenario using the Dormand-Prince propagator and N-Body dynamics.
    """
    dt_launch = datetime.strptime(launch_date_str, "%Y-%m-%d")
    jd_start = date_to_jd(dt_launch.year, dt_launch.month, dt_launch.day)
    jd_end = jd_start + flight_days
    
    # 1. Get initial Earth state and final Mars state
    r_earth_start, v_earth_start = planet_state("earth", jd_start)
    r_mars_end, v_mars_end = planet_state("mars", jd_end)
    
    # 2. Solve Lambert's problem for departure velocity
    dt_s = flight_days * DAY_S
    v_trans_start, _ = lambert_solve(r_earth_start, r_mars_end, dt_s, MU_SUN, prograde=True)
    
    # 3. Propagate state using Dormand-Prince and N-body dynamics (Sun, Earth, Mars)
    y0 = np.concatenate([r_earth_start, v_trans_start])
    
    # We include earth and mars as active perturbing bodies
    bodies_list = ["earth", "mars"]
    
    # The ODE system function signature for dormand_prince_propagate is func(t, y, *args)
    # nbody_dynamics expects: nbody_dynamics(t, state, jd_start, bodies_list)
    t_hist, y_hist = dormand_prince_propagate(
        nbody_dynamics, 0.0, dt_s, y0, 1e-8, 1e-8, 3600.0, jd_start, bodies_list
    )
    
    # 4. Generate planet trajectories for background reference
    time_steps = np.linspace(0.0, dt_s, 200)
    earth_traj = []
    mars_traj = []
    
    for ts in time_steps:
        jd_curr = jd_start + (ts / DAY_S)
        rE, _ = planet_state("earth", jd_curr)
        rM, _ = planet_state("mars", jd_curr)
        earth_traj.append(rE)
        mars_traj.append(rM)
        
    return {
        "t": t_hist.tolist(),
        "sc_position": y_hist[:, :3].tolist(),
        "sc_velocity": y_hist[:, 3:].tolist(),
        "earth_position": earth_traj,
        "mars_position": mars_traj,
        "departure_jd": jd_start,
        "arrival_jd": jd_end
    }

if __name__ == "__main__":
    print("Running Earth-Mars transfer simulation...")
    res = run_mars_scenario()
    print(f"Simulation completed. Final position offset from Mars: {np.linalg.norm(np.array(res['sc_position'][-1]) - res['mars_position'][-1]):.2f} km")
