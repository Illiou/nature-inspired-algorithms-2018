import random
import time

import matplotlib.pyplot as plt
from KnapsackProblem import KnapsackProblem, Item


def current_milli_time():
    return int(round(time.time() * 1000))


def random_knapsack(item_count, max_item_weight, max_item_value):
    items = []
    for i in range(item_count):
        random_weight = random.randint(1, max_item_weight)
        random_value = random.randint(1, max_item_value)
        items.append(Item(random_weight, random_value))
    max_weight = random.randint(max_item_weight * (int(item_count / 10) + 1),
                                max_item_weight * (int(item_count / 3) + 1))
    return KnapsackProblem(items, max_weight)


class Optimisation:
    def __init__(self, knapsack, use_large, use_first_choice):
        self.knapsack = knapsack
        self.use_large = use_large
        self.use_first_choice = use_first_choice

    def improving_neighbour(self, assignment):
        neighbourhood = self.knapsack.large_neighbourhood(assignment) if self.use_large \
            else self.knapsack.small_neighbourhood(assignment)
        current_value = self.knapsack.value_for_assignment(assignment)
        best_neighbour = None
        for neighbour in neighbourhood:
            new_value = self.knapsack.value_for_assignment(neighbour)
            if new_value > current_value:
                best_neighbour = neighbour
                if self.use_first_choice:
                    break
                else:
                    current_value = new_value
        return best_neighbour

    def run(self, initial_assignment):
        start_time = current_milli_time()
        assignment = initial_assignment
        iterations = 0
        while True:
            neighbour = self.improving_neighbour(assignment)
            iterations += 1
            if neighbour is None:
                end_time = current_milli_time()
                return iterations, end_time - start_time, assignment
            assignment = neighbour


def save_data_to_csv(use_large, use_first_choice, opened_file, needed_iterations, needed_time, achieved_value):
    time_per_iteration = needed_time / needed_iterations
    neighbourhood_string = "large" if use_large else "small"
    algorithm_string = "hillClimbing" if not use_first_choice else "firstChoice"
    total_string = "\t".join([neighbourhood_string, algorithm_string, str(needed_iterations),
                              str(needed_time), str(time_per_iteration), str(achieved_value)]) + "\n"
    opened_file.write(total_string)


def save_to_array(dict, needed_iterations, needed_time, achieved_value):
    # index according to order [hillClimbing small, firstChoice small, hC large, fC large]
    index = int(use_first_choice) + int(use_large) * 2
    time_per_iteration = needed_time / needed_iterations
    dict["iter"][index].append(needed_iterations)
    dict["time"][index].append(needed_time)
    dict["time_per_iter"][index].append(time_per_iteration)
    dict["value"][index].append(achieved_value)


def plot_all(key, name):
    for i, values in enumerate(dict[key]):
        plt.boxplot(values)
        neighbourhood_string = "large" if i > 1 else "small"
        algorithm_string = "hillClimbing" if i % 2 == 0 else "firstChoice"
        plt.title("{}: {}, {}".format(name, neighbourhood_string, algorithm_string))
        plt.show()


if __name__ == '__main__':
    runs = 100
    # for plotting
    dict = {"iter": [[], [], [], []], "time": [[], [], [], []], "time_per_iter": [[], [], [], []],
            "value": [[], [], [], []]}
    
    with open("./data/evaluation.csv", "w+") as file:
        knapsack = random_knapsack(10, 500, 5000)
        file.write("neighbourhood\talgorithm\titerations\ttime\ttimeperiteration\tvalue")
        for i in range(runs):
            print("start iteration", i + 1)
            initial_assignment = knapsack.random_assignment()
            file.write("\nRUN {}\n".format(i + 1))

            for use_large in [False, True]:
                for use_first_choice in [False, True]:
                    iteration, needed_time, assignment = Optimisation(knapsack, use_large, use_first_choice) \
                        .run(initial_assignment)
                    save_data_to_csv(use_large, use_first_choice, file, iteration,
                                     needed_time, knapsack.value_for_assignment(assignment))
                    save_to_array(dict, iteration,
                                  needed_time, knapsack.value_for_assignment(assignment))

    plot_all("iter", "Iterations")
    plot_all("time", "Time")
    plot_all("time_per_iter", "Time per Iteration")
    plot_all("value", "Values")
