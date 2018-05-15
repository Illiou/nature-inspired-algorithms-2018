import numpy as np
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
        # minimal and maximal values for pheromones which didn't turn out to be so great
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
            # calculate indices for best paths, then take N and intensify them
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
        # calculate value (not technically a probability) for each city to go to any other city, without normalization
        city_probabilities = self.pheromone_matrix.copy()
        if self.alpha == 1 and self.beta == 1:
            city_probabilities *= self.heuristic_matrix
        elif self.alpha != 1 or self.beta != 0:
            city_probabilities = city_probabilities ** self.alpha * self.heuristic_matrix ** self.beta
        # calculate path for each ant
        paths = np.zeros((self.ant_number, self.cities), dtype=int)
        for k in range(self.ant_number):
            cities_left = city_probabilities.copy()
            # random starting city
            i = random.randrange(0, self.cities)
            paths[k, 0] = i
            for cnt in range(1, self.cities):
                # set current city "probability" to 0 for all cities since it can't go back there
                cities_left[:, i] = 0
                # calculate cumulative sum for row of current city, then get random number of up to the total sum and
                # find point/index of it within cumulative sum, which is then the selected city
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
