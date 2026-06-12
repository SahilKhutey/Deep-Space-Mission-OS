# Spacecraft Design Engineering

## Mass Budget
m_total = m_dry + m_propellant + m_payload

m_dry = m_structure + m_power + m_propulsion + m_ADCS
       + m_thermal + m_comms + m_payload + m_margin

Margin: 20-30% on dry mass standard.

## Power Budget
P_total = P_payload + P_thermal + P_comms + P_ADCS + P_propulsion
Power source sizing based on:
- Eclipse time
- Solar constant (at planet)
- RTG output (if applicable)
- Battery capacity

## Thermal Design
Q_in = Q_solar + Q_albedo + Q_planet_IR
Q_out = Q_radiation + Q_conduction

T⁴ = T₀⁴ + Q_rad / (σ·A·ε)
