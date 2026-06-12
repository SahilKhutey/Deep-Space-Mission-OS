"""
Pytest configuration and shared fixtures.
"""

import sys
import os
import numpy as np
import pytest

# Add ecosystem repositories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "deep-space-core", "src")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "deep-space-mission-planner")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "deep-space-propulsion-simulator")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "deep-space-digital-twin")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "deep-space-sdk")))

# Reference values
@pytest.fixture(scope="session")
def mu_sun():    return 1.32712440018e11
@pytest.fixture(scope="session")
def mu_earth():  return 3.986004418e5
@pytest.fixture(scope="session")
def mu_moon():   return 4.9048695e3
@pytest.fixture(scope="session")
def mu_mars():   return 4.282837e4
@pytest.fixture(scope="session")
def r_earth():   return 6378.137
@pytest.fixture(scope="session")
def r_moon():    return 1737.4
@pytest.fixture(scope="session")
def r_mars():    return 3389.5
@pytest.fixture(scope="session")
def AU():        return 1.495978707e8
@pytest.fixture(scope="session")
def G0():        return 9.80665

@pytest.fixture
def rng():
    """Seeded RNG for reproducibility."""
    return np.random.default_rng(42)

# Common tolerances
TOL_MATH      = 1e-10   # exact analytical
TOL_NUMERICAL = 1e-6    # numerical
TOL_ENGINEERING = 1e-3  # engineering
TOL_MISSION   = 0.01    # 1% for mission metrics
TOL_PHYSICS   = 1e-8    # conservation laws
