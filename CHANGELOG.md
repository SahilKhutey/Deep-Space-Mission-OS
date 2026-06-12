# Changelog

All notable changes to **Deep Space Mission OS** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [v3.0.0] — 2026-06-12 — Digital Twin & Propulsion Diagnostics

### Added
- **Digital Twin Diagnostics Dashboard** — Full tabbed panel with 5 modules:
  - 🛰️ **EKF Filter** — Extended Kalman Filter state estimator on circular Keplerian orbit with configurable fault injection (orbit radius, noise σ, step fault magnitude); dual-axis Plotly chart
  - 📡 **CCSDS Parser** — Decode any CCSDS Space Packet from hex string; field table output
  - 🔮 **Anomaly Forecast** — AI Digital Twin anomaly prediction from telemetry history; forecast chart with safety zone band
  - 🔬 **Vacuum Sim** — Chamber pressure decay (first-order pump/leak model); log-scale Plotly chart
  - ⚗️ **Grid Erosion** — Ion thruster grid erosion rate using Yamamura-Tawara (1996) model; material database for Mo, C, W, Ti

- **Backend API Endpoints (5 new)**:
  - `POST /api/v1/digital-twin/ekf-simulate`
  - `POST /api/v1/digital-twin/ccsds-parse`
  - `POST /api/v1/digital-twin/anomaly-predict`
  - `POST /api/v1/propulsion/vacuum-simulate`
  - `POST /api/v1/propulsion/erosion-rate`

- **9 new automated tests** (`@pytest.mark.diagnostics`) covering all 5 endpoints including edge cases (invalid hex, unknown material, anomaly detection)

- **`pytest.ini`** — Created to register `dashboard` and `diagnostics` custom marks

### Fixed
- **EKF endpoint** — Rewritten to simulate physically correct circular orbit dynamics instead of disconnected random walk
- **Erosion endpoint** — Removed broken import of non-existent `lifetime_materials` module; replaced with self-contained Yamamura-Tawara sputter yield physics

### Changed
- `EKFSimRequest` Pydantic model updated with orbit-centric parameters (`orbit_radius_km`, `dt_s`, `measurement_noise_km`, `fault_step`, `fault_magnitude_km`); legacy fields preserved for backward compatibility

---

## [v2.0.0] — 2026-06-11 — Monte Carlo, Transfers & Station-Keeping

### Added
- **Monte Carlo Uncertainty Dispersion** — 3σ trajectory envelope propagation with configurable runs, position/velocity noise
- **Hohmann Transfer Solver** — Two-impulse coplanar transfer with ΔV₁, ΔV₂, TOF
- **Bi-elliptic Transfer Solver** — Three-impulse with configurable boost apoapsis
- **Low-Thrust Spiral Transfer** — Mass-flow integrated with configurable thrust and Isp
- **Active Station-Keeping Engine** — Impulsive apoapsis burn with Tsiolkovsky fuel accounting and depletion warning
- **Fuel Allocation Warning** — HUD alert when propellant budget is exceeded
- **Atmospheric Entry Boundary Detection** — Color-glow HUD warning when orbit dips below 120 km (Earth)

### Fixed
- Low-thrust spiral solver missing `return` statement causing silent 500 errors

---

## [v1.2.0] — 2026-06-10 — Sun-Synchronous & N-Body Perturbations

### Added
- **Sun-Synchronous Design Tool** — Automatic inclination solver and RAAN optimizer from launch calendar date/LTAN
- **N-Body Perturbation Propagation** — Lunar and solar third-body gravity perturbations
- **J₂ Perturbation Toggles** — Nodal precession (Ω̇) and apsidal rotation (ω̇) rates displayed in HUD
- **Atmospheric Drag Entry Warning** — HUD glow-shift when numerical propagation detects altitude < 120 km

---

## [v1.1.0] — 2026-06-09 — Orbit Tweaker & Visualization

### Added
- **Interactive Orbit Tweaker** — Real-time vis-viva solver with sliders for a, e, i, Ω
- **Live Telemetry HUD** — Periapsis/apoapsis velocity, altitude, and orbital period display
- **Animated Playback Controls** — Time-scrubber for replaying simulated trajectories
- **Porkchop Plot Generator** — C₃ launch energy contour plots for interplanetary missions

---

## [v1.0.0] — 2026-06-08 — Initial Release

### Added
- FastAPI REST backend with mission planning, fuel calculation, and delta-V budgeting
- Genetic Algorithm, PSO, and Differential Evolution trajectory optimizers
- Numerical orbit propagation (RK4, Dormand-Prince, Adams-Bashforth-Moulton)
- Earth-Mars, Earth-Moon, and asteroid rendezvous simulations
- Glassmorphism dark-mode web dashboard
- Python SDK and CLI tools
- 166-test validation suite
