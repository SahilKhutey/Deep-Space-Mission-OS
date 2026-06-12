"""
DSMP REST API
Provides endpoints for mission planning, delta-V budgeting, propellant mass,
launch window optimization (GA/PSO/DE), porkchop plot calculations, and numerical orbit simulations.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import numpy as np
from datetime import datetime

from mission_engine import MissionEngine
from mission_engine.tsiolkovsky import propellant_mass, build_delta_v_budget, multistage_sizing
from optimization_engine.genetic import optimize_trajectory_ga
from optimization_engine.pso import optimize_trajectory_pso
from optimization_engine.differential_evolution import optimize_trajectory_de
from optimization_engine.porkchop import generate_porkchop_data
from trajectory_engine.earth_mars import date_to_jd, jd_to_date
from trajectory_engine.moon_simulation import run_moon_simulation
from trajectory_engine.mars_simulation import run_mars_simulation
from trajectory_engine.asteroid_simulation import run_asteroid_simulation


app = FastAPI(
    title="Deep Space Mission Planner API",
    description="Professional aerospace mission design, trajectory optimization, and simulation platform API",
    version="1.0.0"
)


# Request and Response schemas
class MissionInput(BaseModel):
    origin: str = "Earth"
    destination: str  # Moon, Mars, Bennu, Psyche
    spacecraft_mass: float  # kg
    propulsion_type: str = "Chemical"  # Chemical, Electric, Nuclear
    payload_mass: float  # kg
    launch_date: str  # YYYY-MM-DD


class FuelRequest(BaseModel):
    Isp: float
    m0: float
    target_dv: float  # m/s or km/s depending on budget


class Segment(BaseModel):
    name: str
    dv: float  # m/s


class DeltaVBudgetRequest(BaseModel):
    Isp: float
    m0: float
    m_payload: float
    segments: List[Segment]


class StagingRequest(BaseModel):
    payload_mass: float
    total_dv: float  # m/s
    Isp_stages: List[float]
    structural_fractions: List[float]


class OptimizationRequest(BaseModel):
    destination: str = "mars"
    algorithm: str = "ga"  # ga, pso, de
    min_departure_date: str  # YYYY-MM-DD
    max_departure_date: str  # YYYY-MM-DD
    min_duration_days: float = 150.0
    max_duration_days: float = 350.0
    population_size: int = 30
    generations: int = 30


class PorkchopRequest(BaseModel):
    destination: str = "mars"
    start_departure_date: str  # YYYY-MM-DD
    end_departure_date: str  # YYYY-MM-DD
    start_arrival_date: str  # YYYY-MM-DD
    end_arrival_date: str  # YYYY-MM-DD
    steps: int = 20


class SimulationRequest(BaseModel):
    destination: str  # moon, mars, bennu, psyche
    launch_date: str  # YYYY-MM-DD
    flight_days: float = 258.0


@app.get("/")
def root():
    return {
        "service": "Deep Space Mission Planner",
        "version": "1.0.0",
        "status": "online"
    }


@app.post("/api/v1/mission/plan")
def plan_mission(mission: MissionInput):
    """Plan a complete interplanetary mission and compute budget/feasibility."""
    try:
        engine = MissionEngine(mission.dict())
        results = engine.plan_mission()
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/fuel/compute")
def compute_fuel(req: FuelRequest):
    """Compute propellant mass using Tsiolkovsky rocket equation."""
    try:
        return propellant_mass(req.Isp, req.m0, req.target_dv)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/deltav/budget")
def compute_delta_v_budget(req: DeltaVBudgetRequest):
    """Build a detailed delta-V budget from individual burn segments."""
    try:
        segs = [s.dict() for s in req.segments]
        return build_delta_v_budget(req.Isp, req.m0, req.m_payload, segs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/staging/size")
def size_stages(req: StagingRequest):
    """Calculate sizing configurations for serial multi-stage rocket systems."""
    try:
        return multistage_sizing(req.payload_mass, req.total_dv, req.Isp_stages, req.structural_fractions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/optimization/optimize")
def optimize_trajectory(req: OptimizationRequest):
    """Optimize trajectory launch window using Genetic, PSO, or Differential Evolution algorithms."""
    try:
        dt_min = datetime.strptime(req.min_departure_date, "%Y-%m-%d")
        dt_max = datetime.strptime(req.max_departure_date, "%Y-%m-%d")
        
        jd_min = date_to_jd(dt_min.year, dt_min.month, dt_min.day)
        jd_max = date_to_jd(dt_max.year, dt_max.month, dt_max.day)
        
        bounds = [
            (jd_min, jd_max),
            (req.min_duration_days, req.max_duration_days)
        ]
        
        algo = req.algorithm.lower().strip()
        
        if algo == "ga":
            results = optimize_trajectory_ga(
                bounds, pop_size=req.population_size, generations=req.generations, destination=req.destination
            )
        elif algo == "pso":
            results = optimize_trajectory_pso(
                bounds, num_particles=req.population_size, iterations=req.generations, destination=req.destination
            )
        elif algo == "de":
            results = optimize_trajectory_de(
                bounds, pop_size=req.population_size, generations=req.generations, destination=req.destination
            )
        else:
            raise ValueError(f"Algorithm '{req.algorithm}' not supported. Use 'ga', 'pso', or 'de'.")
            
        # Add calendar dates to response
        y_d, m_d, d_d = jd_to_date(results["best_departure_jd"])
        y_a, m_a, d_a = jd_to_date(results["best_arrival_jd"])
        
        results["best_departure_calendar"] = f"{y_d:04d}-{m_d:02d}-{int(d_d):02d}"
        results["best_arrival_calendar"] = f"{y_a:04d}-{m_a:02d}-{int(d_a):02d}"
        
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/porkchop/generate")
def get_porkchop(req: PorkchopRequest):
    """Generate Porkchop launch energy C3 and delta-V grid data."""
    try:
        dt_dep_start = datetime.strptime(req.start_departure_date, "%Y-%m-%d")
        dt_dep_end = datetime.strptime(req.end_departure_date, "%Y-%m-%d")
        dt_arr_start = datetime.strptime(req.start_arrival_date, "%Y-%m-%d")
        dt_arr_end = datetime.strptime(req.end_arrival_date, "%Y-%m-%d")
        
        jd_dep_start = date_to_jd(dt_dep_start.year, dt_dep_start.month, dt_dep_start.day)
        jd_dep_end = date_to_jd(dt_dep_end.year, dt_dep_end.month, dt_dep_end.day)
        jd_arr_start = date_to_jd(dt_arr_start.year, dt_arr_start.month, dt_arr_start.day)
        jd_arr_end = date_to_jd(dt_arr_end.year, dt_arr_end.month, dt_arr_end.day)
        
        dep_jds = np.linspace(jd_dep_start, jd_dep_end, req.steps)
        arr_jds = np.linspace(jd_arr_start, jd_arr_end, req.steps)
        
        raw_data = generate_porkchop_data(dep_jds, arr_jds, destination=req.destination)
        
        # Convert numpy arrays to lists for JSON serialization, handling NaNs
        # Replace NaNs with None for JSON compatibility
        def clean_grid(grid):
            cleaned = np.where(np.isnan(grid), None, grid)
            return cleaned.tolist()
            
        return {
            "departure_jds": raw_data["departure_jds"].tolist(),
            "arrival_jds": raw_data["arrival_jds"].tolist(),
            "c3": clean_grid(raw_data["c3"]),
            "v_inf_arr": clean_grid(raw_data["v_inf_arr"]),
            "total_dv": clean_grid(raw_data["total_dv"])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/v1/simulations/run")
def run_orbit_simulation(req: SimulationRequest):
    """Run geocentric or heliocentric numerical propagation and return trajectory paths."""
    try:
        dest = req.destination.lower().strip()
        if dest == "moon":
            data = run_moon_simulation(req.launch_date, flight_days=req.flight_days)
        elif dest == "mars":
            data = run_mars_simulation(req.launch_date, flight_days=req.flight_days)
        elif dest in ["bennu", "psyche"]:
            data = run_asteroid_simulation(dest, req.launch_date, flight_days=req.flight_days)
        else:
            raise ValueError(f"Simulation destination '{req.destination}' not supported.")
            
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Presets for ease of testing
@app.get("/api/v1/presets/mars")
def mars_mission_preset():
    mission = {
        "origin": "Earth",
        "destination": "Mars",
        "spacecraft_mass": 2500,
        "propulsion_type": "Chemical",
        "payload_mass": 800,
        "launch_date": "2032-08-15"
    }
    engine = MissionEngine(mission)
    return engine.plan_mission()


@app.get("/api/v1/presets/moon")
def moon_mission_preset():
    mission = {
        "origin": "Earth",
        "destination": "Moon",
        "spacecraft_mass": 1500,
        "propulsion_type": "Chemical",
        "payload_mass": 500,
        "launch_date": "2031-06-01"
    }
    engine = MissionEngine(mission)
    return engine.plan_mission()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
