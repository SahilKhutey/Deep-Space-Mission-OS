# Numerical Integrators

## Selection Criteria

| Method | Order | Use Case |
|--------|-------|----------|
| Euler | 1 | Never for production |
| RK4 | 4 | Smooth, non-stiff |
| RK45 (Dormand-Prince) | 5(4) | Adaptive, smooth |
| Radau | 5 | Stiff |
| BDF | 1-6 | Very stiff |
| Symplectic | 2+ | Long-term energy conservation |
| Gauss-Jackson | 8 | Long-duration precision |

## For Orbit Propagation
- Short missions (< 1 year): RK4 or RK45
- Long missions (> 1 year): Gauss-Jackson, symplectic
- Multi-body: RK45 with tight tolerance
- N-body: RK45 with adaptive step
