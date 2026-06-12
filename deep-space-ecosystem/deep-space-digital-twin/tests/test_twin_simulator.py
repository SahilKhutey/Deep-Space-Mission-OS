"""
Unit tests for Spacecraft Digital Twin
"""

import unittest
from twin_core.twin import SpacecraftTwin
from deep_space_core.constants import AU


class TestDigitalTwin(unittest.TestCase):

    def test_twin_propagation(self):
        twin = SpacecraftTwin(spacecraft_mass=1500.0, payload_mass=300.0)
        
        # Propagate for 2 days
        telemetry = twin.propagate_state(duration_days=2.0, dt_s=3600.0)
        
        # There should be 48 frames (2 days * 24 hours/day)
        self.assertEqual(len(telemetry), 48)
        
        # Check that essential keys exist in every frame
        first_frame = telemetry[0]
        self.assertIn("battery_soc", first_frame)
        self.assertIn("temperature_C", first_frame)
        self.assertIn("cpu_load", first_frame)
        self.assertIn("attitude_error_deg", first_frame)
        self.assertIn("link_quality", first_frame)
        
        # Confirm SoC decreases or stays valid
        self.assertTrue(0.0 <= telemetry[-1]["battery_soc"] <= 1.0)
        
    def test_anomaly_detection(self):
        twin = SpacecraftTwin()
        
        # Force low solar power by setting spacecraft far away from the Sun (e.g. 30 AU)
        # and run with a high duration so battery drops below 0.15
        telemetry = twin.propagate_state(
            duration_days=5.0,
            dt_s=7200.0,
            trajectory_distance_sun_km=30.0 * AU
        )
        
        anomalies = twin.detect_anomalies(telemetry)
        
        # Since solar power was extremely low, we expect low battery SoC anomalies
        battery_anomalies = [a for a in anomalies if a["code"] == "LOW_BATTERY_SOC"]
        self.assertGreater(len(battery_anomalies), 0)
        
        # Emitted anomaly format checks
        first_anomaly = battery_anomalies[0]
        self.assertEqual(first_anomaly["subsystem"], "Power")
        self.assertEqual(first_anomaly["severity"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()
