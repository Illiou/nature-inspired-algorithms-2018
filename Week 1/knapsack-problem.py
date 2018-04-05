import random

items = [(40, 20), (25, 10), (15, 5)]  # weight, value
weight_limit = 100

pattern = []  # weight, value


def gen_pattern():
    for i in items:
        curr_pos = len(pattern)
        while sum(x[0] for x in pattern[curr_pos:]) <= weight_limit:
            pattern.append(i)
        if pattern[-1] == i:
            pattern.pop()


def assignment_value(assignment):
    return sum(pattern[i][1] * a for i, a in enumerate(assignment))


def assignment_weight(assignment):
    return sum(pattern[i][0] * a for i, a in enumerate(assignment))


def satisfies_constraints(assignment):
    return assignment_weight(assignment) <= weight_limit


def small_neighborhood(assignment):
    neighbors = []
    for i in range(len(assignment)):
        new_assignment = assignment.copy()
        new_assignment[i] ^= 1  # toggle variable
        if satisfies_constraints(new_assignment):
            neighbors.append(new_assignment)
    return neighbors


def large_neighborhood(assignment):
    neighbors = []
    for i in range(len(assignment)):
        new_assignment = assignment.copy()
        new_assignment[i] ^= 1  # toggle variable
        if satisfies_constraints(new_assignment):
            neighbors.append(new_assignment)
        for j in range(i + 1, len(assignment)):
            newer_assignment = new_assignment.copy()
            newer_assignment[j] ^= 1  # toggle variable
            if satisfies_constraints(newer_assignment):
                neighbors.append(newer_assignment)
    return neighbors


def hill_climbing(assignment=None, neighborhood_func=small_neighborhood):
    if assignment is None:
        assignment = [random.choice([0, 1]) for _ in pattern]
    while True:
        print(assignment)
        max_neighbor = max((a for a in neighborhood_func(assignment)), key=lambda x: assignment_value(x))
        if assignment_value(max_neighbor) > assignment_value(assignment):
            assignment = max_neighbor
        else:
            return assignment


def first_choice_hill_climbing(assignment=None, neighborhood_func=small_neighborhood):
    if assignment is None:
        assignment = [random.choice([0, 1]) for _ in pattern]
    while True:
        unchanged = True
        for n in neighborhood_func(assignment):
            if assignment_value(n) > assignment_value(assignment):
                unchanged = False
                assignment = n
                break
        if unchanged:
            return assignment


gen_pattern()
print(pattern)
#print(large_neighborhood([0,0,0,0,0,0,0,0,0,0,0,0]))
print(assignment_weight(hill_climbing([1,1,1,0,0,0,0,0,0,0,0,0], neighborhood_func=large_neighborhood)))
