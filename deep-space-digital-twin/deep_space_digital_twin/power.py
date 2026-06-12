"""
Power digital twin modeling solar panels and battery charging/discharging.
"""

class PowerTwin:
    def __init__(self, panel_area=10.0, panel_eff=0.30, battery_capacity_wh=1000.0, initial_charge_wh=500.0):
        self.panel_area = panel_area
        self.panel_eff = panel_eff
        self.battery_capacity = battery_capacity_wh
        self.battery_charge = initial_charge_wh
        self.solar_constant = 1361.0  # W/m^2 at 1 AU
        self.essential_load = 50.0   # W
        self.payload_load = 150.0    # W
        self.load_shedding_active = False

    def update(self, sun_distance_au, dt_hours=1.0):
        # Solar flux decreases with inverse square of distance
        solar_flux = self.solar_constant / (sun_distance_au ** 2)
        solar_output = solar_flux * self.panel_area * self.panel_eff

        # Load shedding logic
        battery_soc_pct = (self.battery_charge / self.battery_capacity) * 100.0
        if battery_soc_pct < 20.0:
            self.load_shedding_active = True
            consumption = self.essential_load
        else:
            self.load_shedding_active = False
            consumption = self.essential_load + self.payload_load

        net_power = solar_output - consumption
        self.battery_charge += net_power * dt_hours
        
        # Clamp battery charge between 0 and capacity
        self.battery_charge = min(max(self.battery_charge, 0.0), self.battery_capacity)

        return {
            "solar_output_w": solar_output,
            "consumption_w": consumption,
            "battery_charge_wh": self.battery_charge,
            "battery_soc_pct": (self.battery_charge / self.battery_capacity) * 100.0,
            "load_shedding_active": self.load_shedding_active
        }
