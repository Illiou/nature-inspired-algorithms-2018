from abc import *
import numpy as np
import random


class DifferentialEvolution(ABC):
    def __init__(self, population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds):

        if len(lower_bounds) != len(upper_bounds):
            raise ValueError("lower and upper bounds arrays need to have the same length")

        self.population_size = population_size
        self.scale_factor = scale_factor
        self.crossover_rate = crossover_rate
        self.lower_bounds = np.asarray(lower_bounds)
        self.upper_bounds = np.asarray(upper_bounds)
        self.chromosome_size = len(lower_bounds)

        self.population = None
        self.initialize()

    @abstractmethod
    def objective_function(self, solution):
        pass

    def run(self, generations=1):
        best_objective_fs = np.zeros(generations)
        for g in range(generations):
            donors = self.mutate()
            trials = self.crossover(donors)
            self.select(trials)
            best_objective_fs[g] = np.apply_along_axis(self.objective_function, 1, self.population).min()
        return best_objective_fs

    def initialize(self):
        rand_arr = np.random.rand(self.population_size, self.chromosome_size)
        self.population = self.lower_bounds + (self.upper_bounds - self.lower_bounds) * rand_arr

    def mutate(self):
        def unique_rands(upper, k, exclude):
            rands = exclude.copy()
            for _ in range(k):
                while True:
                    r = random.randrange(upper)
                    if r not in rands:
                        break
                rands.append(r)
            bla = rands[len(exclude):]
            return bla

        donors = np.zeros_like(self.population)
        for i in range(self.population_size):
            x1, x2, x3 = unique_rands(self.population_size, 3, [i])
            donors[i] = self.population[x1] + self.scale_factor * (self.population[x2] - self.population[x3])
        return np.maximum(self.lower_bounds, donors)

    def crossover(self, donors):
        to_crossover = np.random.rand(self.population_size, self.chromosome_size) <= self.crossover_rate
        for i, j in enumerate(np.random.randint(self.chromosome_size, size=self.population_size)):
            to_crossover[i, j] = True
        return np.where(to_crossover, donors, self.population)

    def select(self, trials):
        trial_obj = np.apply_along_axis(self.objective_function, 1, trials)
        pop_obj = np.apply_along_axis(self.objective_function, 1, self.population)
        self.population = np.where((trial_obj <= pop_obj)[:, np.newaxis], trials, self.population)
