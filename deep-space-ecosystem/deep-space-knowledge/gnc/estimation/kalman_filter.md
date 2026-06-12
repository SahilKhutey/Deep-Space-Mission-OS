# Kalman Filter

## Linear Kalman Filter

Prediction:
x̂_{k|k-1} = F_k·x̂_{k-1|k-1} + B_k·u_k
P_{k|k-1} = F_k·P_{k-1|k-1}·F_k^T + Q_k

Update:
K_k = P_{k|k-1}·H_k^T·(H_k·P_{k|k-1}·H_k^T + R_k)⁻¹
x̂_{k|k} = x̂_{k|k-1} + K_k·(z_k − H_k·x̂_{k|k-1})
P_{k|k} = (I − K_k·H_k)·P_{k|k-1}

Used for:
- Orbit determination
- GPS navigation
- Spacecraft attitude estimation

## Extended Kalman Filter (EKF)
For nonlinear systems: linearize at current estimate.

## Unscented Kalman Filter (UKF)
Uses sigma points — better for highly nonlinear systems.

## Particle Filter
Monte Carlo for non-Gaussian posteriors.
