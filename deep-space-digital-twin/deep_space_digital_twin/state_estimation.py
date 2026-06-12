"""
Extended Kalman Filter (EKF) for spacecraft state estimation.
"""

import numpy as np

class ExtendedKalmanFilter:
    def __init__(self, x_dim, z_dim):
        self.x = np.zeros(x_dim)  # state vector
        self.P = np.eye(x_dim)    # covariance matrix
        self.Q = np.eye(x_dim)    # process noise covariance
        self.R = np.eye(z_dim)    # measurement noise covariance

    def step(self, f_func, F_jac, h_func, H_jac, z):
        """
        Runs one prediction-update step of the EKF.
        f_func: non-linear transition function f(x)
        F_jac: Jacobian matrix of f at self.x
        h_func: non-linear measurement function h(x)
        H_jac: Jacobian matrix of h at predicted x
        z: measurement vector
        """
        # 1. Predict
        x_pred = f_func(self.x)
        F = F_jac(self.x)
        self.P = F.dot(self.P).dot(F.T) + self.Q
        
        # 2. Update
        H = H_jac(x_pred)
        y = np.array(z) - h_func(x_pred)
        S = H.dot(self.P).dot(H.T) + self.R
        K = self.P.dot(H.T).dot(np.linalg.inv(S))
        
        self.x = x_pred + K.dot(y)
        I = np.eye(len(self.x))
        self.P = (I - K.dot(H)).dot(self.P)
        
        return self.x.copy(), self.P.copy()
