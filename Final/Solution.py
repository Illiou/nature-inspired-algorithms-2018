import csv
import json
import numpy as np
from VehicleRoutingClusterAlgorithm import *


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

    def save(self, csv_filename=None, json_filename=None):
        if csv_filename is None and json_filename is None:
            csv_filename = f"./Solution files/solution_{self.cost}.tsv"
            json_filename = f"./Solution files/solution_{self.cost}.json"
        vehicle_zip_list = list(zip([f"vehicle_{i + 1}" for i, _ in enumerate(self.solution_lengths)],
                                    self.tsp_solutions, self.solution_lengths))
        if csv_filename is not None:
            with open(csv_filename, "w+") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow(["vehicles", "visited customers", "driven distance", "cost"])
                csv_writer.writerows(vehicle_zip_list)
                csv_writer.writerow([""] * 3 + [self.cost])
            print(f"Solution written to {csv_filename}")
        if json_filename is not None:
            json_dict = {}
            per_vehicle_key = "per_vehicle"
            per_attribute_key = "per_attribute"
            tsp_key = "visited_customers"
            length_key = "driven_distance"
            json_dict[per_vehicle_key] = {}
            json_dict[per_attribute_key] = {tsp_key: {}, length_key: {}}
            json_dict["cost"] = int(self.cost)
            for vehicle, tsp, length in vehicle_zip_list:
                if isinstance(tsp, np.ndarray):
                    tsp = tsp.tolist()
                json_dict[per_vehicle_key][vehicle] = {tsp_key: tsp, length_key: length}
                if length > 0:
                    json_dict[per_attribute_key][tsp_key][vehicle] = tsp
                    json_dict[per_attribute_key][length_key][vehicle] = length
            json_dumps = json.dumps(json_dict)
            with open(json_filename, "w+") as json_file:
                json_file.write(json_dumps)
            print(f"Solution written to {json_filename}")


def check_json_solution(problem, json_filename):
    with open(json_filename, "r") as json_file:
        json_dump = json.load(json_file)

    customers_to_visit = set(range(1, len(problem.demands)+1))
    visited_customers = set()
    for vehicle in json_dump["per_vehicle"].values():
        for c in vehicle["visited_customers"]:
            visited_customers.add(c)
    print(problem.demands)
    print(customers_to_visit)
    print(visited_customers)
    print(f"{len(customers_to_visit.difference(visited_customers))} customers not visited")


if __name__ == '__main__':
    problem = load_problem(1)
    check_json_solution(problem, "./Solution files/solution_cluster_problem_1.json")
