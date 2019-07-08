import numpy as np
import matplotlib.pyplot as plt
from Final.TSPACO import TSPACO
import os


def run_aco(distance_matrix):
    """
    Run aco on the whole distance file
    Returns(ndarray): the length of the best paths in all repetitions
    """
    # parameters
    initialization_value = 5
    evaporation_rate = 0.02
    intensification_value = 0.6
    iterations = 1000
    repetitions = 4
    alpha = 1
    beta = 6
    ant_number = 100
    n_best_to_intensify = 3

    aco = TSPACO(distance_matrix, initialization_value, evaporation_rate, intensification_value,
                 alpha=alpha, beta=beta, ant_number=ant_number, n_best_to_intensify=n_best_to_intensify)
    best_paths_lengths = np.zeros((repetitions, iterations))
    for repetition in range(repetitions):
        print(f"Repetition {repetition}")
        aco.initialize()
        _, best_paths_lengths[repetition] = aco.run(iterations)

    return best_paths_lengths


def lower_bound_vs_benchmark(problem_number):
    """
    Plots the lowerbound of the problem calculated by assuming that the cheapest truck can go to every city
    against the benchmark
    Args:
        problem_number(int): the number of the problem
    Returns:

    """
    # loading problem
    problem_folder_path = os.path.join("Vehicle_Routing_Problems", f"VRP{problem_number}")
    distances_file = os.path.join(problem_folder_path, "distance.txt")
    distance_matrix = np.loadtxt(distances_file)
    best_paths_lengths = run_aco(distance_matrix)
    benchmark = int(np.loadtxt(os.path.join(problem_folder_path, "should_be_better_than_value.txt"), dtype=int))
    costs = np.loadtxt(os.path.join(problem_folder_path, "transportation_cost.txt"), dtype=int)
    curr_fig, curr_ax = plt.subplots()
    print(best_paths_lengths)
    curr_ax.plot(np.mean(best_paths_lengths, axis=0) * costs[0], label="lowerbound aco")
    curr_ax.axhline(benchmark, linestyle="dashed", label="Benchmark")
    curr_ax.set(title=f"Problem {problem_number}", xlabel="Generations", ylabel="Best path length")
    curr_ax.legend()
    plt.show()


if __name__ == '__main__':
    lower_bound_vs_benchmark(1)
    lower_bound_vs_benchmark(2)
