"""Keplerian element conversions."""
import numpy as np


def keplerian_to_cartesian(a, e, i, raan, arg_p, nu, mu):
    """Classical elements → ECI state vector."""
    r = a * (1.0 - e**2) / (1.0 + e*np.cos(nu))
    v_r = np.sqrt(mu/a/(1.0-e**2)) * e * np.sin(nu)
    v_p = np.sqrt(mu/a/(1.0-e**2)) * (1.0 + e*np.cos(nu))
    r_orb = np.array([r*np.cos(nu), r*np.sin(nu), 0.0])
    v_orb = np.array([v_r*np.cos(nu) - v_p*np.sin(nu),
                      v_r*np.sin(nu) + v_p*np.cos(nu), 0.0])
    cos_O, sin_O = np.cos(raan), np.sin(raan)
    cos_w, sin_w = np.cos(arg_p), np.sin(arg_p)
    cos_i, sin_i = np.cos(i), np.sin(i)
    R = np.array([
        [cos_O*cos_w - sin_O*sin_w*cos_i, -cos_O*sin_w - sin_O*cos_w*cos_i, sin_O*sin_i],
        [sin_O*cos_w + cos_O*sin_w*cos_i, -sin_O*sin_w + cos_O*cos_w*cos_i, -cos_O*sin_i],
        [sin_w*sin_i,                      cos_w*sin_i,                       cos_i]
    ])
    return R @ r_orb, R @ v_orb


def cartesian_to_keplerian(r_vec, v_vec, mu):
    """State vector → classical elements."""
    r_vec = np.asarray(r_vec, dtype=float)
    v_vec = np.asarray(v_vec, dtype=float)
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    h = np.cross(r_vec, v_vec)
    h_mag = np.linalg.norm(h)
    i = np.arccos(h[2] / h_mag) if h_mag > 1e-10 else 0.0
    N = np.cross([0.0, 0.0, 1.0], h)
    N_mag = np.linalg.norm(N)
    raan = np.arccos(N[0]/N_mag) if N_mag > 1e-10 else 0.0
    if N_mag > 1e-10 and N[1] < 0:
        raan = 2.0*np.pi - raan
    e_vec = (np.cross(v_vec, h)/mu) - (r_vec/r)
    e = np.linalg.norm(e_vec)
    arg_p = np.arccos(np.dot(N, e_vec)/(N_mag*e)) if e > 1e-10 and N_mag > 1e-10 else 0.0
    if e > 1e-10 and e_vec[2] < 0:
        arg_p = 2.0*np.pi - arg_p
    nu = np.arccos(np.dot(e_vec, r_vec)/(e*r)) if e > 1e-10 else 0.0
    if np.dot(r_vec, v_vec) < 0:
        nu = 2.0*np.pi - nu
    energy = v**2/2.0 - mu/r
    a = -mu / (2.0*energy) if abs(energy) > 1e-12 else np.inf
    return a, e, i, raan, arg_p, nu
