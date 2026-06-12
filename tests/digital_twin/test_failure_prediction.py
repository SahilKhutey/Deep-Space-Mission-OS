"""
Failure Twin validation.
"""

import pytest
from deep_space_digital_twin.failure import FailureTwin, calculate_metrics

@pytest.mark.digital_twin
class TestFailurePrediction:

    def test_failure_detection(self):
        twin = FailureTwin()
        
        t_nominal = twin.get_telemetry()
        det_nominal = twin.detect_faults(t_nominal)
        assert not any(det_nominal.values())

        twin.inject_fault("battery_failure", True)
        t_faulty = twin.get_telemetry()
        det_faulty = twin.detect_faults(t_faulty)
        assert det_faulty["battery_failure"] is True
        assert not det_faulty["thruster_failure"]

    def test_detection_metrics(self):
        y_true = [True, False, True, True, False]
        y_pred = [True, False, True, False, False]
        metrics = calculate_metrics(y_true, y_pred)
        
        assert metrics["precision"] == 1.0
        assert abs(metrics["recall"] - 0.667) < 0.01
        assert abs(metrics["f1_score"] - 0.8) < 0.01
