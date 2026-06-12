"""
Genetic Algorithm (GA) Optimizer
A class-based, reusable Genetic Algorithm for multi-dimensional optimization.
"""

import numpy as np

class GeneticAlgorithm:
    """
    Standard Genetic Algorithm with tournament selection, arithmetic crossover,
    and Gaussian mutation.
    """
    
    def __init__(self, cost_fn, bounds, pop_size=50, n_gen=100,
                 crossover_rate=0.8, mutation_rate=0.2, seed=42):
        """
        Parameters
        ----------
        cost_fn        : callable - Objective function to minimize: cost = cost_fn(x)
        bounds         : list of tuples - Search space boundaries [(min_1, max_1), (min_2, max_2), ...]
        pop_size       : int - Number of individuals in the population
        n_gen          : int - Number of generations
        crossover_rate : float - Crossover probability [0, 1]
        mutation_rate  : float - Mutation probability [0, 1]
        seed           : int - Random seed for reproducibility
        """
        self.cost_fn = cost_fn
        self.bounds = np.array(bounds, dtype=float)
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.rng = np.random.default_rng(seed)
        self.dim = len(bounds)
        self.history = []
        
    def _initialize_population(self):
        """Generates random initial population within the specified bounds."""
        pop = self.rng.uniform(
            self.bounds[:, 0], self.bounds[:, 1],
            size=(self.pop_size, self.dim)
        )
        return pop
        
    def _evaluate(self, pop):
        """Evaluates cost of each individual in the population."""
        return np.array([self.cost_fn(ind) for ind in pop])
        
    def _select_tournament(self, pop, costs, k=3):
        """Performs tournament selection to select a parent."""
        idx = self.rng.integers(0, self.pop_size, size=k)
        best_idx = idx[np.argmin(costs[idx])]
        return pop[best_idx].copy()
        
    def _crossover(self, parent1, parent2):
        """Performs arithmetic crossover between two parents."""
        if self.rng.random() < self.crossover_rate:
            alpha = self.rng.uniform(0.1, 0.9)
            child = alpha * parent1 + (1.0 - alpha) * parent2
            return child
        return parent1.copy()
        
    def _mutate(self, individual):
        """Performs Gaussian mutation on an individual."""
        mutated = individual.copy()
        for i in range(self.dim):
            if self.rng.random() < self.mutation_rate:
                sigma = (self.bounds[i, 1] - self.bounds[i, 0]) * 0.05
                mutated[i] += self.rng.normal(0, sigma)
                mutated[i] = np.clip(mutated[i], self.bounds[i, 0], self.bounds[i, 1])
        return mutated
        
    def optimize(self):
        """
        Runs the GA optimization process.
        Returns:
            best_ind : numpy array - The best solution vector found
            best_cost: float - The minimum cost value found
        """
        pop = self._initialize_population()
        best_ind = None
        best_cost = float("inf")
        self.history = []
        
        for gen in range(self.n_gen):
            costs = self._evaluate(pop)
            
            # Find current generation best
            min_idx = np.argmin(costs)
            if costs[min_idx] < best_cost:
                best_cost = costs[min_idx]
                best_ind = pop[min_idx].copy()
                
            self.history.append(best_cost)
            
            # Generate next generation
            new_pop = []
            
            # Elitism: keep the best individual
            new_pop.append(best_ind.copy())
            
            while len(new_pop) < self.pop_size:
                p1 = self._select_tournament(pop, costs)
                p2 = self._select_tournament(pop, costs)
                child = self._crossover(p1, p2)
                child = self._mutate(child)
                new_pop.append(child)
                
            pop = np.array(new_pop)[:self.pop_size]
            
        return best_ind, best_cost
