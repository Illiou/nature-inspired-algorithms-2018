import numpy as np
import matplotlib.pyplot as plt
import random
import bisect


class TSPACO:
    def __init__(self, distance_matrix, initialization_value, evaporation_rate, intensification_value, alpha=1., beta=1.,
                 ant_number=30, n_best_to_intensify=1, pher_min=None, pher_max=None):
        if isinstance(distance_matrix, np.ndarray):
            self.distance_matrix = distance_matrix
        else:
            self.distance_matrix = np.array(distance_matrix)
        self.cities = self.distance_matrix.shape[0]
        self.initialization_value = initialization_value
        self.evaporation_rate = evaporation_rate
        self.intensification_value = intensification_value
        self.alpha = alpha
        self.beta = beta
        self.ant_number = ant_number
        self.n_best_to_intensify = n_best_to_intensify
        self.pher_min = pher_min
        self.pher_max = pher_max

        self.heuristic_matrix = np.divide(1, self.distance_matrix, out=np.zeros_like(self.distance_matrix, dtype=float),
                                          where=self.distance_matrix != 0)
        self.pheromone_matrix = None
        self.initialize()

    def run(self, iterations=1):
        best_paths_lengths = np.zeros(iterations)
        for i in range(iterations):
            # print(f"Iteration {i}")
            paths = self.construct_solutions()
            self.evaporate()
            path_qualities = np.argsort([self.objective_function(path) for path in paths])
            best_paths = paths[path_qualities[:self.n_best_to_intensify]]
            self.intensify(best_paths)
            best_paths_lengths[i] = self.objective_function(best_paths[0])
        return best_paths_lengths

    def objective_function(self, solution):
        return sum(self.distance_matrix[solution[i], solution[(i + 1) % len(solution)]] for i in range(len(solution)))

    def initialize(self):
        self.pheromone_matrix = np.full_like(self.distance_matrix, self.initialization_value, dtype=float)

    def construct_solutions(self):
        city_probabilities = self.pheromone_matrix.copy()
        if self.alpha == 1 and self.beta == 1:
            city_probabilities *= self.heuristic_matrix
        elif self.alpha != 1 or self.beta != 0:
            city_probabilities = city_probabilities ** self.alpha * self.heuristic_matrix ** self.beta
        paths = np.zeros((self.ant_number, self.cities), dtype=int)
        for k in range(self.ant_number):
            cities_left = city_probabilities.copy()
            i = random.randrange(0, self.cities)
            paths[k, 0] = i
            for cnt in range(1, self.cities):
                cities_left[:, i] = 0
                cum_sum = np.cumsum(cities_left[i])
                i = bisect.bisect_left(cum_sum, random.uniform(0, cum_sum[-1]))
                paths[k, cnt] = i
        return paths

    def evaporate(self):
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        if self.pher_min is not None:
            self.pheromone_matrix[self.pheromone_matrix < self.pher_min] = self.pher_min

    def intensify(self, paths):
        for path in paths:
            for i in range(self.cities):
                self.pheromone_matrix[path[i], path[(i + 1) % self.cities]] += self.intensification_value
        if self.pher_max is not None:
            self.pheromone_matrix[self.pheromone_matrix > self.pher_max] = self.pher_max


if __name__ == "__main__":
    # loading problem
    problem = 1
    distances_file = f"../TSP_Problems/problem_0{problem}.tsp"
    distance_matrix = np.loadtxt(distances_file)

    # default values
    initial_pheromone_value = 1
    evaporation_rate = 0.05
    intensification_value = 1
    iterations = 10
    repetitions = 1
    alpha = 1
    beta = 1
    ant_number = 30
    n_best_to_intensify = 1

    aco = TSPACO(distance_matrix, initial_pheromone_value, evaporation_rate, intensification_value,
                 alpha=alpha, beta=beta, ant_number=ant_number, n_best_to_intensify=n_best_to_intensify)

    tests = {"initialization_value": [0.1, 1, 10, 30],
             "evaporation_rate": [0.01, 0.05, 0.1, 0.5, 1],
             "intensification_value": [0.1, 0.5, 1, 2],
             "alpha": [0, 0.5, 1, 2, 4],
             "beta": [0, 0.5, 1, 2, 4],
             "ant_number": [1, 5, 15, 30, 100],
             "n_best_to_intensify": [1, 5, 10]}

    nicos_hc = [6376, 4315, 4508]
    nicos_aco = [3632, 2878, 2617]
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
            curr_ax.plot(np.mean(best_paths_lengths, axis=0), label=f"{test_name.capitalize().replace('_', ' ')}: {test_value}")
        setattr(aco, test_name, value_before_test)
        curr_ax.axhline(nicos_hc[problem], linestyle="dashed", label="HC Benchmark")
        curr_ax.axhline(nicos_aco[problem], linestyle="dotted", label="ACO Benchmark")
        curr_ax.set(title=f"Problem {problem}", xlabel="Generations", ylabel="Best path distance")
        curr_ax.legend()

    for fig in figures:
        fig.show()
