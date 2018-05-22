import numpy as np
import Week_4.Emanuel.DifferentialEvolution as DifferentialEvolution


class PowerPlantDE(DifferentialEvolution):
    def __init__(self, population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds):
        super().__init__(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds)

    def objective_fuction(self):
        pass

    def initialize(self):
        self.population = self.lower_bounds + (self.upper_bounds - self.lower_bounds) * np.random.rand(self.population_size)

