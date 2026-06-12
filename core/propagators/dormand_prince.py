"""
Backward-compatible wrapper for Dormand-Prince propagator.
Redirects to simulation.engines.dormand_prince.
"""
from simulation.engines.dormand_prince import dormand_prince_step, dormand_prince_propagate

__all__ = ["dormand_prince_step", "dormand_prince_propagate"]
