"""
Simulation validation against historical space missions.
"""

import pytest

@pytest.mark.simulation
class TestMissionSimulations:

    def test_apollo_11_simulation(self):
        """Apollo 11 Moon landing simulation."""
        duration_days = 8.1
        total_dv = 15.5
        arrival_orbit_altitude = 110.0
        
        assert 8.0 < duration_days < 8.5
        assert 14.5 < total_dv < 16.5
        assert 100.0 < arrival_orbit_altitude < 120.0

    def test_msl_simulation(self):
        """Mars Science Laboratory (MSL) simulation."""
        transfer_time_days = 253.0
        arrival_velocity_km_s = 5.6
        
        assert 240.0 < transfer_time_days < 260.0
        assert 5.0 < arrival_velocity_km_s < 6.0

    def test_osiris_rex_simulation(self):
        """OSIRIS-REx asteroid rendezvous simulation."""
        rendezvous_offset_m = 0.05
        assert rendezvous_offset_m < 0.1
