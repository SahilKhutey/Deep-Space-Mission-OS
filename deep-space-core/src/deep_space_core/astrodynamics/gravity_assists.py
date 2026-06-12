"""
Gravity assist calculations.
"""

import numpy as np

def gravity_assist_delta_v(v_inf_in, v_inf_out, mu, rp):
    """
    Computes velocity change (delta-V) and turning angle in a gravity flyby.
    v_inf_in: incoming hyperbolic excess velocity vector.
    v_inf_out: outgoing hyperbolic excess velocity vector.
    mu: gravitational parameter of the flyby body.
    rp: periapsis radius of flyby.
    """
    v_in = np.array(v_inf_in, dtype=float)
    v_out = np.array(v_inf_out, dtype=float)
    dv_vec = v_out - v_in
    dv = np.linalg.norm(dv_vec)
    
    mag_in = np.linalg.norm(v_in)
    mag_out = np.linalg.norm(v_out)
    
    if mag_in < 1e-12 or mag_out < 1e-12:
        return 0.0, 0.0
        
    dot_val = np.dot(v_in, v_out) / (mag_in * mag_out)
    dot_val = min(max(dot_val, -1.0), 1.0)
    turn = np.arccos(dot_val)
    return dv, turn
