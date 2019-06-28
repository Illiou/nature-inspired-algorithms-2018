import numpy as np
import json

problem = 1
distances_file = f"../Vehicle_Routing_Problems/VRP{problem}/distance.txt"
distance_matrix = np.loadtxt(distances_file)

# direction differences
# compared = distance_matrix != distance_matrix.T
# print(np.dstack((distance_matrix[compared], distance_matrix.T[compared])))

n = distance_matrix.shape[0]
#n = 50

nodes = [{"id": i, "group": i / n} for i in range(n)]
links = []
for i in range(n):
    for j in range(i + 1, n):
        if distance_matrix[i, j] != 0:
            links.append({"source": i, "target": j, "value": (distance_matrix[i, j] + distance_matrix[j, i]) / 2 * 2.1})

data = {"nodes": nodes, "links": links}

with open("force_data.json", "w") as file:
    json.dump(data, file, indent=1)


# best solutions
# def objective_function(solution):
#     return sum(distance_matrix[solution[i], solution[(i + 1) % len(solution)]] for i in range(len(solution)))
#
# solutions_file = "best_solutions.csv"
# solutions = np.loadtxt(solutions_file, dtype=int, delimiter=",")
#
# path_qualities = [objective_function(path) for path in solutions]
# best_path = np.argmin(path_qualities)
# print(path_qualities[best_path])
# print(solutions[best_path])
