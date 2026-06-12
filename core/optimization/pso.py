"""
Particle Swarm Optimization (PSO) for Trajectory Optimization
Optimizes orbital transfer parameters to minimize mission delta-V.
"""

import numpy as np
from core.optimization.genetic import fitness_function


def optimize_trajectory_pso(bounds, num_particles=30, iterations=50, destination="mars"):
    """
    Optimize trajectory departure and duration bounds using Particle Swarm Optimization.
    
    bounds: list of tuples [(min_jd, max_jd), (min_duration, max_duration)]
    """
    w = 0.5   # Inertia weight
    c1 = 1.5  # Cognitive parameter
    c2 = 1.5  # Social parameter
    
    # Initialize particle positions and velocities
    pos = np.zeros((num_particles, 2))
    vel = np.zeros((num_particles, 2))
    
    for dim in range(2):
        pos[:, dim] = np.random.uniform(bounds[dim][0], bounds[dim][1], size=num_particles)
        # Velocity initialization (fraction of search range)
        span = bounds[dim][1] - bounds[dim][0]
        vel[:, dim] = np.random.uniform(-span * 0.1, span * 0.1, size=num_particles)
        
    pbest_pos = pos.copy()
    pbest_cost = np.array([fitness_function(p, destination) for p in pbest_pos])
    
    gbest_idx = np.argmin(pbest_cost)
    gbest_pos = pbest_pos[gbest_idx].copy()
    gbest_cost = pbest_cost[gbest_idx]
    
    history = [gbest_cost]
    
    for _ in range(iterations):
        for i in range(num_particles):
            r1, r2 = np.random.rand(), np.random.rand()
            
            # Update velocity
            vel[i] = w * vel[i] + \
                     c1 * r1 * (pbest_pos[i] - pos[i]) + \
                     c2 * r2 * (gbest_pos - pos[i])
                     
            # Update position
            pos[i] += vel[i]
            
            # Clip position to bounds
            for dim in range(2):
                pos[i, dim] = np.clip(pos[i, dim], bounds[dim][0], bounds[dim][1])
                
            # Evaluate cost
            cost = fitness_function(pos[i], destination)
            
            # Update personal best
            if cost < pbest_cost[i]:
                pbest_cost[i] = cost
                pbest_pos[i] = pos[i].copy()
                
                # Update global best
                if cost < gbest_cost:
                    gbest_cost = cost
                    gbest_pos = pos[i].copy()
                    
        history.append(gbest_cost)
        
    return {
        "best_departure_jd": gbest_pos[0],
        "best_duration_days": gbest_pos[1],
        "best_arrival_jd": gbest_pos[0] + gbest_pos[1],
        "min_delta_v_km_s": gbest_cost,
        "history": history
    }
