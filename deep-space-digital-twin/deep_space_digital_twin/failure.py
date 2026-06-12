"""
Failure Injection and Prediction model.
Allows injecting battery, thruster, and sensor faults, and runs detection/diagnostics.
"""

class FailureTwin:
    def __init__(self):
        self.injected_faults = {
            "battery_failure": False,
            "thruster_failure": False,
            "sensor_failure": False
        }

    def inject_fault(self, fault_name, state=True):
        if fault_name in self.injected_faults:
            self.injected_faults[fault_name] = state
        else:
            raise ValueError(f"Unknown fault: {fault_name}")

    def get_telemetry(self):
        battery_voltage = 12.0
        if self.injected_faults["battery_failure"]:
            battery_voltage = 8.5
            
        thruster_pressure = 250.0
        if self.injected_faults["thruster_failure"]:
            thruster_pressure = 20.0
            
        sensor_value = 100.0
        if self.injected_faults["sensor_failure"]:
            sensor_value = 9999.0
            
        return {
            "battery_voltage": battery_voltage,
            "thruster_pressure": thruster_pressure,
            "sensor_value": sensor_value
        }

    def detect_faults(self, telemetry):
        detected = {
            "battery_failure": False,
            "thruster_failure": False,
            "sensor_failure": False
        }
        
        if telemetry["battery_voltage"] < 10.0:
            detected["battery_failure"] = True
            
        if telemetry["thruster_pressure"] < 100.0:
            detected["thruster_failure"] = True
            
        if telemetry["sensor_value"] > 5000.0:
            detected["sensor_failure"] = True
            
        return detected

def calculate_metrics(y_true, y_pred):
    """
    Computes precision, recall, and F1 score.
    y_true and y_pred are lists of booleans.
    """
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for yt, yp in zip(y_true, y_pred):
        if yt and yp:
            tp += 1
        elif not yt and yp:
            fp += 1
        elif yt and not yp:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 1.0
    f1 = 2.0 * precision * recall / (precision + recall) if (precision + recall) > 0 else 1.0
    
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }
