import numpy as np

class Solution:

    def __init__(self, transportation_costs, vehicle_assignment, tsp_solutions, solution_lengths):
        """

        Args:
            transportation_costs: 1D ndArray of costs per vehicle
            vehicle_assignment: 2D ndArray of assignments of vehicles to customers
            tsp_solutions: 2D List of customer permutation per vehicle. Empty list if no customer is visited
            solution_lengths: 1D ndArray of path length per vehicle in tsp solution. 0 if no customer visited
        """

        self.transportation_costs = transportation_costs
        self.vehicle_assignment = vehicle_assignment
        self.tsp_solutions = tsp_solutions
        self.solution_lengths = solution_lengths
        self.cost = self.objective_function()

    def objective_function(self):
        return np.dot(self.transportation_costs, self.solution_lengths)

    def __repr__(self):
        customer_per_vehicle = [len(x) for x in self.tsp_solutions]
        string = ""
        for i, vehicle in enumerate(customer_per_vehicle):
            string += f"V{i}:\t{vehicle}"
        return string + f"Solution cost:{self.cost}"
