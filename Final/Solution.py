import numpy as np

class Solution:

    def __init__(self, transportation_costs, vehicle_assignment, tsp_solutions, solution_lengths):
        """

        Args:
            transportation_costs: 1D ndArray of costs per vehicle (eg. [12, 32, 34, 5, 45])
            vehicle_assignment: 2D ndArray of assignments of vehicles to customers [[0. 0. 0. 0. 0.], [1. 0. 0. 0. 1.],...]]
            tsp_solutions: 2D List of customer permutation per vehicle. Empty list if no customer is visited (eg. [[1,4,20,5,2], [3,6,0], [7,9], [], []])
            solution_lengths: 1D ndArray of path length per vehicle in tsp solution. 0 if no customer visited (eg. [123, 23, 4, 0, 0])
        """

        self.transportation_costs = transportation_costs
        #self.vehicle_assignment = vehicle_assignment necessary?
        self.tsp_solutions = tsp_solutions
        self.solution_lengths = solution_lengths
        self.cost = self.objective_function()

    def objective_function(self):
        return np.dot(self.transportation_costs, self.solution_lengths)

    def __repr__(self):
        customer_per_vehicle = [len(x) for x in self.tsp_solutions]
        string = ""
        for i, vehicle in enumerate(customer_per_vehicle):
            string += "V{}:\t{}".format(i, vehicle)
        return string + "Solution cost:{}".format(self.cost)
