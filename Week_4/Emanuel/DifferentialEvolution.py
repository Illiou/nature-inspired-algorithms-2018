from abc import *
import numpy as np


class DifferentialEvolution(ABC):
    def __init__(self, population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds):

        if len(lower_bounds) != len(upper_bounds):
            raise ValueError("lower and upper bounds arrays need to have the same length")

        self.population_size = population_size
        self.scale_factor = scale_factor
        self.crossover_rate = crossover_rate
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds

        self.population = None
        self.initialize()

    @abstractmethod
    def objective_function(self):
        pass

    def run(self, generations=1):
        pass

    def initialize(self):
        rand_arr = np.random.rand((self.population_size, len(self.upper_bounds)))
        self.population = self.lower_bounds + (self.upper_bounds - self.lower_bounds) * rand_arr

    def mutate(self):
        pass

    def crossover(self):
        pass

    def select(self):
        pass
