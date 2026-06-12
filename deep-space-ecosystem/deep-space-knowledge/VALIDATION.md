# Knowledge Validation Framework

Every equation, constant, model, and simulation in this repository
must pass a four-stage validation gate.

## Stage 1 — Source Verification
- Peer-reviewed publication
- NASA/ESA technical report
- Standard textbook (Vallado, Wertz, Bate-Mueller-White)

## Stage 2 — Dimensional Analysis
- All equations dimensionally consistent
- Units explicitly declared in code

## Stage 3 — Reference Solution Test
- Test against published benchmark case
- Tolerance: < 1e-6 relative error

## Stage 4 — Cross-Implementation Check
- Independent reimplementation in a different language
- Independent analytical solution where available
