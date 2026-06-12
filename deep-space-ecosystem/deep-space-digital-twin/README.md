# Deep Space Spacecraft Digital Twin

This repository contains high-fidelity Digital Twin models for deep space spacecraft. It enables state tracking, telemetry simulation, and anomaly detection across all major vehicle subsystems.

## Subsystems Modeled

1.  **Power Subsystem**: Solar array power generation (with distance-to-Sun $1/d^2$ scaling), battery state of charge (SoC), bus voltage, and load profiles.
2.  **Thermal Subsystem**: Passive thermal radiation equilibrium, heater/radiator state, thermal capacitance, and component temperatures.
3.  **Avionics Subsystem**: CPU load, memory utilization, data buffer states, and subsystem health indicators.
4.  **Guidance, Navigation & Control (GNC)**: Attitude errors (pitch, yaw, roll), reaction wheel speeds, thruster gating status, and navigation Kalman filter residuals.
5.  **Communications Subsystem**: Free-space path loss (FSPL), carrier-to-noise ratio ($C/N_0$), antenna pointing error, and signal strength.

## Digital Twin Orchestration

The `SpacecraftTwin` class coordinates state propagation and runs anomaly detection rules (such as battery degradation, solar panel degradation, radiator blockage, and communication loss) using statistical threshold checks on simulated telemetry.

## Usage

```python
from twin_core.twin import SpacecraftTwin

twin = SpacecraftTwin(spacecraft_mass=1500.0)
telemetry = twin.propagate_state(duration_days=10.0, dt_s=3600.0)
anomalies = twin.detect_anomalies(telemetry)
```
