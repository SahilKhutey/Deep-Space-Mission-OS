# Deep Space Core

Scientific foundation library for the Deep Space Ecosystem.

Pure scientific computing primitives, fully tested, no domain dependencies. Used by all other repositories.

## Modules

*   `constants/` — Physical and astronomical constants
*   `units/` — Unit conversions and dimensional analysis
*   `mathematics/` — Linear algebra, calculus, ODEs
*   `numerical_methods/` — Root finding, integration, interpolation
*   `astrodynamics/` — Kepler, Lambert, two-body
*   `optimization/` — Gradient methods, GA, PSO
*   `coordinate_systems/` — Frames, transformations
*   `propagators/` — RK4, Dormand-Prince, Gauss-Jackson
*   `ephemeris/` — SPICE, Poliastro, analytical
*   `validation/` — Energy, mass, trajectory checks

## Install

```bash
pip install deep-space-core
```

## Usage

```python
from deep_space_core.constants import MU_SUN
from deep_space_core.astrodynamics.kepler import solve_kepler
```

## License
Apache License 2.0 — see [LICENSE](file:///C:/Users/User/Documents/Deep%20Space%20Mission%20OS/deep-space-ecosystem/deep-space-core/LICENSE).
