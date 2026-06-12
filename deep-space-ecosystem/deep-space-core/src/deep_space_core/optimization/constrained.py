from scipy.optimize import minimize


def solve_constrained(f, x0, constraints=None, bounds=None):
    """Solve constrained optimization problem."""
    return minimize(f, x0, constraints=constraints, bounds=bounds)
