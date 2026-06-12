"""
Linear algebra — rotations, transformations, eigenanalysis.
"""
import numpy as np


def rotation_matrix_3d(axis, angle):
    """Rodrigues formula for rotation about arbitrary axis."""
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    K = np.array([
        [0.0, -axis[2], axis[1]],
        [axis[2], 0.0, -axis[0]],
        [-axis[1], axis[0], 0.0]
    ])
    return np.eye(3) + np.sin(angle) * K + (1.0 - np.cos(angle)) * (K @ K)


def euler_to_dcm(roll, pitch, yaw):
    """3-2-1 Euler to DCM."""
    cr, sr = np.cos(roll), np.sin(roll)
    cp, sp = np.cos(pitch), np.sin(pitch)
    cy, sy = np.cos(yaw), np.sin(yaw)
    return np.array([
        [cp*cy, sr*sp*cy - cr*sy, cr*sp*cy + sr*sy],
        [cp*sy, sr*sp*sy + cr*cy, cr*sp*sy - sr*cy],
        [-sp,   sr*cp,            cr*cp]
    ])


def quaternion_to_dcm(q):
    """Quaternion [w,x,y,z] to rotation matrix."""
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)],
        [2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)],
        [2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)]
    ])


def inertia_tensor(masses, positions):
    """Inertia tensor from point masses."""
    I = np.zeros((3, 3))
    for m, r in zip(masses, positions):
        r = np.asarray(r)
        I += m * (np.dot(r, r) * np.eye(3) - np.outer(r, r))
    return I


def principal_axes(I):
    """Eigendecomposition of inertia tensor."""
    eigenvalues, eigenvectors = np.linalg.eigh(I)
    return eigenvalues, eigenvectors


def eci_to_ecef(r_eci, gmst):
    """Rotate ECI to ECEF by Greenwich Mean Sidereal Time."""
    Rz = np.array([
        [np.cos(gmst),  np.sin(gmst), 0],
        [-np.sin(gmst), np.cos(gmst), 0],
        [0,              0,            1]
    ])
    return Rz @ r_eci
