"""
Unit tests for Deep Space Propulsion Simulator
"""

import unittest
import numpy as np
from propulsion.chemical import BipropellantEngine
from propulsion.electric import IonThruster
from propulsion.nuclear import NuclearEngine


class TestPropulsion(unittest.TestCase):

    def test_chemical_engine(self):
        engine = BipropellantEngine("RL-10")
        self.assertEqual(engine.Isp, 465.5)
        self.assertEqual(engine.thrust, 1.1e5)
        
        # Test burn calculations
        m0 = 5000.0
        dv = 1000.0
        res = engine.compute_propellant_for_burn(m0, dv)
        self.assertGreater(res["fuel_mass"], 0.0)
        self.assertLess(res["fuel_mass"], m0)
        self.assertAlmostEqual(res["oxidizer_mass_kg"] / res["fuel_mass_kg"], engine.mixture_ratio, places=5)
        
        t_burn = engine.burn_time(m0, dv)
        self.assertGreater(t_burn, 0.0)

    def test_electric_engine(self):
        thruster = IonThruster("NSTAR")
        self.assertEqual(thruster.Isp, 3100.0)
        self.assertEqual(thruster.thrust, 0.092)
        
        # Jet power = 0.5 * thrust * Isp * g0
        # 0.5 * 0.092 * 3100 * 9.80665 = 1398.4 W
        self.assertAlmostEqual(thruster.jet_power(), 1398.428, delta=1.0)
        
        # Efficiency = Jet power / Power = 1398.4 / 2300 = 0.608
        self.assertAlmostEqual(thruster.efficiency(), 0.608, delta=0.01)
        
        # Specific power = Power / Thrust = 2300 / 0.092 = 25000 W/N
        self.assertAlmostEqual(thruster.specific_power(), 25000.0, places=5)
        
        t_burn = thruster.burn_time(5000.0, 500.0)
        self.assertGreater(t_burn, 0.0)

    def test_nuclear_engine(self):
        ntp = NuclearEngine("NERVA")
        self.assertEqual(ntp.type, "NTP")
        self.assertEqual(ntp.Isp, 850.0)
        self.assertEqual(ntp.reactor_mass(), 0.0)
        
        nep = NuclearEngine("NEP-500kW")
        self.assertEqual(nep.type, "NEP")
        self.assertEqual(nep.Isp, 5000.0)
        self.assertEqual(nep.reactor_mass(), 8.0 * 500.0)  # alpha * P_kW = 8 * 500 = 4000 kg
        
        # Thrust for NEP: 2 * eta * P / (Isp * g0)
        # 2 * 0.65 * 500000 / (5000 * 9.80665) = 650000 / 49033.25 = 13.256 N
        self.assertAlmostEqual(nep.thrust, 13.2563, delta=0.01)
        
        res = nep.compute_propellant_for_burn(10000.0, 1000.0)
        self.assertIn("reactor_mass_kg", res)
        self.assertEqual(res["reactor_mass_kg"], 4000.0)


if __name__ == "__main__":
    unittest.main()
