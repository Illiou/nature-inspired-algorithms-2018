import numpy as np
import matplotlib.pyplot as plt


class TSPACO:
    def __init__(self, city_distances):
        """
        Creates an TSP-ACO with the given cities
        Args:
            city_distances(ndarray): two dimensional list with all cities and their distances to each other
        """
        self.pheromone_info = None
        self.city_distances = city_distances
        self.heuristics = np.divide(1, self.city_distances,
                                    out=np.zeros_like(self.city_distances), where=self.city_distances!=0)
        self.current_solutions = None
        self.current_best_solution = None
        self.current_shortest_distance = None

    def initialize(self, init_value):
        if self.pheromone_info is not None:
            raise AssertionError("Already initialized")
        self.pheromone_info = np.full_like(self.city_distances, init_value)

    def construct_solutions(self, ant_count, pheromone_influence=1.0, heuristic_influence=1.0):
        self.current_solutions = []
        for ant in range(ant_count):
            city_count = np.size(self.city_distances, axis=0)
            selectable_cities = set(range(1, city_count))
            current_position = 0
            solution = [current_position]
            while len(selectable_cities) > 0:
                is_selectable_mask = np.array([city in selectable_cities for city in range(city_count)])
                probabilities = np.power(self.pheromone_info[current_position], pheromone_influence) \
                                * np.power(self.heuristics[current_position], heuristic_influence) \
                                * is_selectable_mask
                # divide by the total sum of each row to get real probabilities
                probabilities = probabilities / np.sum(probabilities)
                selected_city = np.random.choice(city_count, p=probabilities)
                current_position = selected_city
                solution.append(selected_city)
                selectable_cities.remove(selected_city)
            self.current_solutions.append(solution)
        distances = [self.distance_for_solution(solution) for solution in self.current_solutions]
        index_of_best = int(np.argmin(distances))
        self.current_best_solution = self.current_solutions[index_of_best]
        self.current_shortest_distance = distances[index_of_best]

    def distance_for_solution(self, solution):
        distance = 0
        for i, current_city in enumerate(solution[:-1]):
            next_city = solution[i+1]
            distance += self.city_distances[current_city][next_city]
        return distance

    def evaporate(self, evaporation_factor):
        self.pheromone_info = self.pheromone_info * (1 - evaporation_factor)

    def intensify(self, intensification_value):
        for i, current_city in enumerate(self.current_best_solution[:-1]):
            next_city = self.current_best_solution[i+1]
            self.pheromone_info[current_city][next_city] += intensification_value


def load_tsp(filename):
    with open(filename) as file:
        return np.loadtxt(filename)


if __name__ == '__main__':
    city_differences = load_tsp("../TSP_Problems/problem_01.tsp")
    assert(city_differences[4][10] == city_differences[10][4])
    tsp_aco = TSPACO(city_differences)
    tsp_aco.initialize(1)

    iteration_count = 10
    step_count = 300

    for evaporation_factor in [0.05]:  # [0.01, 0.05, 0.1, 0.5, 1]:
        best_values = np.zeros((iteration_count, step_count))
        for i in range(iteration_count):
            tsp_aco = TSPACO(city_differences)
            tsp_aco.initialize(1)
            for j in range(step_count):
                tsp_aco.construct_solutions(15)
                tsp_aco.evaporate(evaporation_factor)
                tsp_aco.intensify(0.1)
                best_values[i][j] = tsp_aco.current_shortest_distance
                print("step:", j+1)
            print("done iterations:", i+1)
        plt.plot(np.mean(best_values, axis=0), label="evap-factor: {}".format(evaporation_factor))
        print("done evaporation_factor:", evaporation_factor)
    plt.legend()
    plt.show()

