"""
Gradient Descent and optimization methods for Machine Learning models.
"""

import numpy as np

def sgd_update(weights, gradients, learning_rate):
    """Standard Stochastic Gradient Descent (SGD) update."""
    return weights - learning_rate * np.array(gradients)

def adam_update(w, dw, m, v, beta1=0.9, beta2=0.999, lr=0.001, epsilon=1e-8, t=1):
    """
    Adam optimization update.
    Returns: updated_weights, updated_m, updated_v
    """
    w = np.array(w)
    dw = np.array(dw)
    m = beta1 * m + (1.0 - beta1) * dw
    v = beta2 * v + (1.0 - beta2) * (dw**2)
    
    # Bias corrections
    m_corrected = m / (1.0 - beta1**t)
    v_corrected = v / (1.0 - beta2**t)
    
    w_new = w - lr * m_corrected / (np.sqrt(v_corrected) + epsilon)
    return w_new, m, v
