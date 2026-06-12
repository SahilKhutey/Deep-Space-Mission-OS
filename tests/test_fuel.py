"""
Unit tests for Fuel and Staging Calculations
"""

import unittest
from core.fuel_models.tsiolkovsky import delta_v, propellant_mass, build_delta_v_budget, multistage_sizing


class TestFuel(unittest.TestCase):

    def test_delta_v(self):
        # Isp = 300, m0 = 1000, mf = 500
        # dv = 300 * 9.80665 * ln(2) = 2039.2 m/s
        dv_calc = delta_v(300.0, 1000.0, 500.0)
        self.assertAlmostEqual(dv_calc, 300.0 * 9.80665 * 0.69314718056, delta=1.0)

    def test_propellant_mass(self):
        fuel = propellant_mass(Isp=320.0, m0=2500.0, target_dv=1200.0)
        # mass ratio = exp(1200 / (320 * 9.80665)) = exp(1200 / 3138.128) = exp(0.38239) = 1.4658
        # propellant fraction = 1 - 1/1.4658 = 0.31778
        # fuel mass = 2500 * 0.31778 = 794.4 kg
        self.assertAlmostEqual(fuel["fuel_mass"], 794.46, delta=1.0)
        self.assertAlmostEqual(fuel["propellant_fraction"], 0.31778, delta=0.01)

    def test_multistage_sizing(self):
        # Size a two-stage rocket
        # payload = 1000 kg, total_dv = 6000 m/s
        # Stage 1: Isp=300, epsilon=0.1
        # Stage 2: Isp=350, epsilon=0.12
        Isp_stages = [300.0, 350.0]
        eps = [0.1, 0.12]
        vehicle = multistage_sizing(payload_mass=1000.0, total_dv=6000.0, Isp_stages=Isp_stages, structural_fractions=eps)
        
        self.assertGreater(vehicle["total_vehicle_lift_off_mass_kg"], 1000.0)
        self.assertEqual(len(vehicle["stages"]), 2)
        # Verify stages carrying payloads
        # Stage 2 carries 1000kg payload
        self.assertEqual(vehicle["stages"][1]["payload_carried_kg"], 1000.0)


if __name__ == "__main__":
    unittest.main()
