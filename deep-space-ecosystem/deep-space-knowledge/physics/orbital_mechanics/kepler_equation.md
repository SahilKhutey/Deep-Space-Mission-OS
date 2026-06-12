# Kepler's Equation

## Statement
M = E − e·sin(E)

Where:
- M = mean anomaly (linear in time)
- E = eccentric anomaly (auxiliary)
- e = eccentricity

## Solution Methods
1. Newton-Raphson (primary)
2. Series expansion for small e
3. Bessel function series

## Newton-Raphson Iteration
E_{n+1} = E_n − (E_n − e·sin(E_n) − M) / (1 − e·cos(E_n))

Convergence: typically 5-10 iterations
Initial guess: E_0 = M (for e < 0.8) or E_0 = π (for e > 0.8)

## True Anomaly
ν = 2·arctan(√((1+e)/(1-e))·tan(E/2))

## Position
r = a·(1 − e·cos(E))
x = r·cos(ν),  y = r·sin(ν)
