# Root Finding — Critical for Kepler's Equation and Lambert

## Newton-Raphson Method

x_{n+1} = x_n − f(x_n) / f'(x_n)

Convergence: quadratic
Required: smooth f, good initial guess

Used in:
- Kepler's equation: M = E − e·sin(E)
- Lambert solver (z iteration)
- Orbit determination

## Bisection Method

Reliable but slow: linear convergence

Used in:
- Fallback for Newton-Raphson divergence
- Bracketing where derivative is unknown

## Secant Method
x_{n+1} = x_n − f(x_n)·(x_n − x_{n-1}) / (f(x_n) − f(x_{n-1}))

Convergence: 1.618 (golden ratio)
No derivative required
