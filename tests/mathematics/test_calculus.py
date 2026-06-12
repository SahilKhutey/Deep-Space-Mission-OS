"""
Calculus verification — every derivative and integral tested
at multiple points with known analytical answers.
"""

import pytest
import numpy as np
from deep_space_core.mathematics.calculus import (
    numerical_derivative, numerical_gradient, numerical_jacobian,
    numerical_hessian, trapezoidal, simpson
)

@pytest.mark.math
class TestDerivatives:

    @pytest.mark.parametrize("x,expected", [
        (1.0, 2.0), (10.0, 20.0), (100.0, 200.0), (-5.0, -10.0), (0.5, 1.0)
    ])
    def test_d_dx_x_squared(self, x, expected):
        """d/dx(x²) = 2x"""
        d = numerical_derivative(lambda t: t**2, x)
        assert abs(d - expected) < 1e-5

    @pytest.mark.parametrize("x,expected", [
        (0.0, 1.0), (np.pi/2, 0.0), (np.pi, -1.0), (np.pi*1.5, 0.0)
    ])
    def test_d_dx_sin(self, x, expected):
        """d/dx(sin x) = cos x"""
        d = numerical_derivative(np.sin, x)
        assert abs(d - expected) < 1e-5

    def test_d_dx_exp(self):
        """d/dx(e^x) = e^x"""
        for x in [0.0, 1.0, 2.0, 5.0, -1.0]:
            d = numerical_derivative(np.exp, x)
            assert abs(d - np.exp(x)) < 1e-4

    def test_d_dx_log(self):
        """d/dx(ln x) = 1/x"""
        for x in [0.5, 1.0, 2.0, 10.0, 100.0]:
            d = numerical_derivative(np.log, x)
            assert abs(d - 1/x) < 1e-5

@pytest.mark.math
class TestIntegrals:

    def test_integral_sin_0_pi(self):
        """∫₀^π sin(x) dx = 2"""
        result = simpson(np.sin, 0.0, np.pi)
        assert abs(result - 2.0) < 1e-5

    def test_integral_x_squared_0_1(self):
        """∫₀¹ x² dx = 1/3"""
        result = simpson(lambda x: x**2, 0.0, 1.0)
        assert abs(result - 1/3) < 1e-5

    def test_integral_exp(self):
        """∫₀^1 e^x dx = e - 1"""
        result = simpson(np.exp, 0.0, 1.0)
        assert abs(result - (np.e - 1.0)) < 1e-5

    def test_integral_gaussian(self):
        """∫₋∞^∞ e^(-x²) dx = √π"""
        result = simpson(lambda x: np.exp(-x**2), -10.0, 10.0, n=10000)
        assert abs(result - np.sqrt(np.pi)) < 1e-4

@pytest.mark.math
class TestGradients:

    def test_gradient_quadratic(self):
        """∇(x² + y²) = (2x, 2y)"""
        for pt in [(3.0, 4.0), (-1.0, 2.0), (0.0, 0.0)]:
            g = numerical_gradient(lambda v: v[0]**2 + v[1]**2, pt)
            assert abs(g[0] - 2.0*pt[0]) < 1e-4
            assert abs(g[1] - 2.0*pt[1]) < 1e-4

    def test_gradient_rosenbrock(self):
        """∇(100(y-x²)² + (1-x)²)"""
        f = lambda v: 100.0*(v[1] - v[0]**2)**2 + (1.0 - v[0])**2
        g = numerical_gradient(f, [1.0, 1.0])
        assert np.linalg.norm(g) < 1e-3
