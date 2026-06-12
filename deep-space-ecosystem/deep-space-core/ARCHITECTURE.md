# Deep Space Core — Architecture

## Purpose

The scientific foundation of the entire ecosystem. Every other repository depends on this one, but it has no domain dependencies of its own.

## Layer Structure

```
┌──────────────────────────────┐
│       Domain Products        │
│   (mission-planner, etc.)    │
└──────────────────────────────┘
               ↓ depends on
┌──────────────────────────────┐
│       Deep Space Core        │
│                              │
│ constants   · units          │
│ mathematics · numerical      │
│ astrodynamics · propagators  │
│ optimization · ephemeris     │
│ validation                   │
└──────────────────────────────┘
               ↓ references
┌──────────────────────────────┐
│    Knowledge · Datasets      │
└──────────────────────────────┘
```

## Design Principles

1.  **Purity** — No I/O in scientific modules.
2.  **Determinism** — All random number generators are seeded.
3.  **Validation** — Every function has an associated reference validation test.
4.  **Dimensional consistency** — Units must be explicit.
5.  **Pure functions** — No global mutable state.

## Module Dependencies

```
constants ← units
constants ← mathematics
mathematics ← numerical_methods
constants ← astrodynamics
mathematics ← astrodynamics
numerical_methods ← astrodynamics
astrodynamics ← propagators
mathematics ← optimization
validation ← (all)
```

No circular dependencies.
