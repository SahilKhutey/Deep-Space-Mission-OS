"""Gauss-Jackson 8th-order multi-step integrator.
Berry & Healy (JPL) formulation — production placeholder."""
import numpy as np


def gauss_jackson_propagate(f, y0, t0, tf, h, n_startup=8):
    """
    Placeholder production-ready interface.
    Full implementation requires startup with RK4 then coefficients
    from Berry-Healy table.
    """
    from .rk4 import rk4_propagate
    return rk4_propagate(f, y0, t0, tf, h)
