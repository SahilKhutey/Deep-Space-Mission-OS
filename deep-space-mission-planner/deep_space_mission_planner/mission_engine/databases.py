"""
Launch Vehicle and Payload Databases.
"""

LAUNCH_VEHICLES = {
    "Falcon 9": {
        "leo_kg": 22800.0,
        "gto_kg": 8300.0,
        "tli_kg": 4000.0,
        "cost_usd": 67e6
    },
    "Falcon Heavy": {
        "leo_kg": 63800.0,
        "gto_kg": 26700.0,
        "tli_kg": 15000.0,
        "cost_usd": 97e6
    },
    "Atlas V": {
        "leo_kg": 18850.0,
        "gto_kg": 8900.0,
        "tli_kg": 3500.0,
        "cost_usd": 110e6
    },
    "SLS": {
        "leo_kg": 95000.0,
        "gto_kg": 40000.0,
        "tli_kg": 27000.0,
        "cost_usd": 2e9
    },
    "Vulcan": {
        "leo_kg": 27200.0,
        "gto_kg": 14400.0,
        "tli_kg": 6000.0,
        "cost_usd": 120e6
    },
    "Ariane 6": {
        "leo_kg": 21600.0,
        "gto_kg": 11500.0,
        "tli_kg": 5000.0,
        "cost_usd": 115e6
    }
}

PAYLOAD_DATABASE = {
    "Star Tracker": {
        "mass_kg": 0.3,
        "power_w": 1.5,
        "data_rate_kbps": 10.0
    },
    "IMU": {
        "mass_kg": 0.5,
        "power_w": 5.0,
        "data_rate_kbps": 50.0
    },
    "X-Band Transponder": {
        "mass_kg": 3.5,
        "power_w": 65.0,
        "data_rate_kbps": 1000.0
    },
    "Ka-Band": {
        "mass_kg": 5.0,
        "power_w": 90.0,
        "data_rate_kbps": 10000.0
    }
}
