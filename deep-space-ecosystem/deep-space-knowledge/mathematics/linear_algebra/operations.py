"""
Linear Algebra Operations for attitude dynamics and transformations.
"""

import numpy as np

def euler_to_dcm(roll, pitch, yaw):
    """
    Direction Cosine Matrix (DCM) from Euler 3-2-1 rotation sequence.
    Angles in radians.
    """
    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cy, sy = np.cos(yaw), np.sin(yaw)
    
    return np.array([
        [cp*cy, sr*sp*cy - cr*sy, cr*sp*cy + sr*sy],
        [cp*sy, sr*sp*sy + cr*cy, cr*sp*sy - sr*cy],
        [-sp,   sr*cp,            cr*cp]
    ])

def quaternion_to_dcm(q):
    """
    Quaternion [w, x, y, z] to Direction Cosine Matrix (DCM).
    """
    w, x, y, z = q
    return np.array([
        [1.0 - 2.0*(y**2 + z**2), 2.0*(x*y - w*z), 2.0*(x*z + w*y)],
        [2.0*(x*y + w*z), 1.0 - 2.0*(x**2 + z**2), 2.0*(y*z - w*x)],
        [2.0*(x*z - w*y), 2.0*(y*z + w*x), 1.0 - 2.0*(x**2 + y**2)]
    ])

def dcm_to_quaternion(dcm):
    """
    Direction Cosine Matrix (DCM) to Quaternion [w, x, y, z].
    Uses Shepperd's algorithm.
    """
    tr = np.trace(dcm)
    if tr > 0.0:
        s = np.sqrt(tr + 1.0) * 2.0
        w = 0.25 * s
        x = (dcm[2, 1] - dcm[1, 2]) / s
        y = (dcm[0, 2] - dcm[2, 0]) / s
        z = (dcm[1, 0] - dcm[0, 1]) / s
    else:
        # Diagonal elements check
        diags = [dcm[0, 0], dcm[1, 1], dcm[2, 2]]
        max_idx = np.argmax(diags)
        if max_idx == 0:
            s = np.sqrt(1.0 + dcm[0, 0] - dcm[1, 1] - dcm[2, 2]) * 2.0
            w = (dcm[2, 1] - dcm[1, 2]) / s
            x = 0.25 * s
            y = (dcm[0, 1] + dcm[1, 0]) / s
            z = (dcm[0, 2] + dcm[2, 0]) / s
        elif max_idx == 1:
            s = np.sqrt(1.0 + dcm[1, 1] - dcm[0, 0] - dcm[2, 2]) * 2.0
            w = (dcm[0, 2] - dcm[2, 0]) / s
            x = (dcm[0, 1] + dcm[1, 0]) / s
            y = 0.25 * s
            z = (dcm[1, 2] + dcm[2, 1]) / s
        else:
            s = np.sqrt(1.0 + dcm[2, 2] - dcm[0, 0] - dcm[1, 1]) * 2.0
            w = (dcm[1, 0] - dcm[0, 1]) / s
            x = (dcm[0, 2] + dcm[2, 0]) / s
            y = (dcm[1, 2] + dcm[2, 1]) / s
            z = 0.25 * s
    q = np.array([w, x, y, z])
    return q / np.linalg.norm(q)
