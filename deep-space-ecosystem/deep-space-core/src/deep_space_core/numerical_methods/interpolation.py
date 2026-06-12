"""Polynomial and spline interpolation."""
import numpy as np


def linear_interp(x, x_data, y_data):
    return np.interp(x, x_data, y_data)


def lagrange_interp(x, x_data, y_data):
    n = len(x_data); result = 0.0
    for i in range(n):
        term = y_data[i]
        for j in range(n):
            if j != i:
                term *= (x - x_data[j]) / (x_data[i] - x_data[j])
        result += term
    return result


def cubic_spline(x, x_data, y_data):
    n = len(x_data) - 1
    h = np.diff(x_data)
    A = np.zeros((n+1, n+1))
    b = np.zeros(n+1)
    A[0, 0] = A[n, n] = 1.0
    for i in range(1, n):
        A[i, i-1] = h[i-1]
        A[i, i] = 2.0*(h[i-1] + h[i])
        A[i, i+1] = h[i]
        b[i] = 6.0*((y_data[i+1]-y_data[i])/h[i] - (y_data[i]-y_data[i-1])/h[i-1])
    M = np.linalg.solve(A, b)
    idx = np.searchsorted(x_data, x) - 1
    idx = np.clip(idx, 0, n-1)
    dx = x - x_data[idx]
    return (M[idx]/(6.0*h[idx])*dx**3 +
            M[idx+1]/(6.0*h[idx])*(h[idx]-dx)**3 +
            (y_data[idx]/h[idx] - M[idx]*h[idx]/6.0)*(h[idx]-dx) +
            (y_data[idx+1]/h[idx] - M[idx+1]*h[idx]/6.0)*dx)
