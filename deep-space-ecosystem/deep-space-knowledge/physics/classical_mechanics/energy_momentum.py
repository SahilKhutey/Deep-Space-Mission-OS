"""
Conservation Laws — Validated Library
"""

import numpy as np
from deep_space_core.constants import MU_SUN


def kinetic_energy(m, v):
    """T = ½mv²"""
    return 0.5 * m * np.dot(v, v)


def potential_energy(m, M, r, G=6.67430e-20):  # G in km^3/(kg·s^2)
    """U = -G·M·m/r"""
    return -G * M * m / r


def specific_energy(r_vec, v_vec, mu):
    """ε = v²/2 − μ/r"""
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    return 0.5 * v**2 - mu / r


def specific_angular_momentum(r_vec, v_vec):
    """h = r × v"""
    return np.cross(r_vec, v_vec)


def semi_major_axis_from_energy(energy, mu):
    """a = -μ/(2ε)"""
    return -mu / (2 * energy)


# VALIDATION
if __name__ == "__main__":
    # Earth at 1 AU: ε should equal -μ/(2·1AU)
    r = np.array([1.496e8, 0, 0])
    v_mag = np.sqrt(MU_SUN / 1.496e8)
    v = np.array([0, v_mag, 0])
    eps = specific_energy(r, v, MU_SUN)
    expected = -MU_SUN / (2 * 1.496e8)
    assert abs(eps - expected) < 1e-3, f"{eps} vs {expected}"
    print(f"✓ Specific energy: ε = {eps:.4e} km²/s²")
    print(f"  Semi-major axis: {semi_major_axis_from_energy(eps, MU_SUN):.4e} km")
