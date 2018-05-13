import numpy as np
import matplotlib.pyplot as plt
import random
import bisect


class TSPACO:
    def __init__(self, distance_matrix, initialization_value, evaporation_rate, intensification_value, alpha=1., beta=1.,
                 ant_number=100, n_best_to_intensify=1):
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

        self.heuristic_matrix = np.divide(1, self.distance_matrix, out=np.zeros_like(self.distance_matrix, dtype=float),
                                          where=self.distance_matrix != 0)
        self.pheromone_matrix = None
        self.initialize()

    def run(self, iterations=1):
        best_solution_distances = np.zeros(iterations)
        for i in range(iterations):
            # print(f"Iteration {i}")
            paths = self.construct_solutions()
            self.evaporate()
            path_qualities = np.argsort([self.objective_function(path) for path in paths])
            best_paths = paths[path_qualities[:self.n_best_to_intensify]]
            self.intensify(best_paths)
            best_solution_distances[i] = self.objective_function(best_paths[0])
        return best_solution_distances

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

    def intensify(self, paths):
        for path in paths:
            for i in range(self.cities):
                self.pheromone_matrix[path[i], path[(i + 1) % self.cities]] += self.intensification_value


if __name__ == "__main__":
    distances_file = "../TSP_Problems/problem_01.tsp"
    initial_pheromone_value = 1
    # evaporation_rate = 0.1
    intensification_value = 1
    iterations = 300
    repetitions = 5

    distance_matrix = np.loadtxt(distances_file)

    evaporation_tests = [0.01, 0.05, 0.1, 0.5, 1]
    aco = TSPACO(distance_matrix, initial_pheromone_value, 0, intensification_value, alpha=1, beta=1, ant_number=50)

    for evaporation_rate in evaporation_tests:
        print(f"Calculating for evaporation rate {evaporation_rate}")
        aco.evaporation_rate = evaporation_rate
        best_solution_distances = np.zeros((repetitions, iterations))
        for repetition in range(repetitions):
            print(f"Repetition {repetition}")
            aco.initialize()
            best_solution_distances[repetition] = aco.run(iterations)
        plt.plot(np.mean(best_solution_distances, axis=0), label=f"Evaporation rate: {evaporation_rate}")
    plt.legend()
    plt.show()
