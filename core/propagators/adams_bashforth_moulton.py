"""
Backward-compatible wrapper for Adams-Bashforth-Moulton propagator.
Redirects to simulation.engines.adams_bashforth_moulton.
"""
from simulation.engines.adams_bashforth_moulton import adams_bashforth_moulton_propagate

__all__ = ["adams_bashforth_moulton_propagate"]
