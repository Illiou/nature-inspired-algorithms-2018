from VehicleRoutingClusterAlgorithm import *
from VehicleRoutingABC import *


def run_algorithm(algorithm, solution_file_base=None):
    solution = algorithm.run()
    print(f"Solution is {solution}")
    print(f"visited customers: {set([item for sublist in solution.tsp_solutions for item in sublist])}")
    csv_name = None
    json_name = None
    if solution_file_base is not None:
        csv_name = solution_file_base + ".tsv"
        json_name = solution_file_base + ".json"
    solution.save(csv_name, json_name)


def run_cluster_algo(problem):
    run_algorithm(VRPAlgorithm(problem), solution_file_base=f"./Solution files/solution_cluster_{problem.name}")


def run_abc_algo(problem):
    bee_count = 100
    abandoned_limit = 50
    swaps_per_truck = 1
    swap_probability = 0.5
    iterations = 1000
    capacities, transportation_costs = zip(*problem.vehicles)
    run_algorithm(VehicleRoutingABC(bee_count, abandoned_limit, problem.distances,
                                    list(transportation_costs), list(capacities), problem.demands,
                                    neighbourhood=SWAPANY, swaps_per_truck=swaps_per_truck,
                                    swap_probability=swap_probability, iterations=iterations),
                  solution_file_base=f"./Solution files/solution_abc_{problem.name}")


if __name__ == '__main__':
    problem_1 = load_problem(1)
    problem_2 = load_problem(2)

    run_abc_algo(problem_1)
    run_abc_algo(problem_2)
    run_cluster_algo(problem_1)
    run_cluster_algo(problem_2)
