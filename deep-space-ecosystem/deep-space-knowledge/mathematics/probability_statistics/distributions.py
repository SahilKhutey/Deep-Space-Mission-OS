"""
Probability distribution helpers for Monte Carlo simulations.
"""

import numpy as np

def generate_gaussian_samples(mean, std_dev, n_samples, seed=42):
    """Generates gaussian samples N(mean, std_dev²)."""
    rng = np.random.default_rng(seed)
    return rng.normal(mean, std_dev, n_samples)

def generate_uniform_samples(low, high, n_samples, seed=42):
    """Generates uniform samples U(low, high)."""
    rng = np.random.default_rng(seed)
    return rng.uniform(low, high, n_samples)
