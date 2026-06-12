"""
Loss functions: Mean Squared Error (MSE) and Cross Entropy.
"""

import numpy as np

def mean_squared_error(predictions, targets):
    """Mean Squared Error (MSE) loss: 1/N * sum((y_pred - y_true)^2)."""
    predictions = np.array(predictions)
    targets = np.array(targets)
    return np.mean((predictions - targets)**2)

def cross_entropy_loss(predictions, targets, epsilon=1e-15):
    """Cross-Entropy loss for classification models."""
    predictions = np.clip(predictions, epsilon, 1.0 - epsilon)
    targets = np.array(targets)
    return -np.mean(targets * np.log(predictions) + (1.0 - targets) * np.log(1.0 - predictions))
