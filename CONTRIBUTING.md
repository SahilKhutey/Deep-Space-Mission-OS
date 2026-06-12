# Contributing to Deep Space Mission OS

Thank you for your interest in contributing! This document outlines how to contribute effectively.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project adheres to respectful, professional collaboration. All contributors are expected to:
- Be respectful and constructive in reviews and discussions
- Focus on technical merit in all feedback
- Follow aerospace engineering best practices

---

## Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_USERNAME/Deep-Space-Mission-OS.git
cd Deep-Space-Mission-OS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install pytest httpx  # test dependencies
```

### 3. Verify Tests Pass
```bash
python -m pytest tests/ -v
```

All 175 tests must pass before submitting a PR.

---

## Development Workflow

### Branch Naming
- `feature/feature-name` — New features
- `fix/bug-description` — Bug fixes
- `docs/doc-section` — Documentation updates
- `test/test-description` — Additional tests

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add cislunar transfer solver
fix: correct Dormand-Prince step rejection condition
docs: update API reference for vis-viva endpoint
test: add edge cases for J2 perturbation propagator
```

---

## Coding Standards

### Python
- Follow **PEP 8** style guide
- Use type hints for all function signatures
- Docstrings required for all public functions (NumPy format preferred)
- Maximum line length: 100 characters

### JavaScript
- ES6+ syntax
- `async/await` for all API calls
- JSDoc comments for exported functions

### Physics Code
- All physical constants must reference a published source in a comment
- Units must be explicitly documented in variable names or docstrings (e.g., `altitude_km`, `velocity_m_s`)
- Mathematical formulas must include the equation in the docstring

---

## Testing Requirements

Every PR must include tests covering new functionality:

```python
@pytest.mark.dashboard   # for astrodynamics endpoints
@pytest.mark.diagnostics # for digital twin / propulsion endpoints
def test_my_new_feature():
    """Test description — what physical invariant does this verify?"""
    payload = { ... }
    r = client.post("/api/v1/...", json=payload)
    assert r.status_code == 200
    data = r.json()
    # Physical invariant checks (not just schema)
    assert data["velocity_km_s"] > 0
    assert data["velocity_km_s"] < 11.2  # Earth escape velocity bound
```

---

## Pull Request Process

1. Ensure all 175 existing tests pass
2. Add tests for new functionality
3. Update `CHANGELOG.md` under `[Unreleased]`
4. Update `README.md` API reference if adding new endpoints
5. Request review from maintainers

---

## Areas for Contribution

- Additional planetary bodies (Venus, Jupiter, Saturn)
- More accurate ephemeris models (JPL SPICE integration)
- WebSocket-based real-time telemetry streaming
- 3D attitude visualization (quaternion-based)
- Chemical propulsion thermal modeling
- Ground station contact window calculator
