"""
Unit tests for Differential Equations, Probability & Statistics, Optimization,
Dynamical Systems, Control Theory, and Machine Learning Mathematics.
"""

import unittest
import numpy as np

# Imports from mathematical submodules
from differential_equations.ode import two_body_ode, harmonic_oscillator_ode
from differential_equations.pde_intro import heat_equation_1d
from differential_equations.two_body import hill_equations
from probability_statistics.distributions import generate_gaussian_samples, generate_uniform_samples
from probability_statistics.bayesian import bayes_posterior
from optimization.gradient_methods import gradient_descent, newton_optimization
from optimization.constrained import solve_constrained_quadratic
from dynamical_systems.phase_space import find_equilibria
from dynamical_systems.stability import is_stable_equilibrium, lyapunov_candidate
from control_theory.state_space import is_controllable, is_observable
from machine_learning_math.gradient_descent import sgd_update, adam_update
from machine_learning_math.loss_functions import mean_squared_error, cross_entropy_loss

class TestAdvancedDomains(unittest.TestCase):

    def test_differential_equations(self):
        # Test 2-body ODE return shapes
        state = np.array([1e4, 0.0, 0.0, 0.0, 7.0, 0.0])
        deriv = two_body_ode(0.0, state, mu=398600.0)
        self.assertEqual(len(deriv), 6)
        self.assertTrue(np.allclose(deriv[:3], state[3:]))

        # Test harmonic oscillator
        osc_deriv = harmonic_oscillator_ode(0.0, [1.0, 0.0], k_over_m=1.0)
        self.assertTrue(np.allclose(osc_deriv, [0.0, -1.0]))

        # Test 1D heat equation (PDE)
        u_prev = np.array([0.0, 10.0, 0.0])
        u_next = heat_equation_1d(u_prev, alpha=0.1, dx=1.0, dt=1.0)
        # u_next[1] = 10.0 + 0.1 * 1.0 * (0.0 - 20.0 + 0.0) = 8.0
        self.assertAlmostEqual(u_next[1], 8.0)

        # Test Hill equations
        hill_deriv = hill_equations(0.0, [1.0, 0.0, 0.0, 0.0, 1.0, 0.0], n=0.001)
        self.assertEqual(len(hill_deriv), 6)

    def test_probability_statistics(self):
        # Generate samples and check statistics
        samples_gaussian = generate_gaussian_samples(5.0, 2.0, 1000)
        self.assertAlmostEqual(np.mean(samples_gaussian), 5.0, delta=0.2)
        self.assertAlmostEqual(np.std(samples_gaussian), 2.0, delta=0.2)

        samples_uniform = generate_uniform_samples(0.0, 10.0, 1000)
        self.assertTrue(np.all(samples_uniform >= 0.0))
        self.assertTrue(np.all(samples_uniform <= 10.0))
        self.assertAlmostEqual(np.mean(samples_uniform), 5.0, delta=0.3)

        # Test Bayesian posterior
        post = bayes_posterior(prior_a=0.01, likelihood_b_given_a=0.95, likelihood_b_given_not_a=0.05)
        self.assertAlmostEqual(post, 0.1610169, places=6)

    def test_optimization(self):
        # Minimize f(x) = x^2, grad = 2x
        f = lambda x: x[0]**2
        grad_f = lambda x: np.array([2.0 * x[0]])
        x_min, history = gradient_descent(f, grad_f, [5.0], lr=0.1, max_iter=100)
        self.assertLess(np.linalg.norm(x_min), 1e-3)

        # Newton optimization for f(x) = x^2
        hess_f = lambda x: np.array([[2.0]])
        x_min_newton = newton_optimization(f, grad_f, hess_f, [5.0])
        self.assertLess(np.linalg.norm(x_min_newton), 1e-6)

        # Constrained quadratic
        sol = solve_constrained_quadratic()
        self.assertAlmostEqual(sol[0], 0.5, places=4)
        self.assertAlmostEqual(sol[1], 0.5, places=4)

    def test_dynamical_systems(self):
        # dx/dt = sin(x) -> equilibria at k * pi. range [-1, 4] should have roots near 0 and pi (~3.14159)
        eqs = find_equilibria(np.sin, [-1.0, 4.0])
        # We expect two equilibria: one near 0.0, one near pi
        has_near_zero = any(abs(e) < 0.1 for e in eqs)
        has_near_pi = any(abs(e - np.pi) < 0.1 for e in eqs)
        self.assertTrue(has_near_zero)
        self.assertTrue(has_near_pi)

        # Stability of f(x) = -x -> df_dx = -1 (stable)
        df_dx = lambda x: -1.0
        self.assertTrue(is_stable_equilibrium(df_dx, 0.0))
        self.assertEqual(lyapunov_candidate(3.0), 9.0)

    def test_control_theory(self):
        # Controllable system (double integrator)
        A = np.array([[0.0, 1.0],
                      [0.0, 0.0]])
        B = np.array([[0.0],
                      [1.0]])
        self.assertTrue(is_controllable(A, B))

        # Uncontrollable system
        B_un = np.array([[0.0],
                         [0.0]])
        self.assertFalse(is_controllable(A, B_un))

        # Observable system
        C = np.array([[1.0, 0.0]])
        self.assertTrue(is_observable(A, C))

        # Unobservable system
        C_un = np.array([[0.0, 0.0]])
        self.assertFalse(is_observable(A, C_un))

    def test_machine_learning_math(self):
        # Test SGD
        w = np.array([1.0, 2.0])
        dw = np.array([0.1, -0.2])
        w_new = sgd_update(w, dw, 0.5)
        self.assertTrue(np.allclose(w_new, [0.95, 2.1]))

        # Test Adam update
        w = np.array([1.0])
        dw = np.array([0.1])
        m = np.array([0.0])
        v = np.array([0.0])
        w_new, m_new, v_new = adam_update(w, dw, m, v, lr=0.1, t=1)
        self.assertNotEqual(w_new[0], w[0])

        # Test Loss Functions
        mse = mean_squared_error([1.0, 2.0], [1.1, 1.9])
        self.assertAlmostEqual(mse, 0.01)

        ce = cross_entropy_loss([0.9, 0.1], [1.0, 0.0])
        self.assertAlmostEqual(ce, -0.5 * (np.log(0.9) + np.log(0.9)), places=6)

if __name__ == "__main__":
    unittest.main()
