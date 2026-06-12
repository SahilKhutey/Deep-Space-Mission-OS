"""
Telemetry Ingestion, Sensor Noise/Bias Models, and Fault Injection framework.
"""

import numpy as np

class TelemetryIngestor:
    def parse_ccsds_packet(self, binary_packet):
        """
        Parses a mock CCSDS binary packet.
        Format: [16-bit APID][32-bit Time][64-bit Data]
        """
        if len(binary_packet) < 14:
            raise ValueError("Packet length too short for CCSDS header.")
        apid = int.from_bytes(binary_packet[0:2], byteorder="big")
        time_s = int.from_bytes(binary_packet[2:6], byteorder="big")
        value = float(np.frombuffer(binary_packet[6:14], dtype=np.float64)[0])
        return {
            "apid": apid,
            "timestamp": time_s,
            "data_value": value
        }

class SensorModels:
    def __init__(self, rng=None):
        self.rng = rng or np.random.default_rng(42)

    def star_tracker(self, true_q, noise_sigma=1e-4):
        """Adds Gaussian noise to true quaternion."""
        noise = self.rng.normal(0, noise_sigma, 4)
        noisy_q = true_q + noise
        return noisy_q / np.linalg.norm(noisy_q)

    def imu_rate(self, true_rate, bias=0.01, noise_sigma=1e-3):
        """Adds bias and noise to angular rate."""
        noise = self.rng.normal(0, noise_sigma, len(true_rate))
        return np.array(true_rate) + bias + noise

    def gps_position(self, true_pos, noise_sigma=5.0):
        """Adds noise to 3D position."""
        noise = self.rng.normal(0, noise_sigma, 3)
        return np.array(true_pos) + noise

class FaultInjector:
    def __init__(self):
        self.active_faults = {}

    def inject_fault(self, sensor_name, fault_type, param=0.0):
        """
        Injects: 'bias', 'drift', 'spike', 'freeze'.
        """
        self.active_faults[sensor_name] = {"type": fault_type, "param": param, "history": []}

    def clear_faults(self):
        self.active_faults.clear()

    def process(self, sensor_name, t, value):
        if sensor_name not in self.active_faults:
            return value
            
        fault = self.active_faults[sensor_name]
        ftype = fault["type"]
        param = fault["param"]
        
        if ftype == "bias":
            return value + param
        elif ftype == "drift":
            return value + param * t
        elif ftype == "spike":
            if int(t) % 10 == 0:
                return value + param
            return value
        elif ftype == "freeze":
            if not fault["history"]:
                fault["history"].append(value)
            return fault["history"][0]
        return value
