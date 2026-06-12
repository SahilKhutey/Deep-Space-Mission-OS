# Knowledge Graph — Cross-Domain Dependencies

This document defines how each knowledge entry connects to others
and to the software systems that consume them.

## Equations → Software Mapping

| Equation | Domain | Implemented In | Validated By |
|----------|--------|----------------|--------------|
| Kepler's Equation | Orbital Mechanics | core/astrodynamics/keplerian.py | Vallado Ex. 2-3 |
| Vis-Viva | Orbital Mechanics | core/astrodynamics/keplerian.py | GMAT benchmark |
| Tsiolkovsky | Propulsion | core/fuel_models/tsiolkovsky.py | NASA NTRS |
| Lambert's Theorem | Astrodynamics | core/astrodynamics/lambert/ | ESA ACT |
| Stumpff Functions | Numerical Methods | core/astrodynamics/lambert/solver.py | Bate-Mueller-White |
| J2 Perturbation | Orbital Mechanics | core/astrodynamics/perturbations/j2.py | Vallado Ex. 8-3 |
| Newton-Raphson | Numerical Methods | core/astrodynamics/keplerian.py | Standard text |
| RK4 | Numerical Methods | core/propagators/rk4.py | Hairer-Norsett |
| Dormand-Prince | Numerical Methods | core/propagators/dormand_prince.py | Hairer-Norsett |
| Gauss-Jackson | Numerical Methods | simulation/engines/gauss_jackson/ | Berry-Healy |
| Kalman Filter | Estimation | digital_twin/state_estimation/ | NASA TN D-7347 |

## Cross-Domain Dependencies

Calculus → Classical Mechanics → Orbital Mechanics → Astrodynamics
Linear Algebra → State Estimation → Digital Twin
Numerical Methods → Simulations → Validation
Physics → Propulsion → Mission Planning
Systems Engineering → Trade Studies → Product Requirements
