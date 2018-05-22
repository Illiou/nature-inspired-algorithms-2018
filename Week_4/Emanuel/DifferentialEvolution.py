from abc import *
import numpy as np


class DifferentialEvolution(ABC):
    def __init__(self, population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds):

        if population_size != len(lower_bounds) or population_size != len(upper_bounds):
            raise ValueError("lower and upper bound array needs to be of length equal to the population size")

        self.population_size = population_size
        self.scale_factor = scale_factor
        self.crossover_rate = crossover_rate
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds

        self.population = None
        self.initialize()

    def run(self, generations=1):
        pass

    @abstractmethod
    def objective_function(self):
        pass

    def initialize(self):
        self.population = self.lower_bounds + (self.upper_bounds - self.lower_bounds) * np.random.rand(self.population_size)

    def mutate(self):
        pass

    def crossover(self):
        pass

    def select(self):
        pass
