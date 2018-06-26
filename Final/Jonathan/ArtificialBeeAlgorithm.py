from abc import *
import numpy as np
import matplotlib.pyplot as plt


class ArtificialBeeColony(ABC):
    def __init__(self, bee_count, abandoned_limit, lower_bounds, upper_bounds, minimization=False, store_best=True):
        if len(lower_bounds) != len(upper_bounds):
            raise ValueError("lower and upper bounds arrays need to have the same length")

        self.lower_bounds = np.asarray(lower_bounds)
        self.upper_bounds = np.asarray(upper_bounds)
        self.bee_count = bee_count
        self.abandoned_limit = abandoned_limit
        self.dimensions = self.lower_bounds.shape[0]
        self.minimization = minimization
        self.store_best = store_best

        self.solutions = None
        self.not_changed_count = np.zeros(self.bee_count)
        self.nectar = None
        self.initialize()

    @abstractmethod
    def objective_function(self, solutions):
        """
        Args:
            solutions(ndarray(ndarray(float))):  the solutions
        Returns:
            (ndarray(float)): the nectar values for the solutions
        """
        pass

    # noinspection PyTypeChecker
    def max_or_minimizing_objective_function(self, solutions):
        values = self.objective_function(solutions)
        if self.minimization:
            return np.where(values < 0, 1 + np.abs(values), 1/(1 + values))
        else:
            return values

    def initialize(self):
        self.solutions = self.random_solutions(self.bee_count)
        self.nectar = self.max_or_minimizing_objective_function(self.solutions)

    def random_solutions(self, count):
        rand_arr = np.random.rand(count, self.dimensions)
        return self.lower_bounds + (self.upper_bounds - self.lower_bounds) * rand_arr

    def employed_phase(self):
        new_solutions, new_nectar = self.generate_neighbours(self.solutions)
        should_change = self.nectar < new_nectar
        self.solutions = np.where(np.reshape(should_change, (-1, 1)), new_solutions, self.solutions)
        self.nectar = np.where(should_change, new_nectar, self.nectar)
        no_change_int = 1 - should_change.astype(int)
        self.not_changed_count = (self.not_changed_count + no_change_int) * no_change_int

    def generate_neighbours(self, solutions):
        """
        Generates a neighbour for every solution in solutions
        Args:
            solutions(ndarray): 2-d array of solutions
        Returns:
            (ndarray): the neighbours in same shape as solutions
        """
        ks = np.random.choice(self.bee_count - 1, self.bee_count)
        indices = np.arange(self.bee_count)
        ks = ks + (ks >= indices).astype(int)  # prevent from having k==i
        js = np.random.choice(self.dimensions, self.bee_count)
        js_one_hot = np.zeros((self.bee_count, self.dimensions))
        js_one_hot[np.arange(self.bee_count), js] = 1
        phis = (np.random.rand(self.bee_count) * 2) - 1  # random number between -1 and 1
        neighbours = solutions + np.reshape(phis, (-1, 1)) * (
                    solutions * js_one_hot - solutions[ks] * js_one_hot)
        # Set values out of bounds to bounds
        neighbours = np.where(neighbours >= np.repeat(self.lower_bounds[np.newaxis, :], [self.bee_count], axis=0),
                              neighbours, self.lower_bounds)
        neighbours = np.where(neighbours <= np.repeat(self.upper_bounds[np.newaxis, :], [self.bee_count], axis=0),
                              neighbours, self.upper_bounds)
        # print("ks", ks)
        # print("js", js)
        # print("jonehot", js_one_hot)
        # print("phis", phis)
        # print(self.solutions)
        # print(self.solutions[ks])
        # print(neighbours)
        neighbour_nectar = self.max_or_minimizing_objective_function(neighbours)
        return neighbours, neighbour_nectar

    def onlooker_phase(self):
        probabilities = self.nectar / np.sum(self.nectar)
        solution_choices = np.random.choice(self.bee_count, self.bee_count, p=probabilities)
        neighbours, neighbours_nectar = self.generate_neighbours(self.solutions[solution_choices])
        choices_unique = list(set(solution_choices))
        for choice in choices_unique:
            best_for_choice = np.argmax(np.hstack((np.where(solution_choices == choice, neighbours_nectar, 0), self.nectar[choice])))
            if best_for_choice != self.bee_count:  # the old solution was the best one
                self.solutions[choice] = neighbours[best_for_choice]
                self.nectar[choice] = neighbours_nectar[best_for_choice]
                self.not_changed_count[choice] = 0

    def scout_phase(self, best_index=None):
        limit_exceeded = self.not_changed_count >= self.abandoned_limit
        if any(limit_exceeded):
            for i, exceeded in enumerate(limit_exceeded):
                if exceeded and best_index != i:
                    new_solutions = self.random_solutions(1)
                    self.solutions[i] = new_solutions[0]
                    self.nectar[i] = self.max_or_minimizing_objective_function(new_solutions)[0]

    def run(self, iterations=100):
        best_nectar = np.zeros(iterations)
        best_index = -1
        for i in range(iterations):
            if i % 10 == 0:
                print("step", i)
            self.employed_phase()
            self.onlooker_phase()
            if self.store_best:
                self.scout_phase(best_index)
            else:
                self.scout_phase()
            # to not have the transformed nectar in minimization
            best_index = np.argmax(self.nectar)
            best_nectar[i] = self.objective_function(np.reshape(self.solutions[best_index], (1, -1)))[0]
        return best_nectar, self.solutions[best_index]


class ABCTest(ArtificialBeeColony):
    def objective_function(self, solutions):
        return np.sum(np.power(solutions, 2)-10*np.cos(2*np.pi*solutions)+10, axis=1)


if __name__ == '__main__':
    problem_num = 2
    dims = 5
    bee_count = 100
    iterations = 1000
    limit = 20

    best_nectar, best_solution = ABCTest(bee_count, limit, [-15]*dims, [15]*dims, minimization=True).run(iterations)

    curr_fig, curr_ax = plt.subplots()
    curr_ax.plot(best_nectar, label="Best nectar")
    # curr_ax.axhline(benchmark, linestyle="dashed", label="Benchmark")
    curr_ax.set(title=f"Problem {problem_num}", xlabel="iteration", ylabel="Best objective function")
    curr_ax.legend()
    plt.show()
