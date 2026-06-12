# Contributing to Deep Space Core

## Code Standards

*   All public functions must have docstrings with scientific source references.
*   All functions must be unit-tested with reference solutions.
*   Type hints are required on all signatures.
*   Black formatting standard.
*   No global state.

## Pull Request Process

1.  Open an issue explaining the motivation.
2.  Add tests FIRST.
3.  Reference the source (textbook, paper, or standard) in comments.
4.  Update `ARCHITECTURE.md` if changing the dependency graph.

## Validation Required

Every new equation must:
*   Cite its source.
*   Pass a reference test (Vallado, GMAT, etc.).
*   Be dimensionally consistent.
