# Numerical Integration — Foundational for Orbit Propagation

## Runge-Kutta 4 (RK4)
y_{n+1} = y_n + (h/6)(k₁ + 2k₂ + 2k₃ + k₄)

Order: 4
Error per step: O(h⁵)
Use: general-purpose, smooth systems

## Dormand-Prince (RK45)
Adaptive step-size, embedded error estimate
Industry standard for orbital mechanics
Order: 5 with 4th-order error estimate

## Gauss-Jackson
8th-order multi-step
Reference: Berry & Healy (JPL)
Use: long-duration high-precision missions

## Symplectic Integrators
Preserve phase-space volume
Use: very long-term integration (resonances, stability)

## Verlet Integration
Used in molecular dynamics
Preserves energy over long times
