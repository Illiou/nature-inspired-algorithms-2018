import random


class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value


class KnapsackProblem:
    def __init__(self, items, max_weight):
        self.items = items
        self.item_count = len(items)
        self.max_weight = max_weight

    def random_assignment(self):
        assignment = []
        while True:
            for i in range(self.item_count):
                assignment.append(random.randint(0, 1))
            if self.is_feasible(assignment):
                return assignment
            assignment = []

    def small_neighbourhood(self, assignment):
        if len(assignment) != self.item_count:
            raise AssertionError("assignment must match item_count")
        neighbourhood = []
        for i in range(self.item_count):
            neighbour = assignment.copy()
            neighbour[i] = int(not neighbour[i])
            if self.is_feasible(neighbour):
                neighbourhood.append(neighbour)
        return neighbourhood

    def large_neighbourhood(self, assignment):
        if len(assignment) != self.item_count:
            raise AssertionError("assignment must match item_count")
        neighbourhood = []
        for i in range(self.item_count):
            # Add neighbours with one bit toggled
            neighbour = assignment.copy()
            neighbour[i] = int(not neighbour[i])
            if self.is_feasible(neighbour):
                neighbourhood.append(neighbour)
            for j in range(i+1, self.item_count):
                new_neighbour = neighbour.copy()
                # Add neighbour with two bit toggled
                new_neighbour[j] = int(not new_neighbour[j])
                if self.is_feasible(new_neighbour):
                    neighbourhood.append(new_neighbour)
        return neighbourhood

    def value_for_assignment(self, assignment):
        if len(assignment) != self.item_count:
            raise AssertionError("assignment must match item_count")
        value = 0
        for index, item in enumerate(self.items):
            value += assignment[index] * item.value
        return value

    def weight_for_assignment(self, assignment):
        if len(assignment) != self.item_count:
            raise AssertionError("assignment must match item_count")
        weight = 0
        for index, item in enumerate(self.items):
            weight += assignment[index] * item.weight
        return weight

    def is_feasible(self, assignment):
        return self.weight_for_assignment(assignment) <= self.max_weight

    def assignment_to_value_weight_string(self, assignment):
        return "weight: {}, value {}".format(self.weight_for_assignment(assignment),
                                             self.value_for_assignment(assignment))
