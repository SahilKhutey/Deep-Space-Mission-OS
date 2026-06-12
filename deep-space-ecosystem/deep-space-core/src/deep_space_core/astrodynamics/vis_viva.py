"""Vis-Viva and orbital energy."""
import numpy as np


def vis_viva(r, a, mu):
    """v = √(μ·(2/r - 1/a))"""
    return np.sqrt(mu * (2.0/r - 1.0/a))


def specific_energy(a, mu):
    """ε = -μ/(2a)"""
    return -mu / (2.0 * a)


def semi_major_axis(energy, mu):
    return -mu / (2.0 * energy)
