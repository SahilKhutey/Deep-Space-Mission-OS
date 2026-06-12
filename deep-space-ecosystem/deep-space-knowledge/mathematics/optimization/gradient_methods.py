"""
Unconstrained optimization: Gradient Descent and Newton-Raphson optimization.
"""

import numpy as np

def gradient_descent(f, grad_f, x0, lr=0.01, max_iter=1000, tol=1e-6):
    """Performs standard gradient descent to minimize f(x)."""
    x = np.array(x0, dtype=float)
    history = [f(x)]
    for _ in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        x = x - lr * g
        history.append(f(x))
    return x, history

def newton_optimization(f, grad_f, hess_f, x0, max_iter=100, tol=1e-6):
    """Newton's optimization method using Hessian information."""
    x = np.array(x0, dtype=float)
    for _ in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        H = hess_f(x)
        try:
            dx = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            break
        x = x - dx
    return x
