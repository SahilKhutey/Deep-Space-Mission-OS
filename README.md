<h1 align="center">
  🚀 Deep Space Mission OS
</h1>

<p align="center">
  <strong>Professional Aerospace Engineering &amp; Trajectory Design Platform</strong><br>
  Astrodynamics · Orbital Mechanics · Digital Twin · Propulsion Diagnostics
</p>

<p align="center">
  <a href="https://github.com/SahilKhutey/Deep-Space-Mission-OS/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
  </a>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python 3.9+">
  </a>
  <img src="https://img.shields.io/badge/FastAPI-0.104%2B-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Tests-175%20Passing-brightgreen" alt="Tests">
  <img src="https://img.shields.io/badge/Platform-Web%20Dashboard-purple" alt="Dashboard">
</p>

---

## 📡 Overview

**Deep Space Mission OS** is a full-stack, production-grade aerospace engineering platform providing:

- **Interactive 3D Orbital Visualization** — Plotly.js-powered trajectory rendering with live telemetry HUD
- **Mission Planning & Delta-V Budgeting** — Tsiolkovsky rocket equation, multi-stage sizing, and propellant fractions
- **Interplanetary Porkchop Plots** — C₃ launch energy optimization grids for Earth-Mars, Lunar, and asteroid destinations
- **Trajectory Optimization** — Genetic Algorithm, Particle Swarm, and Differential Evolution solvers
- **J₂ Perturbation Propagation** — Nodal precession (Ω̇) and apsidal rotation (ω̇) over configurable timelines
- **N-Body Perturbations** — Lunar and solar third-body gravity integrated via adaptive Dormand-Prince RK5(4) propagator
- **Sun-Synchronous Design Tool** — Automatic inclination solver + RAAN optimizer from launch calendar date
- **Monte Carlo Uncertainty Dispersion** — 3σ trajectory envelope visualization across perturbed initial conditions
- **Active Station-Keeping Engine** — Impulsive ΔV burn simulator with fuel allocation and depletion warnings
- **Orbital Transfer Solver** — Hohmann, Bi-elliptic, and Low-Thrust Spiral transfer computations
- **Digital Twin Diagnostics** — EKF state estimation, CCSDS telemetry parsing, AI anomaly forecasting
- **Propulsion Simulation** — Vacuum chamber pressure decay and ion thruster grid erosion rate (Yamamura-Tawara model)

---

## 🖥️ Dashboard Preview

The platform features a glassmorphism dark-mode UI with:

- 🛸 **3D Trajectory Viewer** with animated playback controls
- 📊 **Porkchop Contour Plots** and optimizer convergence charts
- 🎯 **Live Orbit Tweaker** with real-time vis-viva feedback
- 🔭 **5-Tab Diagnostics Panel** (EKF · CCSDS · Anomaly · Vacuum · Erosion)

---

## 🏗️ Architecture

```
Deep Space Mission OS/
│
├── backend/
│   ├── api/
│   │   └── main.py              # FastAPI REST server (1,300+ lines, 35+ endpoints)
│   └── static/
│       ├── index.html           # Single-page dashboard (600+ lines)
│       ├── style.css            # Glassmorphism design system (760+ lines)
│       └── app.js               # Interactive JS logic (2,100+ lines)
│
├── deep-space-ecosystem/
│   ├── deep-space-core/         # Astrodynamics kernel (Keplerian, Lambert, propagators)
│   ├── deep-space-mission-planner/  # Mission engine & optimizer
│   ├── deep-space-digital-twin/ # EKF, CCSDS telemetry, AI anomaly twin
│   ├── deep-space-propulsion-simulator/ # Electric, chemical, nuclear propulsion
│   ├── deep-space-sdk/          # Python SDK & CLI tools
│   ├── deep-space-datasets/     # Validated reference datasets
│   ├── deep-space-docs/         # API documentation
│   └── deep-space-knowledge/    # Mathematics & physics libraries
│
├── simulations/                 # Standalone scenario scripts (Mars, Moon, Asteroid)
├── tests/                       # 175-test verification suite
│   ├── test_tweaker_api.py      # Orbit tweaker + diagnostics endpoint tests
│   ├── test_phase5_ai.py        # AI digital twin tests
│   ├── test_sdk.py              # SDK & CLI integration tests
│   └── unit/                   # Unit tests (algebra, constants, propagators)
│
├── ARCHITECTURE.md              # Deep system design documentation
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
└── pytest.ini                   # Test configuration
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python **3.9+**
- pip / virtualenv

### 1. Clone the Repository
```bash
git clone https://github.com/SahilKhutey/Deep-Space-Mission-OS.git
cd Deep-Space-Mission-OS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Dashboard Server
```bash
uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

### 4. API Documentation (Swagger UI)
```
http://127.0.0.1:8000/docs
```

---

## 🚀 API Endpoint Reference

### Mission Planning
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/mission/plan` | POST | Full interplanetary mission plan with feasibility check |
| `/api/v1/fuel/compute` | POST | Tsiolkovsky propellant mass calculation |
| `/api/v1/deltav/budget` | POST | Segment-by-segment ΔV budget tracker |
| `/api/v1/staging/size` | POST | Multi-stage rocket sizing |
| `/api/v1/presets/mars` | GET | Pre-planned Mars mission architecture |
| `/api/v1/presets/moon` | GET | Pre-planned Lunar mission architecture |

### Trajectory & Optimization
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/porkchop/generate` | POST | Porkchop C₃ launch energy grid |
| `/api/v1/optimization/optimize` | POST | GA / PSO / DE launch window optimizer |
| `/api/v1/simulations/run` | POST | Numerical trajectory propagation (Mars, Moon, Asteroid) |

### Astrodynamics Toolkit
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/astrodynamics/vis-viva` | POST | Vis-viva velocities + J₂ precession rates |
| `/api/v1/astrodynamics/propagate-perturbed` | POST | J₂ + N-body perturbed propagation |
| `/api/v1/astrodynamics/sun-synchronous` | POST | Sun-synchronous inclination solver |
| `/api/v1/astrodynamics/sunsync-raan` | POST | RAAN optimizer from launch date |
| `/api/v1/astrodynamics/station-keeping` | POST | Station-keeping burn + fuel warning |
| `/api/v1/astrodynamics/hohmann` | POST | Hohmann transfer ΔV computation |
| `/api/v1/astrodynamics/bielliptic` | POST | Bi-elliptic transfer ΔV computation |
| `/api/v1/astrodynamics/low-thrust-spiral` | POST | Low-thrust spiral transfer solver |
| `/api/v1/astrodynamics/monte-carlo` | POST | Monte Carlo 3σ dispersion envelopes |

### Digital Twin & Propulsion Diagnostics
| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/digital-twin/ekf-simulate` | POST | EKF state estimator on circular orbit with fault injection |
| `/api/v1/digital-twin/ccsds-parse` | POST | Decode CCSDS Space Packet from hex |
| `/api/v1/digital-twin/anomaly-predict` | POST | AI twin anomaly forecasting from telemetry history |
| `/api/v1/propulsion/vacuum-simulate` | POST | Vacuum chamber pressure decay simulation |
| `/api/v1/propulsion/erosion-rate` | POST | Ion thruster grid erosion rate (Yamamura-Tawara model) |

---

## 🔬 Key Physics Models

### Orbital Mechanics
| Model | Implementation |
|---|---|
| **Vis-Viva Equation** | $v = \sqrt{\mu\left(\tfrac{2}{r} - \tfrac{1}{a}\right)}$ |
| **Kepler's Equation** | Newton-Raphson with bisection fallback |
| **J₂ Perturbation** | Nodal precession $\dot\Omega = -\tfrac{3}{2}nJ_2\left(\tfrac{R}{p}\right)^2\cos i$ |
| **Lambert's Problem** | Universal Variable Formulation |
| **Hohmann Transfer** | Two-impulse coplanar |
| **Bi-elliptic Transfer** | Three-impulse with configurable boost apoapsis |
| **Low-Thrust Spiral** | Mass-flow integrated Edelbaum-style solver |
| **Monte Carlo Dispersion** | Gaussian state perturbations, 3σ envelope |

### Propagators
| Integrator | Order | Usage |
|---|---|---|
| Dormand-Prince RK5(4) | 5th-order | Adaptive perturbed orbit propagation |
| Adams-Bashforth-Moulton | 4th-order | Long-arc mission propagation |
| Classical RK4 | 4th-order | Fixed-step orbit simulation |

### Propulsion Science
| Model | Description |
|---|---|
| **Tsiolkovsky Rocket Equation** | Multi-stage mass-ratio and propellant sizing |
| **Yamamura-Tawara (1996)** | Ion thruster grid sputter-yield: $Y(E) = Y_{300}\cdot(E/300)^{0.6}\cdot(1-\sqrt{E_{th}/E})^2$ |
| **Vacuum Chamber Model** | First-order pressure decay: $\dot{p} = Q_{leak}/V - S\cdot p/V$ |

---

## 🧪 Running Tests

```bash
# Run full test suite (175 tests)
python -m pytest tests/ -v

# Run only astrodynamics tests
python -m pytest tests/ -m dashboard -v

# Run only diagnostics tests
python -m pytest tests/ -m diagnostics -v

# Run unit tests only
python -m pytest tests/unit/ -v
```

Expected output:
```
====================== 175 passed in ~12s =======================
```

---

## 📦 Python SDK

A fully-typed Python SDK and CLI are included in `deep-space-ecosystem/deep-space-sdk/`:

```python
from deep_space_sdk import DeepSpaceClient

client = DeepSpaceClient(base_url="http://127.0.0.1:8000")

# Plan a mission
plan = client.plan_mission(
    destination="Mars",
    spacecraft_mass=2500,
    propulsion_type="Chemical",
    payload_mass=800,
    launch_date="2032-08-15"
)
print(plan)
```

CLI usage:
```bash
python -m deep_space_sdk.cli mission-plan --destination mars --mass 2500
python -m deep_space_sdk.cli cost-estimate --destination mars
python -m deep_space_sdk.cli risk-report
python -m deep_space_sdk.cli digital-twin-check
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍🚀 Author

**Sahil Khutey**  
[GitHub](https://github.com/SahilKhutey) · Deep Space Mission OS

---

<p align="center">
  <em>Built with ❤️ for the future of space exploration</em>
</p>
