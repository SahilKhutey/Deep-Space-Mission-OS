import numpy as np


def gradient_descent(f, grad_f, x0, lr=0.01, max_iter=1000, tol=1e-6):
    x = np.array(x0, dtype=float)
    for _ in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        x = x - lr * g
    return x


def newton_method(f, grad_f, hess_f, x0, max_iter=100, tol=1e-6):
    x = np.array(x0, dtype=float)
    for _ in range(max_iter):
        g = grad_f(x)
        if np.linalg.norm(g) < tol:
            break
        try:
            x = x - np.linalg.solve(hess_f(x), g)
        except np.linalg.LinAlgError:
            break
    return x
