import numpy as np


class GeneticAlgorithm:
    def __init__(self, cost_fn, bounds, pop_size=50, n_gen=100,
                 crossover=0.7, mutation=0.2, seed=42):
        self.cost_fn = cost_fn
        self.bounds = np.array(bounds)
        self.pop_size = pop_size
        self.n_gen = n_gen
        self.crossover = crossover
        self.mutation = mutation
        self.rng = np.random.default_rng(seed)
        self.history = []

    def optimize(self):
        dim = len(self.bounds)
        pop = self.rng.uniform(self.bounds[:, 0], self.bounds[:, 1], (self.pop_size, dim))
        for _ in range(self.n_gen):
            fitness = np.array([self.cost_fn(x) for x in pop])
            self.history.append(fitness.min())
            idx = np.argmin(fitness)
            new = [pop[idx]]
            while len(new) < self.pop_size:
                i, j, k = self.rng.integers(0, self.pop_size, 3)
                p1 = pop[i] if fitness[i] < fitness[j] else pop[j]
                p2 = pop[k]
                if self.rng.random() < self.crossover:
                    alpha = self.rng.random()
                    child = alpha * p1 + (1.0 - alpha) * p2
                else:
                    child = p1.copy()
                for g in range(dim):
                    if self.rng.random() < self.mutation:
                        child[g] += self.rng.normal(0.0, 0.1) * (self.bounds[g, 1] - self.bounds[g, 0])
                new.append(np.clip(child, self.bounds[:, 0], self.bounds[:, 1]))
            pop = np.array(new)
        fitness = np.array([self.cost_fn(x) for x in pop])
        return pop[np.argmin(fitness)], fitness.min()
