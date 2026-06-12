"""Kepler's equation solvers."""
import numpy as np


def solve_kepler(M, e, tol=1e-12, max_iter=100):
    """Solve M = E - e·sin(E) for eccentric anomaly E."""
    M = np.mod(M, 2.0*np.pi)
    E = M + 0.85 * e * np.sign(np.sin(M))
    for _ in range(max_iter):
        f = E - e*np.sin(E) - M
        fp = 1.0 - e*np.cos(E)
        E_new = E - f/fp
        if np.all(np.abs(E_new - E) < tol):
            return E_new
        E = E_new
    return E


def true_anomaly(E, e):
    return 2.0*np.arctan2(np.sqrt(1.0+e)*np.sin(E/2.0),
                          np.sqrt(1.0-e)*np.cos(E/2.0))


def eccentric_from_true(nu, e):
    return 2.0*np.arctan2(np.sqrt(1.0-e)*np.sin(nu/2.0),
                          np.sqrt(1.0+e)*np.cos(nu/2.0))
