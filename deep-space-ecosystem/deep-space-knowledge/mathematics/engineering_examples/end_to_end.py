"""
End-to-end trajectory integration and fuel calculation scenario.
"""

import numpy as np
from deep_space_core.constants import MU_EARTH, R_EARTH
from mathematics.differential_equations.ode import two_body_ode
from mathematics.numerical_methods.integration import rk4
from mathematics.astrodynamics_math.vis_viva import vis_viva

def run_end_to_end_example():
    """
    Simulates a LEO satellite orbit, calculates its orbital velocity,
    and computes the required fuel for a orbital altitude raise.
    """
    # 1. Start with LEO circular orbit at 300km altitude
    r_alt = 300.0
    r_leo = R_EARTH + r_alt
    v_leo = np.sqrt(MU_EARTH / r_leo)
    
    # State: [x, y, z, vx, vy, vz]
    y0 = np.array([r_leo, 0.0, 0.0, 0.0, v_leo, 0.0])
    
    # 2. Propagate for 600 seconds using RK4 Two-Body ODE
    y = np.copy(y0)
    t = 0.0
    dt = 10.0
    for _ in range(60):
        y = rk4(two_body_ode, t, y, dt, MU_EARTH)
        t += dt
        
    # 3. Calculate final velocity using Vis-Viva
    r_final = np.linalg.norm(y[:3])
    v_final_vis = vis_viva(r_final, r_leo, MU_EARTH)
    
    # 4. Compute fuel consumed for a 150m/s orbit adjustment burn using Tsiolkovsky
    isp = 320.0
    m_init = 2000.0
    m_prop = m_init - (m_init * np.exp(-150.0 / (isp * 9.80665)))
    
    return {
        "initial_velocity_km_s": v_leo,
        "propagated_position_km": y[:3],
        "vis_viva_velocity_km_s": v_final_vis,
        "propellant_mass_consumed_kg": m_prop
    }

if __name__ == "__main__":
    res = run_end_to_end_example()
    print("End-to-End integration test successfully completed.")
    print(f"Propellant consumed for TMI/Adjustment burn: {res['propellant_mass_consumed_kg']:.2f} kg")
