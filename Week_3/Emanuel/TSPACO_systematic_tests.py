import numpy as np
import matplotlib.pyplot as plt
from TSPACO import TSPACO


# loading problem
problem = 1
distances_file = f"../TSP_Problems/problem_0{problem}.tsp"
distance_matrix = np.loadtxt(distances_file)

# default values
initialization_value = 1
evaporation_rate = 0.05
intensification_value = 1
iterations = 800
repetitions = 5
alpha = 1
beta = 1
ant_number = 30
n_best_to_intensify = 1

aco = TSPACO(distance_matrix, initialization_value, evaporation_rate, intensification_value,
             alpha=alpha, beta=beta, ant_number=ant_number, n_best_to_intensify=n_best_to_intensify)

tests = {"initialization_value": [0.1, 1, 5, 20],
         "evaporation_rate": [0.01, 0.02, 0.05, 0.1, 0.5, 1],
         "intensification_value": [0.1, 0.3, 0.6, 1, 3],
         "alpha": [0, 0.5, 1, 2, 4],
         "beta": [0, 0.5, 1, 2, 4, 6],
         "ant_number": [1, 5, 15, 30, 100],
         "n_best_to_intensify": [1, 3, 5, 10]}

nicos_hc = [0, 6376, 4315, 4508]
nicos_aco = [0, 3632, 2878, 2617]
figures = []

for test_name, test_values in tests.items():
    curr_fig, curr_ax = plt.subplots()
    figures.append(curr_fig)
    value_before_test = getattr(aco, test_name)
    for test_value in test_values:
        print(f"Calculating for {test_name}: {test_value}")
        setattr(aco, test_name, test_value)
        best_paths_lengths = np.zeros((repetitions, iterations))
        for repetition in range(repetitions):
            print(f"Repetition {repetition}")
            aco.initialize()
            best_paths_lengths[repetition] = aco.run(iterations)
        curr_ax.plot(np.mean(best_paths_lengths, axis=0),
                     label=f"{test_name.capitalize().replace('_', ' ')}: {test_value}")
    setattr(aco, test_name, value_before_test)
    curr_ax.axhline(nicos_hc[problem], linestyle="dashed", label="HC Benchmark")
    curr_ax.axhline(nicos_aco[problem], linestyle="dotted", label="ACO Benchmark")
    curr_ax.set(title=f"Problem {problem}", xlabel="Generations", ylabel="Best path length")
    curr_ax.legend()

for fig in figures:
    fig.show()
