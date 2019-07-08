import numpy as np


class Solution:

    def __init__(self, tsp_solutions, solution_lengths):
        """

        Args:
            tsp_solutions: 2D List of customer permutation per vehicle.
            Empty list if no customer is visited (eg. [[1,4,20,5,2], [3,6,0], [7,9], [], []])
            solution_lengths: 1D ndArray of path length per vehicle in tsp solution.
            0 if no customer visited (eg. [123, 23, 4, 0, 0])
        """
        self.tsp_solutions = tsp_solutions
        self.solution_lengths = solution_lengths
        self.cost = None

    def __repr__(self):
        customer_per_vehicle = [len(x) - 1 for x in self.tsp_solutions]
        string = ""
        for i, vehicle in enumerate(customer_per_vehicle):
            string += "\tV{}:\t{}".format(i, vehicle)
        return string + "\nSolution cost:{}".format(self.cost)
