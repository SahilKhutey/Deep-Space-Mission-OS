# Deep Space Mission Planner

The mission planner application layer. Built on top of `deep-space-core` for trajectory design, Delta-V optimization, porkchop calculations, and timeline scheduling.

## Modules

*   `mission_engine/` — Coordinates transfers (Hohmann, bi-elliptic, low-thrust) and captures.
*   `trajectory_engine/` — Coordinates 3D orbital representations and parking orbit adjustments.
*   `optimization_engine/` — Integrates global search heuristics (PSO, Genetic, Differential Evolution) for launch windows.
*   `timeline_engine/` — Coordinates events, burns, and scheduling.
*   `launch_window_engine/` — Search optimization engines for Earth-Mars TMI windows.
*   `backend/` — FastAPI endpoint services.
*   `exports/` — Data export managers.
*   `visualization/` — 2D and 3D orbit plots.
