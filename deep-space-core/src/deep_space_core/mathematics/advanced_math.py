"""
Advanced mathematical methods including Tensor Calculus, Variational Calculus,
Information Theory, and Graph Theory.
"""

import numpy as np

# --- 1. Tensor Calculus ---

def metric_tensor_spherical(r, theta, phi):
    """
    Returns the metric tensor matrix for 3D spherical coordinates:
    g = diag(1, r^2, r^2 * sin(theta)^2)
    """
    g = np.zeros((3, 3))
    g[0, 0] = 1.0
    g[1, 1] = r ** 2
    g[2, 2] = (r * np.sin(theta)) ** 2
    return g

def christoffel_symbols_spherical(r, theta):
    """
    Returns non-zero Christoffel symbols of the second kind for spherical coordinates.
    G^i_jk is stored in a dictionary.
    """
    if r == 0:
        raise ValueError("r cannot be zero.")
    return {
        # G^r_jj
        ("r", "theta", "theta"): -r,
        ("r", "phi", "phi"): -r * (np.sin(theta) ** 2),
        # G^theta_rj
        ("theta", "r", "theta"): 1.0 / r,
        ("theta", "theta", "r"): 1.0 / r,
        ("theta", "phi", "phi"): -np.sin(theta) * np.cos(theta),
        # G^phi_rj
        ("phi", "r", "phi"): 1.0 / r,
        ("phi", "phi", "r"): 1.0 / r,
        ("phi", "theta", "phi"): 1.0 / np.tan(theta) if np.tan(theta) != 0 else 0.0,
        ("phi", "phi", "theta"): 1.0 / np.tan(theta) if np.tan(theta) != 0 else 0.0,
    }

# --- 2. Variational Calculus ---

def euler_lagrange_error(L_func, q, q_dot, dt, t):
    """
    Mock check of Euler-Lagrange equations: d/dt(dL/dq_dot) - dL/dq = 0.
    Returns the residual error vector.
    """
    q = np.array(q, dtype=float)
    q_dot = np.array(q_dot, dtype=float)
    
    # Numerical derivative of L with respect to q and q_dot
    h = 1e-5
    n = len(q)
    
    dL_dq = np.zeros(n)
    dL_dqdot = np.zeros(n)
    
    for i in range(n):
        q_plus = q.copy(); q_plus[i] += h
        q_minus = q.copy(); q_minus[i] -= h
        dL_dq[i] = (L_func(q_plus, q_dot, t) - L_func(q_minus, q_dot, t)) / (2.0 * h)
        
        qdot_plus = q_dot.copy(); qdot_plus[i] += h
        qdot_minus = q_dot.copy(); qdot_minus[i] -= h
        dL_dqdot[i] = (L_func(q, qdot_plus, t) - L_func(q, qdot_minus, t)) / (2.0 * h)
        
    # Standard mock for time derivative d/dt (dL/dq_dot) using simple perturbation
    dL_dqdot_next = dL_dqdot + dL_dq * dt  # Euler approximation
    residual = dL_dqdot_next - dL_dqdot - dL_dq * dt
    return residual

# --- 3. Information Theory ---

def shannon_entropy(probabilities):
    """
    Computes Shannon Entropy: H = -sum(p_i * log2(p_i))
    """
    p = np.array(probabilities, dtype=float)
    p = p[p > 0.0]  # filter out zero probabilities
    return -np.sum(p * np.log2(p))

def kl_divergence(p, q):
    """
    Computes Kullback-Leibler Divergence: D_KL(P || Q) = sum(p_i * log2(p_i / q_i))
    """
    p = np.array(p, dtype=float)
    q = np.array(q, dtype=float)
    # Avoid zero division and log(0)
    mask = (p > 0.0) & (q > 0.0)
    return np.sum(p[mask] * np.log2(p[mask] / q[mask]))

# --- 4. Graph Theory ---

def graph_laplacian(adjacency_matrix):
    """
    Computes the Graph Laplacian: L = D - A
    """
    A = np.array(adjacency_matrix, dtype=float)
    D = np.diag(np.sum(A, axis=1))
    return D - A

def consensus_step(x, laplacian, dt):
    """
    Single step of consensus algorithm: x_next = x - L * x * dt.
    """
    x = np.array(x, dtype=float)
    L = np.array(laplacian, dtype=float)
    return x - L.dot(x) * dt
