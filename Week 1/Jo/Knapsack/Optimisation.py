from Woche1.Jo.Knapsack.KnapsackProblem import KnapsackProblem, Item
import time
import random


def current_milli_time():
    return int(round(time.time() * 1000))


def random_knapsack(item_count, max_item_weight, max_item_value):
    items = []
    for i in range(item_count):
        random_weight = random.randint(1, max_item_weight)
        random_value = random.randint(1, max_item_value)
        items.append(Item(random_weight, random_value))
    max_weight = random.randint(max_item_weight * (int(item_count / 10) + 1), max_item_weight * (int(item_count / 3) + 1))
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


if __name__ == '__main__':
    knapsack = random_knapsack(100, 500, 5000)
    initial_assignment = knapsack.random_assignment()

    iteration, needed_time, assignment = Optimisation(knapsack, False, False).run(initial_assignment)
    time_per_iteration = needed_time / iteration
    print(iteration, needed_time, time_per_iteration, knapsack.assignment_to_value_weight_string(assignment))
    iteration, needed_time, assignment = Optimisation(knapsack, False, True).run(initial_assignment)
    time_per_iteration = needed_time / iteration
    print(iteration, needed_time, time_per_iteration, knapsack.assignment_to_value_weight_string(assignment))
    iteration, needed_time, assignment = Optimisation(knapsack, True, False).run(initial_assignment)
    time_per_iteration = needed_time / iteration
    print(iteration, needed_time, time_per_iteration, knapsack.assignment_to_value_weight_string(assignment))
    iteration, needed_time, assignment = Optimisation(knapsack, True, True).run(initial_assignment)
    time_per_iteration = needed_time / iteration
    print(iteration, needed_time, time_per_iteration, knapsack.assignment_to_value_weight_string(assignment))