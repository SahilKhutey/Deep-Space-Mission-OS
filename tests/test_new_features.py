"""
Unit tests for new DSMP features:
- Hohmann, Bi-elliptic, Low-Thrust Trajectories
- Bipropellant and Ion Propulsion Sizing
- Class-based GA, PSO, and DE Optimizers
- Scientific Validation Checks
"""

import unittest
import numpy as np
from core.constants import MU_EARTH, MU_SUN, G0
from core.trajectories.hohmann.transfer import hohmann_transfer
from core.trajectories.bielliptic.transfer import bielliptic_transfer
from core.trajectories.low_thrust.spiral import low_thrust_spiral
from core.propulsion.chemical.bipropellant import BipropellantEngine
from core.propulsion.electric.ion_thruster import IonThruster
from core.optimization.genetic.ga import GeneticAlgorithm
from core.optimization.pso.pso import PSO
from core.optimization.differential_evolution.de import DifferentialEvolution
from core.validation.checks import (
    check_trajectory_continuity,
    check_energy_conservation,
    check_mass_monotonicity,
    check_orbital_elements,
    check_fuel_mass,
    check_feasibility
)

class TestNewFeatures(unittest.TestCase):

    def test_hohmann_transfer(self):
        r1 = 7000.0  # LEO radius (km)
        r2 = 42000.0 # GEO-like radius (km)
        
        res = hohmann_transfer(r1, r2, mu=MU_EARTH)
        
        self.assertGreater(res["total_dv_km_s"], 0)
        self.assertGreater(res["tof_seconds"], 0)
        # Expected total dv for Hohmann between 7000 and 42000 km is around 3.768 km/s
        self.assertAlmostEqual(res["total_dv_km_s"], 3.768029, places=4)

    def test_bielliptic_transfer(self):
        r1 = 7000.0
        r2 = 42000.0
        rb = 100000.0 # intermediate boost radius
        
        res = bielliptic_transfer(r1, r2, rb, mu=MU_EARTH)
        
        self.assertGreater(res["total_dv_km_s"], 0)
        self.assertGreater(res["tof_seconds"], 0)
        self.assertEqual(res["dv1_km_s"] + res["dv2_km_s"] + res["dv3_km_s"], res["total_dv_km_s"])

    def test_low_thrust_spiral(self):
        r1 = 7000.0
        r2 = 42000.0
        thrust = 0.5  # Newtons
        Isp = 3000.0  # seconds
        m0 = 1500.0   # kg
        
        res = low_thrust_spiral(r1, r2, thrust, Isp, m0, mu=MU_EARTH)
        
        self.assertGreater(res["delta_v_km_s"], 0)
        self.assertGreater(res["propellant_kg"], 0)
        self.assertLess(res["final_mass_kg"], m0)

    def test_chemical_propulsion(self):
        engine = BipropellantEngine("RL-10")
        m0 = 5000.0
        dv = 2000.0  # m/s
        
        res = engine.compute_propellant_for_burn(m0, dv)
        m_prop = res["fuel_mass"]
        
        self.assertGreater(m_prop, 0)
        self.assertLess(m_prop, m0)
        self.assertEqual(res["propellants"], "LOX/LH2")
        
        t_burn = engine.burn_time(m0, dv)
        self.assertGreater(t_burn, 0)

    def test_electric_propulsion(self):
        thruster = IonThruster("NSTAR")
        m0 = 1000.0
        dv = 5000.0  # m/s
        
        res = thruster.compute_propellant_for_burn(m0, dv)
        self.assertGreater(res["fuel_mass"], 0)
        self.assertGreater(thruster.specific_power(), 0)
        self.assertGreater(thruster.efficiency(), 0)

    def test_optimizers(self):
        # Optimize simple quadratic function: minimize f(x, y) = (x-2.5)^2 + (y-3.5)^2
        cost_fn = lambda x: (x[0] - 2.5)**2 + (x[1] - 3.5)**2
        bounds = [(0.0, 5.0), (0.0, 5.0)]
        
        # 1. Genetic Algorithm
        ga = GeneticAlgorithm(cost_fn, bounds, pop_size=20, n_gen=30, seed=42)
        best_ga, cost_ga = ga.optimize()
        self.assertAlmostEqual(best_ga[0], 2.5, places=1)
        self.assertAlmostEqual(best_ga[1], 3.5, places=1)
        
        # 2. PSO
        pso = PSO(cost_fn, bounds, n_particles=20, n_iter=30, seed=42)
        best_pso, cost_pso = pso.optimize()
        self.assertAlmostEqual(best_pso[0], 2.5, places=1)
        self.assertAlmostEqual(best_pso[1], 3.5, places=1)
        
        # 3. Differential Evolution
        de = DifferentialEvolution(cost_fn, bounds, pop_size=20, n_gen=30, seed=42)
        best_de, cost_de = de.optimize()
        self.assertAlmostEqual(best_de[0], 2.5, places=1)
        self.assertAlmostEqual(best_de[1], 3.5, places=1)

    def test_validation_checks(self):
        # 1. Trajectory continuity
        self.assertTrue(check_trajectory_continuity([100.0, 0, 0], [100.0, 0.1, 0], tol=0.5))
        is_continuous_false = check_trajectory_continuity([100.0, 0, 0], [105.0, 0, 0], tol=1.0)
        self.assertFalse(is_continuous_false)
        
        # 2. Energy conservation
        # Bound orbit state: pos = [7000.0, 0, 0], vel = [0, 7.5, 0] relative to Earth
        self.assertTrue(check_energy_conservation([7000.0, 0.0, 0.0], [0.0, 7.5, 0.0], mu=MU_EARTH))
        
        # 3. Mass monotonicity
        self.assertTrue(check_mass_monotonicity([1000.0, 950.0, 900.0, 900.0]))
        self.assertFalse(check_mass_monotonicity([1000.0, 950.0, 980.0, 900.0])) # mass increased
        
        # 4. Mass budget
        valid, msg = check_fuel_mass(1000.0, 800.0, 200.0)
        self.assertTrue(valid)
        valid, msg = check_fuel_mass(1000.0, 800.0, 150.0)
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()
