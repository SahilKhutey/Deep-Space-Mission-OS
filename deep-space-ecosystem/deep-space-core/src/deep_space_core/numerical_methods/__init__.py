"""Numerical methods: root finding, integration, interpolation."""
from .root_finding import newton_raphson, bisection, secant, brent
from .integration import rk4, rk45_step, trapezoidal, simpson
from .interpolation import lagrange_interp, cubic_spline, linear_interp

__all__ = [
    "newton_raphson", "bisection", "secant", "brent",
    "rk4", "rk45_step", "trapezoidal", "simpson",
    "lagrange_interp", "cubic_spline", "linear_interp"
]
