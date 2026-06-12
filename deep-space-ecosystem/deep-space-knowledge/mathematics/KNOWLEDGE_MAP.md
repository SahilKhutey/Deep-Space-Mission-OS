# Cross-Domain Knowledge Map

This document establishes the traceability from pure and applied mathematical concepts to physics equations, engineering models, and final software modules.

## Domain → Equation → Software Map

| Domain | Equation | Software Module |
|--------|----------|-----------------|
| Algebra | Tsiolkovsky (log) | core/fuel_models/tsiolkovsky.py |
| Trigonometry | True anomaly | core/astrodynamics/keplerian.py |
| Calculus | d²r/dt² = -μ/r³/r³ | core/propagators/rk4.py |
| Diff. Eq. | ẋ = Ax + Bu | core/gnc/state_space.py |
| Linear Algebra | R ∈ SO(3) | core/linear_algebra/transforms.py |
| Numerical | Newton-Raphson | core/astrodynamics/keplerian.py |
| Statistics | Bayesian posterior | core/risk_analysis/ |
| Optimization | ∇f = λ∇g | core/optimization/ |
| Dynamical | Lyapunov | core/dynamical_systems/ |
| Astrodynamics | M = E − e·sin(E) | core/astrodynamics/keplerian.py |
| Control | Kalman filter | digital_twin/state_estimation/ |
| ML | ∇L = 0 | ai/trajectory_predictor/ |
