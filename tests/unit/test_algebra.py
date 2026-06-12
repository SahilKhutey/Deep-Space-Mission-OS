"""Unit tests for algebraic operations."""

import pytest
import numpy as np
from deep_space_core.mathematics.algebra import (
    rocket_equation_delta_v, mass_ratio, propellant_mass,
    solve_quadratic, solve_linear_system
)

@pytest.mark.unit
def test_rocket_equation_known():
    """Apollo-LM descent: Isp=311, m0=15000, mf=2000 → ΔV ≈ 6145 m/s"""
    dv = rocket_equation_delta_v(Isp=311, m0=15000, mf=2000)
    assert abs(dv - 6145.4) < 10

@pytest.mark.unit
def test_mass_ratio():
    mr = mass_ratio(Isp=320, dv=3000)
    expected = np.exp(3000 / (320 * 9.80665))
    assert abs(mr - expected) < 1e-10

@pytest.mark.unit
def test_propellant_mass():
    pm = propellant_mass(m0=1000, mass_ratio=2.5)
    assert abs(pm - 600) < 1e-9

@pytest.mark.unit
def test_solve_quadratic():
    x1, x2 = solve_quadratic(1, -5, 6)
    assert {round(x1, 6), round(x2, 6)} == {2.0, 3.0}

@pytest.mark.unit
def test_solve_linear_system():
    A = [[3, 2], [1, 2]]
    b = [7, 5]
    x = solve_linear_system(A, b)
    assert np.allclose(x, [1.0, 2.0])
