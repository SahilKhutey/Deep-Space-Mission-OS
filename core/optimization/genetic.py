"""
Genetic Algorithm Optimizer for Trajectory Design
Finds optimal launch date and flight duration to minimize total delta-V.
"""

import numpy as np
from core.astrodynamics.lambert import lambert_solve
from core.trajectories.earth_mars import get_planet_state
from core.constants import MU_SUN, MU_EARTH, MU_MARS, R_EARTH, R_MARS, DAY_S


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
    Optimize launch window using a Genetic Algorithm.
    
    bounds: list of tuples [(min_jd, max_jd), (min_duration, max_duration)]
    """
    # 1. Initialize population
    pop = np.zeros((pop_size, 2))
    for dim in range(2):
        pop[:, dim] = np.random.uniform(bounds[dim][0], bounds[dim][1], size=pop_size)
        
    best_ind = None
    best_cost = 1e9
    history = []
    
    for gen in range(generations):
        # Evaluate fitness
        costs = np.array([fitness_function(ind, destination) for ind in pop])
        
        # Track best
        min_idx = np.argmin(costs)
        if costs[min_idx] < best_cost:
            best_cost = costs[min_idx]
            best_ind = pop[min_idx].copy()
            
        history.append(best_cost)
        
        # Selection: Tournament selection
        parents = []
        for _ in range(pop_size):
            cand_indices = np.random.choice(pop_size, size=3, replace=False)
            best_cand = cand_indices[np.argmin(costs[cand_indices])]
            parents.append(pop[best_cand].copy())
        parents = np.array(parents)
        
        # Crossover (Arithmetic Crossover)
        next_pop = []
        for i in range(0, pop_size, 2):
            p1, p2 = parents[i], parents[min(i+1, pop_size-1)]
            alpha = np.random.uniform(0.1, 0.9)
            c1 = alpha * p1 + (1 - alpha) * p2
            c2 = (1 - alpha) * p1 + alpha * p2
            next_pop.append(c1)
            next_pop.append(c2)
        next_pop = np.array(next_pop)[:pop_size]
        
        # Mutation (Gaussian perturbation)
        for i in range(pop_size):
            if np.random.rand() < mutation_rate:
                for dim in range(2):
                    sigma = (bounds[dim][1] - bounds[dim][0]) * 0.05
                    next_pop[i, dim] += np.random.normal(0, sigma)
                    # Clip to bounds
                    next_pop[i, dim] = np.clip(next_pop[i, dim], bounds[dim][0], bounds[dim][1])
                    
        # Elite preservation
        next_pop[0] = best_ind.copy()
        pop = next_pop
        
    return {
        "best_departure_jd": best_ind[0],
        "best_duration_days": best_ind[1],
        "best_arrival_jd": best_ind[0] + best_ind[1],
        "min_delta_v_km_s": best_cost,
        "history": history
    }
