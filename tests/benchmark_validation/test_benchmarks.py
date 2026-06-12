"""
Benchmark validation checking code computations against static benchmarks.
"""

import pytest
import os
import json
import numpy as np

@pytest.mark.benchmark
class TestBenchmarks:

    def test_orbital_mechanics_benchmarks(self):
        benchmarks_dir = os.path.join(os.path.dirname(__file__), "..", "..", "deep-space-benchmarks")
        ref_file = os.path.join(benchmarks_dir, "orbital_mechanics", "reference_orbits.json")
        
        with open(ref_file, "r") as f:
            data = json.load(f)
            
        iss_ref = data["iss"]["velocity_km_s"]
        
        from deep_space_core.constants import MU_EARTH, R_EARTH
        from deep_space_core.astrodynamics import vis_viva
        
        r = R_EARTH + data["iss"]["altitude_km"]
        iss_calc = vis_viva(r, r, MU_EARTH)
        
        rel_diff = abs(iss_calc - iss_ref) / iss_ref
        assert rel_diff < 0.005

    def test_propulsion_benchmarks(self):
        benchmarks_dir = os.path.join(os.path.dirname(__file__), "..", "..", "deep-space-benchmarks")
        ref_file = os.path.join(benchmarks_dir, "propulsion", "engine_specs.json")
        
        with open(ref_file, "r") as f:
            data = json.load(f)
            
        from deep_space_propulsion_simulator.propulsion.chemical.bipropellant import BipropellantEngine
        for eng_name, specs in data.items():
            e = BipropellantEngine(eng_name)
            assert e.Isp == specs["Isp"]
            assert e.thrust == specs["thrust"]
