"""
Differential Evolution (DE) Optimizer
A class-based, reusable Differential Evolution solver.
"""

import numpy as np

class DifferentialEvolution:
    """
    Differential Evolution optimizer using the DE/rand/1/bin strategy.
    """
    
    def __init__(self, cost_fn, bounds, pop_size=30, n_gen=50,
                 F=0.6, CR=0.7, seed=42):
        """
        Parameters
        ----------
        cost_fn  : callable - Objective function to minimize: cost = cost_fn(x)
        bounds   : list of tuples - Search space boundaries [(min_1, max_1), (min_2, max_2), ...]
        pop_size : int - Number of individuals in the population
        n_gen    : int - Number of evolution generations
        F        : float - Mutation scaling factor [0.0, 2.0]
        CR       : float - Crossover probability [0.0, 1.0]
        seed     : int - Random seed for reproducibility
        """
        self.cost_fn = cost_fn
        self.bounds = np.array(bounds, dtype=float)
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.F = F
        self.CR = CR
        self.rng = np.random.default_rng(seed)
        self.dim = len(bounds)
        self.history = []
        
    def optimize(self):
        """
        Runs the DE optimization process.
        Returns:
            best_ind : numpy array - The best solution vector found
            best_cost: float - The minimum cost value found
        """
        # Initialize population
        pop = self.rng.uniform(
            self.bounds[:, 0], self.bounds[:, 1],
            size=(self.pop_size, self.dim)
        )
        
        costs = np.array([self.cost_fn(ind) for ind in pop])
        
        best_idx = np.argmin(costs)
        best_ind = pop[best_idx].copy()
        best_cost = costs[best_idx]
        
        self.history = [best_cost]
        
        for gen in range(self.n_gen):
            for i in range(self.pop_size):
                # Select three distinct random candidates different from i
                candidates = [idx for idx in range(self.pop_size) if idx != i]
                r1, r2, r3 = self.rng.choice(candidates, size=3, replace=False)
                
                # Mutation: mutant = x_r1 + F * (x_r2 - x_r3)
                mutant = pop[r1] + self.F * (pop[r2] - pop[r3])
                
                # Clip mutant to search bounds
                mutant = np.clip(mutant, self.bounds[:, 0], self.bounds[:, 1])
                
                # Crossover
                trial = np.zeros(self.dim)
                cross_idx = self.rng.integers(0, self.dim)
                for d in range(self.dim):
                    if self.rng.random() < self.CR or d == cross_idx:
                        trial[d] = mutant[d]
                    else:
                        trial[d] = pop[i, d]
                        
                # Selection
                trial_cost = self.cost_fn(trial)
                if trial_cost < costs[i]:
                    pop[i] = trial
                    costs[i] = trial_cost
                    
                    if trial_cost < best_cost:
                        best_cost = trial_cost
                        best_ind = trial.copy()
                        
            self.history.append(best_cost)
            
        return best_ind, best_cost
