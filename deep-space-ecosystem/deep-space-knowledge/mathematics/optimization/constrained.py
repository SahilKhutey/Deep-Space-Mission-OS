"""
Constrained optimization using SciPy constraints (Lagrange multiplier concept).
"""

import numpy as np
from scipy.optimize import minimize

def solve_constrained_quadratic():
    """
    Minimize f(x, y) = x^2 + y^2 subject to equality constraint:
    g(x, y) = x + y - 1 = 0.
    Analytical Solution: x = 0.5, y = 0.5.
    """
    f = lambda v: v[0]**2 + v[1]**2
    g = lambda v: v[0] + v[1] - 1.0
    
    constraints = {'type': 'eq', 'fun': g}
    result = minimize(f, [0.0, 0.0], constraints=constraints)
    return result.x
