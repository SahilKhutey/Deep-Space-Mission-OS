"""
State-space models and system properties (controllability, observability).
"""

import numpy as np

def is_controllable(A, B):
    """
    Checks controllability of system dx/dt = A*x + B*u.
    System is controllable if controllability matrix C = [B, AB, A²B, ..., Aⁿ⁻¹B] has full rank n.
    """
    n = A.shape[0]
    cols = [B]
    current = B
    for _ in range(1, n):
        current = A @ current
        cols.append(current)
    controllability_matrix = np.hstack(cols)
    return np.linalg.matrix_rank(controllability_matrix) == n

def is_observable(A, C):
    """
    Checks observability of system:
    dx/dt = A*x, y = C*x.
    System is observable if observability matrix O = [C; CA; CA²; ...; CAⁿ⁻¹] has full rank n.
    """
    n = A.shape[0]
    rows = [C]
    current = C
    for _ in range(1, n):
        current = current @ A
        rows.append(current)
    observability_matrix = np.vstack(rows)
    return np.linalg.matrix_rank(observability_matrix) == n
