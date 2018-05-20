import numpy as np
import random
import bisect


class TSPACO:
    def __init__(self, distance_matrix, initialization_value, evaporation_rate, intensification_value, alpha=1., beta=1.,
                 ant_number=30, n_best_to_intensify=1, pher_min=None, pher_max=None):
        """ Initializes all needed parameters for the TSP-ACO """

        self.distance_matrix = np.asarray(distance_matrix)
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
        # never changes, so calculating once in the beginning saves time
        # divide, except where distance is 0, there the value of the "out" array stays
        self.heuristic_matrix = np.divide(1, self.distance_matrix, out=np.zeros_like(self.distance_matrix, dtype=float),
                                          where=self.distance_matrix != 0)
        self.pheromone_matrix = None
        self.initialize()

    def run(self, iterations=1):
        """ Runs the algorithm for the given number of iterations """
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
        """ Returns the length of the given solution """
        return sum(self.distance_matrix[solution[i], solution[(i + 1) % len(solution)]] for i in range(len(solution)))

    def initialize(self):
        """ Initializes the pheromone matrix with the initialization value"""
        self.pheromone_matrix = np.full_like(self.distance_matrix, self.initialization_value, dtype=float)

    def construct_solutions(self):
        """ Calculates a solution for every ant and returns them """

        # calculate weights for each city to go to any other city. It's not a probability because normalization
        # is omitted (the denominator of the equation), which means values are not between 0 and 1.
        # This saves time and more importantly means the values don't need to be recalculated every time
        # a column gets set to 0 when the corresponding city is not up for selection anymore.
        cite_weights = self.pheromone_matrix.copy()
        if self.alpha == 1 and self.beta == 1:
            cite_weights *= self.heuristic_matrix
        elif self.alpha != 1 or self.beta != 0:
            cite_weights = cite_weights ** self.alpha * self.heuristic_matrix ** self.beta

        # calculate path for each ant
        paths = np.zeros((self.ant_number, self.cities), dtype=int)
        for k in range(self.ant_number):
            cities_left = cite_weights.copy()
            # random starting city
            i = random.randrange(0, self.cities)
            paths[k, 0] = i
            # we want to do as little as possible in the innermost loop, so we make an array of random numbers now
            # instead of calling random every time inside, which generates a lof of overhead
            rands = np.random.rand(self.cities)
            for cnt in range(1, self.cities):
                # set "probability" to go from any city to current city to 0 since it can't go back there
                cities_left[:, i] = 0
                # to get a random number considering weights we calculate the cumulative sum of the weights, which
                # basically means we get ascending numbers, but the step size/difference to the lest entry differs,
                # corresponding to how likely this particular entry should be.
                # We then multiply a random number in [0, 1) by the upper limit of the cumulative sum and
                # find the point/index at which this number would be inserted to keep the cumulative sum ordered
                # (which is what bisect does), which then makes for a weighted random selection of a city
                cum_sum = np.cumsum(cities_left[i])
                i = bisect.bisect_left(cum_sum, cum_sum[-1] * rands[cnt])
                paths[k, cnt] = i
        return paths

    def evaporate(self):
        """ Evaporation by a fixed percentage """
        self.pheromone_matrix *= (1 - self.evaporation_rate)
        if self.pher_min is not None:
            self.pheromone_matrix[self.pheromone_matrix < self.pher_min] = self.pher_min

    def intensify(self, paths):
        """ Intensification by a fixed value """
        for path in paths:
            for i in range(self.cities):
                self.pheromone_matrix[path[i], path[(i + 1) % self.cities]] += self.intensification_value
        if self.pher_max is not None:
            self.pheromone_matrix[self.pheromone_matrix > self.pher_max] = self.pher_max
