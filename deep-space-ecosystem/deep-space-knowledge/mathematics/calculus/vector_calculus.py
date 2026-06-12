"""
Vector Calculus Operations — Validated Library
"""

import numpy as np


def gradient(scalar_field, point, h=1e-6):
    """Numerical gradient of a scalar field."""
    x, y, z = point
    dfdx = (scalar_field(x + h, y, z) - scalar_field(x - h, y, z)) / (2*h)
    dfdy = (scalar_field(x, y + h, z) - scalar_field(x, y - h, z)) / (2*h)
    dfdz = (scalar_field(x, y, z + h) - scalar_field(x, y, z - h)) / (2*h)
    return np.array([dfdx, dfdy, dfdz])


def divergence(vector_field, point, h=1e-6):
    """Numerical divergence of a vector field."""
    x, y, z = point
    Fx, Fy, Fz = vector_field
    dFxdx = (Fx(x+h, y, z) - Fx(x-h, y, z)) / (2*h)
    dFydy = (Fy(x, y+h, z) - Fy(x, y-h, z)) / (2*h)
    dFzdz = (Fz(x, y, z+h) - Fz(x, y, z-h)) / (2*h)
    return dFxdx + dFydy + dFzdz


def curl(vector_field, point, h=1e-6):
    """Numerical curl of a vector field."""
    x, y, z = point
    Fx, Fy, Fz = vector_field
    dFz_dy = (Fz(x, y+h, z) - Fz(x, y-h, z)) / (2*h)
    dFy_dz = (Fy(x, y, z+h) - Fy(x, y, z-h)) / (2*h)
    dFx_dz = (Fx(x, y, z+h) - Fx(x, y, z-h)) / (2*h)
    dFz_dx = (Fz(x+h, y, z) - Fz(x-h, y, z)) / (2*h)
    dFy_dx = (Fy(x+h, y, z) - Fy(x-h, y, z)) / (2*h)
    dFx_dy = (Fx(x, y+h, z) - Fx(x, y-h, z)) / (2*h)
    return np.array([dFz_dy - dFy_dz,
                     dFx_dz - dFz_dx,
                     dFy_dx - dFx_dy])


# VALIDATION
if __name__ == "__main__":
    # Test on F = (-y, x, 0) — should give curl = (0, 0, 2)
    Fx = lambda x, y, z: -y
    Fy = lambda x, y, z: x
    Fz = lambda x, y, z: 0
    result = curl((Fx, Fy, Fz), (0, 0, 0))
    expected = np.array([0, 0, 2])
    assert np.allclose(result, expected, atol=1e-4), f"Curl test failed: {result}"
    print("✓ Vector calculus validation passed")
