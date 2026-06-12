import unittest
import numpy as np
from deep_space_core.numerical_methods import newton_raphson, brent, rk4
from deep_space_core.mathematics import harmonic_oscillator, two_body_ode
from deep_space_core.constants import MU_SUN


class TestNumerical(unittest.TestCase):

    def test_newton(self):
        f = lambda x: x**3 - 2
        fp = lambda x: 3*x**2
        r = newton_raphson(f, fp, 1.5)
        self.assertAlmostEqual(r, 2.0**(1.0/3.0), places=8)

    def test_brent(self):
        f = lambda x: x**3 - 2
        r = brent(f, 1, 2)
        self.assertAlmostEqual(r, 2.0**(1.0/3.0), places=8)

    def test_rk4_oscillator(self):
        f = lambda t, y: harmonic_oscillator(t, y)
        y = np.array([1.0, 0.0])
        for _ in range(int(2.0*np.pi/0.01)):
            y = rk4(f, 0, y, 0.01)
        self.assertAlmostEqual(y[0], 1.0, places=3)

    def test_two_body_energy(self):
        y0 = np.array([1.496e8, 0, 0, 0, np.sqrt(MU_SUN/1.496e8), 0])
        from deep_space_core.propagators import rk4_propagate
        traj = rk4_propagate(two_body_ode, y0, 0, 30*86400, 3600, MU_SUN)
        r0 = np.linalg.norm(traj[0][1][:3])
        rf = np.linalg.norm(traj[-1][1][:3])
        # Simple check for conservation of orbit radius (circular orbit)
        self.assertAlmostEqual(r0, rf, delta=r0 * 0.01)


if __name__ == "__main__":
    unittest.main()
