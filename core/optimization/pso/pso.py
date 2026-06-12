"""
Particle Swarm Optimization (PSO)
A class-based, reusable Particle Swarm Optimizer for multi-dimensional optimization.
"""

import numpy as np

class PSO:
    """
    Standard Particle Swarm Optimization solver with cognitive and social updates.
    """
    
    def __init__(self, cost_fn, bounds, n_particles=30, n_iter=100,
                 w=0.5, c1=1.5, c2=1.5, seed=42):
        """
        Parameters
        ----------
        cost_fn     : callable - Objective function to minimize: cost = cost_fn(x)
        bounds      : list of tuples - Search space boundaries [(min_1, max_1), (min_2, max_2), ...]
        n_particles : int - Number of particles in the swarm
        n_iter      : int - Number of optimization iterations
        w           : float - Inertia weight
        c1          : float - Cognitive acceleration coefficient
        c2          : float - Social acceleration coefficient
        seed        : int - Random seed for reproducibility
        """
        self.cost_fn = cost_fn
        self.bounds = np.array(bounds, dtype=float)
        self.n_particles = n_particles
        self.n_iter = n_iter
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.rng = np.random.default_rng(seed)
        self.dim = len(bounds)
        self.history = []
        
    def optimize(self):
        """
        Runs the PSO optimization process.
        Returns:
            gbest_pos : numpy array - The global best position found
            gbest_cost: float - The minimum cost value found
        """
        # Initialize particle positions and velocities
        pos = self.rng.uniform(
            self.bounds[:, 0], self.bounds[:, 1],
            size=(self.n_particles, self.dim)
        )
        
        vel = np.zeros((self.n_particles, self.dim))
        for d in range(self.dim):
            span = self.bounds[d, 1] - self.bounds[d, 0]
            vel[:, d] = self.rng.uniform(-span * 0.1, span * 0.1, size=self.n_particles)
            
        pbest_pos = pos.copy()
        pbest_cost = np.array([self.cost_fn(p) for p in pos])
        
        gbest_idx = np.argmin(pbest_cost)
        gbest_pos = pbest_pos[gbest_idx].copy()
        gbest_cost = pbest_cost[gbest_idx]
        
        self.history = [gbest_cost]
        
        for it in range(self.n_iter):
            for i in range(self.n_particles):
                r1 = self.rng.random(self.dim)
                r2 = self.rng.random(self.dim)
                
                # Update velocity
                vel[i] = (self.w * vel[i] +
                          self.c1 * r1 * (pbest_pos[i] - pos[i]) +
                          self.c2 * r2 * (gbest_pos - pos[i]))
                          
                # Update position
                pos[i] += vel[i]
                
                # Enforce boundaries
                pos[i] = np.clip(pos[i], self.bounds[:, 0], self.bounds[:, 1])
                
                # Evaluate cost
                cost = self.cost_fn(pos[i])
                
                # Update personal best
                if cost < pbest_cost[i]:
                    pbest_cost[i] = cost
                    pbest_pos[i] = pos[i].copy()
                    
                    # Update global best
                    if cost < gbest_cost:
                        gbest_cost = cost
                        gbest_pos = pos[i].copy()
                        
            self.history.append(gbest_cost)
            
        return gbest_pos, gbest_cost
