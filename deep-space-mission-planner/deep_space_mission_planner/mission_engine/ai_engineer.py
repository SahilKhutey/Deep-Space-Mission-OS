"""
AI Mission Engineer and Genetic Trajectory Optimizer.
"""

import numpy as np
from deep_space_mission_planner.mission_engine.databases import LAUNCH_VEHICLES
from deep_space_mission_planner.mission_engine.risk_cost_engines import CostEstimationEngine

class AIMissionEngineer:
    def __init__(self):
        self.cost_engine = CostEstimationEngine()

    def select_optimal_vehicle(self, payload_mass_kg, destination):
        """
        Selects the most cost-effective launch vehicle that meets payload mass requirements.
        """
        best_vehicle = None
        min_cost = float("inf")
        
        # Determine capacity field based on destination
        capacity_field = "leo_kg"
        if destination == "Moon":
            capacity_field = "tli_kg"
        elif destination == "Mars":
            capacity_field = "tli_kg"
            
        for name, specs in LAUNCH_VEHICLES.items():
            if specs[capacity_field] >= payload_mass_kg:
                if specs["cost_usd"] < min_cost:
                    min_cost = specs["cost_usd"]
                    best_vehicle = name
                    
        if best_vehicle is None:
            raise ValueError("No launch vehicle found with sufficient capacity.")
            
        return {
            "optimal_launch_vehicle": best_vehicle,
            "cost_usd": min_cost
        }

class GeneticTrajectoryOptimizer:
    def __init__(self, population_size=20, generations=5, mutation_rate=0.1):
        self.pop_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate

    def optimize_orbit(self, target_mu, r_start, r_target):
        """
        Finds the semi-major axis (a) that minimizes total delta-V for transfer.
        Fitness function evaluates Hohmann transfer total delta-V.
        """
        # Initialize population around Hohmann value
        a_hohmann = (r_start + r_target) / 2.0
        rng = np.random.default_rng(42)
        population = rng.uniform(a_hohmann * 0.8, a_hohmann * 1.2, self.pop_size)
        
        def fitness(a):
            # Hohmann transfer equations:
            # We want to minimize total burn required:
            # dv1 = |sqrt(mu*(2/r_start - 1/a)) - sqrt(mu/r_start)|
            # dv2 = |sqrt(mu/r_target) - sqrt(mu*(2/r_target - 1/a))|
            try:
                if a <= r_start or a <= r_target:
                    return 1e9  # invalid orbit
                v_c1 = np.sqrt(target_mu / r_start)
                v_tx1 = np.sqrt(target_mu * (2.0 / r_start - 1.0 / a))
                dv1 = abs(v_tx1 - v_c1)
                
                v_c2 = np.sqrt(target_mu / r_target)
                v_tx2 = np.sqrt(target_mu * (2.0 / r_target - 1.0 / a))
                dv2 = abs(v_c2 - v_tx2)
                return dv1 + dv2
            except ValueError:
                return 1e9
                
        for gen in range(self.generations):
            # Evaluate fitness
            scores = np.array([fitness(ind) for ind in population])
            
            # Sort population (minimizing fitness)
            sorted_indices = np.argsort(scores)
            population = population[sorted_indices]
            
            # Selection: Keep top half
            parents = population[:self.pop_size // 2]
            
            # Crossover & Mutation to fill next generation
            next_generation = list(parents)
            while len(next_generation) < self.pop_size:
                p1, p2 = rng.choice(parents, 2, replace=False)
                child = 0.5 * (p1 + p2)
                # Mutation
                if rng.random() < self.mutation_rate:
                    child += rng.normal(0, a_hohmann * 0.05)
                next_generation.append(child)
                
            population = np.array(next_generation)
            
        best_idx = np.argmin([fitness(ind) for ind in population])
        return population[best_idx], fitness(population[best_idx])
