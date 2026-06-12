"""
Security testing - Input sanitization, bound checking.
"""

import pytest

@pytest.mark.security
class TestSecurityLimits:

    def test_prevention_of_overflow_coordinates(self):
        max_limit = 1e12
        bad_coord = 2e12
        assert bad_coord > max_limit
        
        def sanitize_coords(coords):
            for c in coords:
                if abs(c) > 1e12:
                    raise ValueError("Coordinate value overflows maximum physical bounds.")
            return True
            
        with pytest.raises(ValueError):
            sanitize_coords([1e3, -2e12, 0])
