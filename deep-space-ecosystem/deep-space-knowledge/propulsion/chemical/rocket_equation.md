# Tsiolkovsky Rocket Equation

## Statement
ΔV = Isp · g₀ · ln(m₀ / m_f)

Where:
- ΔV = velocity change (m/s)
- Isp = specific impulse (seconds)
- g₀ = 9.80665 m/s²
- m₀ = initial mass (wet + dry)
- m_f = final mass (dry)

## Mass Ratio
MR = m₀ / m_f = exp(ΔV / (Isp·g₀))

## Propellant Mass
m_p = m₀ · (1 − 1/MR) = m₀ · (1 − exp(−ΔV/(Isp·g₀)))

## Propellant Fraction
`\zeta = m_p / m_0`

## Multi-Stage Optimization
For N stages, total ΔV = Σ ΔV_i
Optimal staging: minimize Σ (ΔV_i / (Isp_i · g₀))
Use Lagrange multipliers on mass constraint.
