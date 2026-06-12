"""
Differential Evolution (DE) Optimizer for Trajectory Design
Finds global minimum for transfer trajectories by mutating difference vectors.
"""

import numpy as np
from .genetic import fitness_function


def optimize_trajectory_de(bounds, pop_size=30, generations=50, F=0.6, CR=0.7, destination="mars"):
    """
    Optimize launch windows using Differential Evolution (DE/rand/1/bin).
    bounds: list of tuples [(min_jd, max_jd), (min_duration, max_duration)]
    """
    # 1. Initialize population
    pop = np.zeros((pop_size, 2))
    for dim in range(2):
        pop[:, dim] = np.random.uniform(bounds[dim][0], bounds[dim][1], size=pop_size)
        
    costs = np.array([fitness_function(ind, destination) for ind in pop])
    
    best_idx = np.argmin(costs)
    best_ind = pop[best_idx].copy()
    best_cost = costs[best_idx]
    
    history = [best_cost]
    
    for gen in range(generations):
        for i in range(pop_size):
            # 2. Mutation: select three random distinct candidates
            candidates = [idx for idx in range(pop_size) if idx != i]
            r1, r2, r3 = np.random.choice(candidates, size=3, replace=False)
            
            mutant = pop[r1] + F * (pop[r2] - pop[r3])
            
            # Force mutant inside boundary bounds
            for dim in range(2):
                mutant[dim] = np.clip(mutant[dim], bounds[dim][0], bounds[dim][1])
                
            # 3. Crossover
            trial = np.zeros(2)
            cross_index = np.random.randint(0, 2)
            for dim in range(2):
                if np.random.rand() < CR or dim == cross_index:
                    trial[dim] = mutant[dim]
                else:
                    trial[dim] = pop[i, dim]
                    
            # 4. Selection
            trial_cost = fitness_function(trial, destination)
            if trial_cost < costs[i]:
                pop[i] = trial
                costs[i] = trial_cost
                
                # Update global best
                if trial_cost < best_cost:
                    best_cost = trial_cost
                    best_ind = trial.copy()
                    
        history.append(best_cost)
        
    return {
        "best_departure_jd": best_ind[0],
        "best_duration_days": best_ind[1],
        "best_arrival_jd": best_ind[0] + best_ind[1],
        "min_delta_v_km_s": best_cost,
        "history": history
    }
