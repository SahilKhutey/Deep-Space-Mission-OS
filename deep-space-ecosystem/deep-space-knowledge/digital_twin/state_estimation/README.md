# State Estimation for Digital Twin

## Models of Each Subsystem
Power: solar array I-V curve, battery SOC dynamics
Thermal: lumped-mass RC network
Propulsion: thrust + Isp from telemetry
Comms: link budget equations
Attitude: kinematic + dynamic equations

## State Vector
x = [r, v, q, ω, T_battery, SOC, T_components, ...]

## Estimator Selection
Linear Gaussian: Kalman Filter
Nonlinear Gaussian: EKF, UKF
Nonlinear Non-Gaussian: Particle Filter

## Reference
- NASA's GMAT Kalman module
- ESA's GODOT operational tool
- NASA STD-7009 model-based systems engineering
