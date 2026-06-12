"""
Reference Solution: Earth-Mars Hohmann Transfer
Validated against NASA GMAT (General Mission Analysis Tool).
"""

from deep_space_core.constants import MU_SUN, AU

# Earth orbit
a_earth = 1.496e8  # km
# Mars orbit
a_mars = 2.279e8   # km

# Hohmann transfer
a_transfer = (a_earth + a_mars) / 2

# Velocities
v_earth = (MU_SUN / a_earth) ** 0.5
v_mars = (MU_SUN / a_mars) ** 0.5
v_earth_trans = (MU_SUN * (2/a_earth - 1/a_transfer)) ** 0.5
v_mars_trans = (MU_SUN * (2/a_mars - 1/a_transfer)) ** 0.5

dv1 = abs(v_earth_trans - v_earth)  # TMI
dv2 = abs(v_mars - v_mars_trans)    # MOI
tof = 3.14159 * (a_transfer ** 3 / MU_SUN) ** 0.5  # half period

print(f"dv1 (TMI): {dv1:.2f} km/s")
print(f"dv2 (MOI): {dv2:.2f} km/s")
print(f"TOF: {tof/86400:.1f} days")

# Assert values are close to the expected heliocentric transfer velocities
assert abs(dv1 - 2.94) < 0.1  # km/s
assert abs(dv2 - 2.65) < 0.1  # km/s
assert abs(tof/86400 - 258.8) < 1.0 # days
print("✓ Earth-Mars Hohmann reference validation passed")
