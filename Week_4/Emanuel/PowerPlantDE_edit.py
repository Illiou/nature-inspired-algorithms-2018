import numpy as np
from Week_4.Emanuel.DifferentialEvolution_edit import DifferentialEvolution


class PowerPlantDE(DifferentialEvolution):
    def __init__(self, population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds,problem):
        super().__init__(population_size, scale_factor, crossover_rate, lower_bounds, upper_bounds,problem)

    def objective_function(self, solution):

        if np.any(solution[0:3] <= 0):
            return 0

        if np.any((solution[0:3] - np.array(self.problem["c"])*np.array(self.problem["k"])) > 0):
            return 9999999999999999999

        # revenue = what we produce * price
        revenue = np.sum(np.minimum(solution[4:7],self.problem["d"]) * np.array(self.problem["p"]))
        # Cost = Production cost + Purchasing cost
        prod_cost = np.sum(self.problem["c"]*np.ceil(solution[1:4]/self.problem["k"]))
        # Purchasing cost = max(sum(si)-sum(ei))*0.6
        purchasing_cost = np.sum(np.maximum(solution[3:6]-solution[0:3],np.zeros(solution[0:3].shape))*0.6)
        # fitness = revenue - cost
        return -(revenue - (prod_cost + purchasing_cost))
