import numpy as np


class PSO:
    def __init__(self, cost_fn, bounds, n_particles=30, n_iter=100,
                 w=0.7, c1=1.5, c2=1.5, seed=42):
        self.cost_fn = cost_fn
        self.bounds = np.array(bounds)
        self.n = n_particles
        self.n_iter = n_iter
        self.w, self.c1, self.c2 = w, c1, c2
        self.rng = np.random.default_rng(seed)
        self.history = []

    def optimize(self):
        dim = len(self.bounds)
        pos = self.rng.uniform(self.bounds[:, 0], self.bounds[:, 1], (self.n, dim))
        vel = self.rng.uniform(-1.0, 1.0, (self.n, dim))
        pbest = pos.copy()
        pbest_fit = np.array([self.cost_fn(x) for x in pos])
        gi = np.argmin(pbest_fit)
        gbest, gbest_fit = pbest[gi].copy(), pbest_fit[gi]
        for _ in range(self.n_iter):
            for i in range(self.n):
                r1, r2 = self.rng.random(dim), self.rng.random(dim)
                vel[i] = self.w*vel[i] + self.c1*r1*(pbest[i]-pos[i]) + self.c2*r2*(gbest-pos[i])
                pos[i] = np.clip(pos[i] + vel[i], self.bounds[:, 0], self.bounds[:, 1])
                f = self.cost_fn(pos[i])
                if f < pbest_fit[i]:
                    pbest[i], pbest_fit[i] = pos[i].copy(), f
                    if f < gbest_fit:
                        gbest, gbest_fit = pos[i].copy(), f
            self.history.append(gbest_fit)
        return gbest, gbest_fit
