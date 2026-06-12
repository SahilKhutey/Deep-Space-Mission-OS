# Ordinary Differential Equations — The Heart of Dynamics

## Two-Body Equation
d²r/dt² = −(μ/r³)·r

This is THE central equation of orbital mechanics.
Linearized → Keplerian analytical solution
Nonlinear → must integrate numerically

## N-Body Equation
m_i · d²r_i/dt² = G · Σ_{j≠i} m_j · (r_j − r_i) / |r_j − r_i|³

For deep space, must integrate numerically.

## Equations of Motion (Spacecraft)
ẋ = v
v̇ = a_grav + a_thrust + a_drag + a_SRP + a_J2 + ...

## Stiffness
Some systems (e.g., chemical kinetics) are stiff
→ use implicit methods (Radau, BDF)

## Lyapunov Stability
Used in:
- Relative motion (Hill-Clohessy-Wiltshire)
- Formation flying
- Libration point stability (Lyapunov, Halo orbits)
