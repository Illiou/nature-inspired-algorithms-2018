import numpy as np
from itertools import combinations


# Set weight limit of the knapsack
weight_limit = 100
# Set items as tupels of the form (weight,value)
items = [(40,20), (40,20), (25,10), (25,10), (25,10), (25,10), (15,5), (15,5),
        (15,5), (15,5), (15,5), (15,5)]


def swap_neighbourhood(assignment):
    neighbours = []
    for i in range(len(assignment)):
        new_neighbour = assignment.copy()
        new_neighbour[i] = assignment[(i+1)%12]
        new_neighbour[(i+1)%12] = assignment[i]
        neighbours.append(new_neighbour)

    return neighbours


def transposition_neighbourhood(assignment):
    neighbours = []
    for i,j in combinations(range(len(assignment)), 2):
        new_neighbour = assignment.copy()
        new_neighbour[i] = assignment[(i+j)%len(assignment)]
        new_neighbour[(i+j)%len(assignment)] = assignment[i]
        neighbours.append(new_neighbour)

    return neighbours


def weight_value(assignment):
    selected_items_index = np.where(assignment == 1)[0]
    selected_items = [items[index] for index in selected_items_index]
    weight = np.sum([item[0] for item in selected_items])
    value = np.sum([item[1] for item in selected_items])

    return (weight,value)


def feasible(neighbours):
    feasible_neighbours = [neighbour for neighbour in neighbours if weight_value(neighbour)[0] <= weight_limit]

    return feasible_neighbours


def hill_climbing():
    not_feasible = True
    while not_feasible:
        assignment = np.random.choice([0, 1], size=(12,))
        if weight_value(assignment)[0] <= weight_limit:
            not_feasible = False

    while True:
        neighbours = feasible(swap_neighbourhood(assignment))
        #neighbours = feasible(transposition_neighbourhood(assignment))

        values = []
        for neighbour in neighbours:
            values.append(weight_value(neighbour)[1])

        if len(values) > 0:
            if np.max(values) > weight_value(assignment)[1]:
                max_value_neighbour = neighbours[np.argmax(values)]
                assignment = max_value_neighbour
            else:
                return assignment, weight_value(assignment)
        else:
            return assignment, weight_value(assignment)


def first_choice_hill_climbing():
    not_feasible = True
    while not_feasible:
        assignment = np.random.choice([0, 1], size=(12,))
        if weight_value(assignment)[0] <= weight_limit:
            not_feasible = False

    while True:
        old_assingment = assignment.copy()
        neighbours = feasible(swap_neighbourhood(assignment))
        #neighbours = feasible(transposition_neighbourhood(assignment))

        for neighbour in neighbours:
            if weight_value(neighbour)[1] > weight_value(assignment)[1]:
                assignment = neighbour
                break

        if (old_assingment == assignment).all():
            return assignment, weight_value(assignment)


print(first_choice_hill_climbing())
