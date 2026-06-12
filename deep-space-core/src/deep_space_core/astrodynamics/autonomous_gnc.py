"""
Autonomous Guidance, Navigation, and Control (GNC) loops.
"""

import numpy as np

class OrbitCorrectionLoop:
    def __init__(self, kp=1e-5, ki=1e-7, kd=1e-6):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_integral = 0.0
        self.last_error = 0.0

    def compute_correction_burn(self, a_target, a_meas, dt):
        """
        Feedback controller computing required delta-V to correct orbital semi-major axis.
        """
        error = a_target - a_meas
        self.error_integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        self.last_error = error
        
        burn = self.kp * error + self.ki * self.error_integral + self.kd * derivative
        return float(burn)

class CollisionAvoidance:
    def compute_avoidance_maneuver(self, satellite_r, satellite_v, debris_r, safety_threshold_m=100.0):
        """
        Computes the delta-V vector (km/s) required to avoid debris if conjunction is detected.
        """
        r_rel = np.array(satellite_r) - np.array(debris_r)
        dist_m = np.linalg.norm(r_rel) * 1000.0
        
        if dist_m >= safety_threshold_m:
            return np.zeros(3)
            
        r_unit = np.array(satellite_r) / np.linalg.norm(satellite_r)
        return r_unit * 0.01
