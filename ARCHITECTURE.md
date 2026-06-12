# Deep Space Mission Planner (DSMP)
## System Architecture Document

**Version:** 1.0
**Status:** Production-Ready Foundation
**Audience:** Aerospace Engineers, Mission Designers, Software Architects, Research Institutions

---

## 1. System Overview

The Deep Space Mission Planner (DSMP) is a scientific mission-design platform used to
design, simulate, optimize, and validate deep-space missions. It provides a unified
engineering environment bridging classical astrodynamics with modern computational
infrastructure.

### 1.1 Mission Domains Supported
- Earth → Cislunar (Lunar) Missions
- Earth → Mars (Trans-planetary) Missions
- Asteroid Rendezvous and Sampling Missions
- Multi-body (Lagrange point) Missions (V2)
- Deep Space Exploration Missions (V3)

### 1.2 Engineering Disciplines Integrated
- Astrodynamics (Keplerian + N-Body)
- Mission Planning & Sequencing
- Propulsion Modeling (Chemical, Electric, Nuclear)
- Numerical Optimization (GA, PSO, DE)
- Numerical Simulation (RK4, Dormand-Prince, Gauss-Jackson)
- Scientific Visualization (3D, Gantt, Porkchop)
- Validation & Verification (V&V)

---

## 2. Architectural Principles

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | UI, API, Engine, and Scientific layers are fully decoupled |
| **Domain Purity** | Core scientific modules are pure functions, no I/O dependencies |
| **Numerical Reproducibility** | All computations are deterministic, seeded, and unit-tested |
| **Testability** | Every scientific module is independently testable against reference solutions |
| **Extensibility** | New trajectories, propagators, and propulsion types can be added without modification |
| **Data Integrity** | SPICE-based ephemeris with pluggable backends (SPICE, Poliastro, Analytical) |
| **API-First** | Every engine exposes a typed contract via Pydantic |
| **Defense in Depth Validation** | Trajectory, energy, fuel, and feasibility checks at every output |

---

## 3. High-Level Architecture (Layered Model)

```
┌────────────────────────────────────────────────────────────────┐
│ LAYER 5 │                   CLIENT LAYER                       │
│         │ React Dashboard · Mission Designer · Orbit Viewer    │
│         │ Timeline Dashboard · Report Generator                │
└────────────────────────────────────────────────────────────────┘
                               ↓ HTTPS / WebSocket
┌────────────────────────────────────────────────────────────────┐
│ LAYER 4 │           API LAYER (FastAPI Gateway)                │
│         │ Auth · Rate Limiting · Mission APIs · Sim APIs       │
│         │ Pydantic Schemas · Request/Response Validation       │
└────────────────────────────────────────────────────────────────┘
                               ↓ Internal Service Bus
┌────────────────────────────────────────────────────────────────┐
│ LAYER 3 │              MISSION ENGINE LAYER                    │
│         │ Mission Planner · Trajectory Designer                 │
│         │ ΔV Calculator · Fuel Estimator · Risk Engine         │
└────────────────────────────────────────────────────────────────┘
                               ↓ Pure-Function API
┌────────────────────────────────────────────────────────────────┐
│ LAYER 2 │           SCIENTIFIC COMPUTING LAYER                 │
│         │ Astrodynamics · Propagation · Optimization           │
│         │ Numerical Solvers · Stumpff Functions                │
└────────────────────────────────────────────────────────────────┘
                               ↓ Data Access Abstraction
┌────────────────────────────────────────────────────────────────┐
│ LAYER 1 │                    DATA LAYER                        │
│         │ SPICE Kernels · PostgreSQL · TimescaleDB             │
│         │ Simulation Results · Planetary Ephemeris             │
└────────────────────────────────────────────────────────────────┘
```

---

## 4. Core Subsystems (Engineering View)

### 4.1 Mission Planning Subsystem
**Responsibility:** Mission definition, target selection, launch date planning,
transfer strategy generation, constraint enforcement.

**Inputs:** MissionConfig (origin, destination, mass, propulsion, payload, launch_date)
**Outputs:** MissionProfile, Timeline, DeltaVBudget, PhaseSequence

**Key Components:**
- `core/mission/planner/` — Top-level mission orchestrator
- `core/mission/phases/` — Phase definitions (Launch → Cruise → Arrival)
- `core/mission/timeline/` — Event sequence generation
- `core/mission/constraints/` — Mission feasibility constraints

---

### 4.2 Astrodynamics Subsystem
**Responsibility:** Orbit calculations, Lambert solutions, transfer trajectories,
planetary ephemeris, gravity assists.

**Mathematical Foundation:**
- Kepler's Equation: $M = E − e \sin E$
- Vis-Viva: $v = \sqrt{\mu \left(\frac{2}{r} − \frac{1}{a}\right)}$
- Specific Energy: $\mathcal{E} = -\frac{\mu}{2a}$
- Stumpff Functions: $S(z)$, $C(z)$ for universal variable formulation
- Lambert's Theorem: Two-point boundary value problem

**Key Components:**
- `core/astrodynamics/orbital_mechanics/` — Keplerian motion, two-body problem
- `core/astrodynamics/lambert/` — Universal variable Lambert solver
- `core/astrodynamics/propagators/` — Numerical orbit propagation
- `core/astrodynamics/perturbations/` — J2, drag, SRP, third-body
- `core/astrodynamics/gravity_assists/` — $V_{\infty}$-leveraging, flyby geometry
- `core/astrodynamics/ephemeris/` — SPICE/Poliastro backends

---

### 4.3 Propulsion Analysis Subsystem
**Responsibility:** Chemical, electric, nuclear, and hybrid propulsion modeling.

**Mathematical Foundation:**
- Tsiolkovsky Equation: $\Delta V = I_{sp} g_0 \ln\left(\frac{m_0}{m_f}\right)$
- Mass Ratio: $MR = \frac{m_0}{m_f}$
- Propellant Fraction: $\zeta = \frac{m_p}{m_0}$

**Key Components:**
- `core/propulsion/chemical/` — Bipropellant, solid, staged
- `core/propulsion/electric/` — Ion, Hall, VASIMR
- `core/propulsion/nuclear/` — NEP, NTP
- `core/propulsion/hybrid/` — Combined-cycle

---

### 4.4 Optimization Subsystem
**Responsibility:** Multi-objective trajectory optimization.

**Algorithms:**
- Genetic Algorithms (GA)
- Particle Swarm Optimization (PSO)
- Differential Evolution (DE)
- Simulated Annealing (SA)
- Multi-Objective NSGA-II

**Key Components:**
- `core/optimization/genetic/`
- `core/optimization/pso/`
- `core/optimization/differential_evolution/`
- `core/optimization/multi_objective/`

---

### 4.5 Simulation Subsystem
**Responsibility:** Mission propagation, gravity modeling, maneuver execution,
numerical integration.

**Integration Methods:**
- Runge-Kutta 4 (RK4) — Phase 1 baseline
- Dormand-Prince (RK45) — Adaptive, Phase 2 high-fidelity
- Gauss-Jackson — Long-duration, Phase 3

**Key Components:**
- `simulation/engines/patched_conic/` — Fast Phase 1
- `simulation/engines/nbody/` — Full Phase 3
- `simulation/engines/rk4/`
- `simulation/engines/dormand_prince/`
- `simulation/engines/gauss_jackson/`
- `simulation/scenarios/{moon,mars,asteroid}/`
- `simulation/monte_carlo/` — Uncertainty quantification

---

### 4.6 Validation Subsystem
**Responsibility:** Scientific correctness of every result before delivery to API.

**Validation Checks:**
1. **Trajectory Validation** — Endpoints match input state vectors
2. **Energy Conservation** — Specific energy stable to < 1e-8 in closed systems
3. **Orbital Consistency** — Position/velocity satisfy conic equation
4. **Fuel Validation** — Mass monotonicity through burn sequence
5. **Numerical Stability** — Integrator residuals below tolerance
6. **Mission Feasibility** — ΔV, mass, propellant fraction within bounds

---

## 5. Mission Planning Pipeline (Data Flow)

```
[Mission Definition]
        │ (mission_config dict / Pydantic)
        ▼
 [Mission Planner]  ← validates inputs, applies constraints
        │
        ▼
[Trajectory Generator]  ← selects strategy (Hohmann/Lambert/Low-thrust)
        │
        ▼
   [ΔV Engine]      ← computes burn-by-burn velocity changes
        │
        ▼
 [Fuel Estimator]   ← applies Tsiolkovsky per burn
        │
        ▼
[Simulation Engine] ← forward-propagates with chosen fidelity
        │
        ▼
[Validation Engine] ← energy/orbit/mass checks
        │
        ▼
[Dashboard Visualization]
```

**Pipeline Properties:**
- **Idempotent:** Same input always produces same output
- **Stateless:** Each module can be called independently
- **Composable:** Modules can be chained into custom pipelines
- **Auditable:** Every output carries provenance metadata

---

## 6. Computational Layers (Fidelity Tiers)

| Layer | Name | Use Case | Methods |
|-------|------|----------|---------|
| **L1** | Analytical | Fast first-pass design | Hohmann, Patched-Conic |
| **L2** | Semi-Analytical | Trade studies, mission ops | Lambert, Gravity Assists, J2 |
| **L3** | Numerical | High-fidelity campaigns | N-Body, SRP, multi-body, full perturbations |
| **L4** | Monte Carlo | Risk, reliability, uncertainty | UQ over L1-L3 |

**Selection Logic:**
- V1 (SaaS) → L1 only
- V2 (Professional) → L1 + L2
- V3 (Autonomous) → L1 + L2 + L3 + L4

---

## 7. Data Architecture

### 7.1 Data Sources
- **JPL SPICE Kernels** — High-fidelity planetary ephemeris (de421.bsp, naif0012.tls)
- **Poliastro Built-in** — Analytical Keplerian ephemeris
- **ESA NEO Coordination Centre** — Asteroid catalog
- **NASA NTRS** — Propulsion performance database
- **Celestrak** — Launch vehicle performance envelopes

### 7.2 Database Schema
- `missions` — Mission configurations and metadata
- `trajectories` — Computed state vectors (TimescaleDB hypertables)
- `delta_v_budgets` — Burn-by-burn budget history
- `simulations` — Full simulation runs with provenance
- `users` — Authentication, RBAC
- `audit_log` — Compliance and traceability

### 7.3 Data Validation
- All inputs validated via Pydantic
- All outputs validated via `core/validation/`
- All DB writes wrapped in transactions

---

## 8. API Architecture

### 8.1 REST Endpoints
- `POST /api/v1/mission/plan` — Full mission design
- `POST /api/v1/trajectory/lambert` — Solve Lambert's problem
- `POST /api/v1/deltav/budget` — Compute ΔV budget
- `POST /api/v1/fuel/compute` — Propellant mass
- `POST /api/v1/simulate/propagate` — Run propagation
- `POST /api/v1/optimize/mission` — Run optimization
- `GET  /api/v1/presets/{moon|mars|asteroid}` — Standard profiles

### 8.2 WebSocket Channels
- `/ws/simulation/{id}` — Live simulation progress
- `/ws/optimization/{id}` — Optimization convergence plots

### 8.3 Authentication
- JWT-based with refresh tokens
- RBAC: `student | researcher | engineer | admin`
- API key support for institutional integration

---

## 9. Validation & Verification Framework

Every computation passes through the validation engine before reaching the API:

```python
def validate(result):
    assert check_trajectory_continuity(result)
    assert check_energy_conservation(result, tol=1e-8)
    assert check_mass_monotonicity(result)
    assert check_orbital_elements(result)
    assert check_fuel_mass(result)
    assert check_feasibility(result)
```

### Reference Solutions:
- Vallado "Fundamentals of Astrodynamics" examples
- NASA GMAT benchmark cases
- ESA ACT tests
- ESA NEO flyby reference trajectories

---

## 10. Deployment Architecture

| Tier | Target | Stack |
|------|--------|-------|
| **Dev** | Docker Compose | FastAPI, Postgres, Redis, Celery |
| **Staging** | Kubernetes (EKS/GKE) | Helm chart, Prometheus, Grafana |
| **Production** | Multi-region K8s | Istio, ArgoCD, Terraform, CloudFront |

---

## 11. Glossary
- **ΔV**: Delta-V — velocity change required for a maneuver
- **C3**: Characteristic energy — $v_{\infty}^2$ at departure
- **TOF**: Time of flight
- **Isp**: Specific impulse (seconds)
- **SOI**: Sphere of influence
- **SRP**: Solar radiation pressure
- **J2**: Earth's oblateness perturbation
- **$V_{\infty}$**: Hyperbolic excess velocity
