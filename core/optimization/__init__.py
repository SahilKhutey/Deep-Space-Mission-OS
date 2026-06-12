"""
Optimization Subsystem
Provides class-based Genetic Algorithm, Particle Swarm Optimization,
and Differential Evolution, along with backward-compatible helper functions.
"""

import numpy as np
from core.optimization.genetic.ga import GeneticAlgorithm
from core.optimization.pso.pso import PSO
from core.optimization.differential_evolution.de import DifferentialEvolution

# Re-use the existing fitness function logic for backward compatibility
from core.constants import MU_SUN, MU_EARTH, MU_MARS, R_EARTH, R_MARS, DAY_S
from core.astrodynamics.lambert.solver import lambert_solve
from core.trajectories.earth_mars import get_planet_state

def fitness_function(params, destination="mars"):
    """
    Compute total delta-V cost for a given [jd_departure, flight_duration_days].
    Lower delta-V is better.
    """
    jd_dep, flight_duration = params
    jd_arr = jd_dep + flight_duration
    dt_s = flight_duration * DAY_S
    
    if flight_duration <= 10.0:
        return 1e9  # Penalty
        
    try:
        rE, vE = get_planet_state("earth", jd_dep)
        rD, vD = get_planet_state(destination, jd_arr)
        
        # Solve Lambert
        v_trans1, v_trans2 = lambert_solve(rE, rD, dt_s, MU_SUN, prograde=True)
        
        v_inf_dep = np.linalg.norm(v_trans1 - vE)
        v_inf_arr = np.linalg.norm(v_trans2 - vD)
        
        # LEO and destination circular orbit details
        r_leo = R_EARTH + 300.0
        v_leo = np.sqrt(MU_EARTH / r_leo)
        
        if destination.lower() == "mars":
            mu_dest = MU_MARS
            r_dest_orbit = R_MARS + 300.0
            v_dest_orbit = np.sqrt(MU_MARS / r_dest_orbit)
        else:
            mu_dest = MU_MARS
            r_dest_orbit = R_MARS + 300.0
            v_dest_orbit = np.sqrt(MU_MARS / r_dest_orbit)
            
        dv_dep = np.sqrt(2.0 * MU_EARTH / r_leo + v_inf_dep**2) - v_leo
        dv_arr = np.sqrt(2.0 * mu_dest / r_dest_orbit + v_inf_arr**2) - v_dest_orbit
        
        total_dv = dv_dep + dv_arr
        
        if np.isnan(total_dv):
            return 1e9
            
        return total_dv
    except Exception:
        return 1e9

def optimize_trajectory_ga(bounds, pop_size=40, generations=50, mutation_rate=0.15, destination="mars"):
    """
    Function-based wrapper for GA optimization, matching the old API.
    """
    cost_fn = lambda x: fitness_function(x, destination=destination)
    ga = GeneticAlgorithm(
        cost_fn=cost_fn,
        bounds=bounds,
        pop_size=pop_size,
        n_gen=generations,
        mutation_rate=mutation_rate,
        crossover_rate=0.8
    )
    best_ind, best_cost = ga.optimize()
    return {
        "best_departure_jd": best_ind[0],
        "best_duration_days": best_ind[1],
        "best_arrival_jd": best_ind[0] + best_ind[1],
        "min_delta_v_km_s": best_cost,
        "history": ga.history
    }

def optimize_trajectory_pso(bounds, num_particles=30, iterations=50, destination="mars"):
    """
    Function-based wrapper for PSO optimization, matching the old API.
    """
    cost_fn = lambda x: fitness_function(x, destination=destination)
    pso = PSO(
        cost_fn=cost_fn,
        bounds=bounds,
        n_particles=num_particles,
        n_iter=iterations,
        w=0.5,
        c1=1.5,
        c2=1.5
    )
    best_ind, best_cost = pso.optimize()
    return {
        "best_departure_jd": best_ind[0],
        "best_duration_days": best_ind[1],
        "best_arrival_jd": best_ind[0] + best_ind[1],
        "min_delta_v_km_s": best_cost,
        "history": pso.history
    }

def optimize_trajectory_de(bounds, pop_size=30, generations=50, F=0.6, CR=0.7, destination="mars"):
    """
    Function-based wrapper for DE optimization, matching the old API.
    """
    cost_fn = lambda x: fitness_function(x, destination=destination)
    de = DifferentialEvolution(
        cost_fn=cost_fn,
        bounds=bounds,
        pop_size=pop_size,
        n_gen=generations,
        F=F,
        CR=CR
    )
    best_ind, best_cost = de.optimize()
    return {
        "best_departure_jd": best_ind[0],
        "best_duration_days": best_ind[1],
        "best_arrival_jd": best_ind[0] + best_ind[1],
        "min_delta_v_km_s": best_cost,
        "history": de.history
    }

__all__ = [
    "GeneticAlgorithm",
    "PSO",
    "DifferentialEvolution",
    "fitness_function",
    "optimize_trajectory_ga",
    "optimize_trajectory_pso",
    "optimize_trajectory_de"
]
