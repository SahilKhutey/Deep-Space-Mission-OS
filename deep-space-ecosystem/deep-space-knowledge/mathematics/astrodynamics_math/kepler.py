"""
Kepler's Equation solver and anomalies.
"""

import numpy as np

def solve_kepler_equation(mean_anomaly, eccentricity, tolerance=1e-12, max_iterations=100):
    """
    Solves Kepler's Equation M = E - e*sin(E) for Eccentric Anomaly (E).
    """
    m = np.mod(mean_anomaly, 2.0 * np.pi)
    e = eccentricity
    
    # Initial guess
    if e < 0.8:
        ecc = m
    else:
        ecc = np.pi
        
    for _ in range(max_iterations):
        f = ecc - e * np.sin(ecc) - m
        df = 1.0 - e * np.cos(ecc)
        delta = f / df
        ecc_new = ecc - delta
        if abs(ecc_new - ecc) < tolerance:
            return ecc_new
        ecc = ecc_new
    return ecc

def true_anomaly_from_eccentric(eccentric_anomaly, eccentricity):
    """
    Computes true anomaly (nu) from eccentric anomaly (E).
    """
    e = eccentricity
    E = eccentric_anomaly
    nu = 2.0 * np.arctan2(np.sqrt(1.0 + e) * np.sin(E / 2.0), np.sqrt(1.0 - e) * np.cos(E / 2.0))
    return np.mod(nu, 2.0 * np.pi)
