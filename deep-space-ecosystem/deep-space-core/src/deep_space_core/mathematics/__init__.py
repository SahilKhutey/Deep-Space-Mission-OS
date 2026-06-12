"""
Linear algebra, calculus, ODE — pure math.
"""
from .linear_algebra import (
    rotation_matrix_3d, euler_to_dcm, quaternion_to_dcm,
    inertia_tensor, principal_axes, eci_to_ecef
)
from .calculus import (
    numerical_derivative, numerical_gradient, numerical_jacobian,
    numerical_hessian, trapezoidal, simpson
)
from .vector_calculus import (
    gradient_scalar, divergence, curl, laplacian_scalar
)
from .ode_systems import (
    two_body_ode, harmonic_oscillator, pendulum,
    hill_equations, restricted_three_body_ode
)

__all__ = [
    "rotation_matrix_3d", "euler_to_dcm", "quaternion_to_dcm",
    "inertia_tensor", "principal_axes", "eci_to_ecef",
    "numerical_derivative", "numerical_gradient", "numerical_jacobian",
    "numerical_hessian", "trapezoidal", "simpson",
    "gradient_scalar", "divergence", "curl", "laplacian_scalar",
    "two_body_ode", "harmonic_oscillator", "pendulum",
    "hill_equations", "restricted_three_body_ode"
]
