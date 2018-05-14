import numpy as np
import matplotlib.pyplot as plt
from TSPACO import TSPACO


# loading problem
problem = 1
distances_file = f"../TSP_Problems/problem_0{problem}.tsp"
distance_matrix = np.loadtxt(distances_file)

# default values
initialization_value = 5
evaporation_rate = 0.05
intensification_value = 0.5
iterations = 800
repetitions = 1
alpha = 1
beta = 4
ant_number = 50
n_best_to_intensify = 3

aco = TSPACO(distance_matrix, initialization_value, evaporation_rate, intensification_value,
             alpha=alpha, beta=beta, ant_number=ant_number, n_best_to_intensify=n_best_to_intensify)

nicos_hc = [0, 6376, 4315, 4508]
nicos_aco = [0, 3632, 2878, 2617]
curr_fig, curr_ax = plt.subplots()
best_paths_lengths = np.zeros((repetitions, iterations))

for repetition in range(repetitions):
    print(f"Repetition {repetition}")
    aco.initialize()
    best_paths_lengths[repetition] = aco.run(iterations)

curr_ax.plot(np.mean(best_paths_lengths, axis=0), label="Our ACO")
curr_ax.axhline(nicos_hc[problem], linestyle="dashed", label="HC Benchmark")
curr_ax.axhline(nicos_aco[problem], linestyle="dotted", label="ACO Benchmark")
curr_ax.set(title=f"Problem {problem}", xlabel="Generations", ylabel="Best path length")
curr_ax.legend()
curr_fig.show()