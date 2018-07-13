import numpy as np
import matplotlib.pyplot as plt
from Final.TSPACO import TSPACO


# loading problem
problem_number = 1
distances_file = f"Vehicle_Routing_Problems/VRP{problem_number}/distance.txt"
distance_matrix = np.loadtxt(distances_file)

# default values
initialization_value = 5
evaporation_rate = 0.02
intensification_value = 0.6
iterations = 1200
repetitions = 1
alpha = 1
beta = 6
ant_number = 100
n_best_to_intensify = 3

aco = TSPACO(distance_matrix, initialization_value, evaporation_rate, intensification_value,
             alpha=alpha, beta=beta, ant_number=ant_number, n_best_to_intensify=n_best_to_intensify)

nicos = [0, 80000, 110000]
curr_fig, curr_ax = plt.subplots()
best_paths_lengths = np.zeros((repetitions, iterations))

for repetition in range(repetitions):
    print(f"Repetition {repetition}")
    aco.initialize()
    _, best_paths_lengths[repetition] = aco.run(iterations)

print(best_paths_lengths)
curr_ax.plot(np.mean(best_paths_lengths, axis=0), label="Our ACO")
curr_ax.axhline(nicos[problem_number], linestyle="dashed", label="Benchmark")
curr_ax.set(title=f"Problem {problem_number}", xlabel="Generations", ylabel="Best path length")
curr_ax.legend()
plt.show()
