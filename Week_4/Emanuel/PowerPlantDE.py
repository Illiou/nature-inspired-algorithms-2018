import numpy as np
from Week_4.Emanuel.DifferentialEvolution import DifferentialEvolution


class PowerPlantDE(DifferentialEvolution):
    def __init__(self, population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds):
        super().__init__(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds)

    def objective_function(self):
        pass
