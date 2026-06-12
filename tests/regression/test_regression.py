"""
Regression testing against frozen outputs.
"""

import pytest
import numpy as np
from deep_space_core.mathematics.algebra import rocket_equation_delta_v

@pytest.mark.regression
class TestRegression:

    def test_rocket_equation_regression(self):
        frozen_dv = 6145.188547690648
        current_dv = rocket_equation_delta_v(311, 15000, 2000)
        assert abs(current_dv - frozen_dv) < 1e-4
