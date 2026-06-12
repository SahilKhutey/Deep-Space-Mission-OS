"""
Matrix decomposition methods: SVD, QR, Cholesky, and Eigendecomposition.
"""

import numpy as np

def eigendecomposition(A):
    """
    Computes eigenvalues and eigenvectors of matrix A.
    Returns: (eigenvalues, eigenvectors)
    """
    return np.linalg.eig(A)

def singular_value_decomposition(A):
    """
    Computes the Singular Value Decomposition (SVD) of A:
    A = U * S * Vt
    Returns: (U, S, Vt)
    """
    return np.linalg.svd(A)

def qr_decomposition(A):
    """
    Computes the QR decomposition of A:
    A = Q * R
    Returns: (Q, R)
    """
    return np.linalg.qr(A)

def cholesky_decomposition(A):
    """
    Computes the Cholesky decomposition of symmetric positive-definite matrix A:
    A = L * Lᵀ
    Returns: Lower triangular matrix L.
    """
    return np.linalg.cholesky(A)
