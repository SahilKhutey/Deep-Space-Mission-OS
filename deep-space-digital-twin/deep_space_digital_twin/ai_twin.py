"""
AI Digital Twin for predictive state forecasting and anomaly detection.
"""

import numpy as np

class AIDigitalTwin:
    def __init__(self):
        self.history = {}

    def log_state(self, param_name, val):
        if param_name not in self.history:
            self.history[param_name] = []
        self.history[param_name].append(val)
        if len(self.history[param_name]) > 50:
            self.history[param_name].pop(0)

    def forecast_state(self, param_name, steps_future):
        """
        Uses a linear trend fit to forecast values into the future.
        """
        if param_name not in self.history or len(self.history[param_name]) < 5:
            return float("nan")
            
        y = np.array(self.history[param_name])
        x = np.arange(len(y))
        
        m, c = np.polyfit(x, y, 1)
        
        future_x = len(y) - 1 + steps_future
        return float(m * future_x + c)

    def predict_anomaly(self, param_name, steps_future, safety_bounds):
        """
        Predicts if a parameter will exceed safety bounds in steps_future.
        safety_bounds: tuple (min_val, max_val)
        """
        val_forecast = self.forecast_state(param_name, steps_future)
        if np.isnan(val_forecast):
            return False, 0.0
            
        lower, upper = safety_bounds
        is_anomaly = val_forecast < lower or val_forecast > upper
        return is_anomaly, val_forecast
