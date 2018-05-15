import numpy as np
import json

problem = 3
distances_file = f"../TSP_Problems/problem_0{problem}.tsp"
distance_matrix = np.loadtxt(distances_file)

n = distance_matrix.shape[0]
#n = 50

nodes = [{"id": i, "group": i / n} for i in range(n)]
links = []
for i in range(n):
    for j in range(i + 1, n):
        if distance_matrix[i, j] != 0:
            links.append({"source": i, "target": j, "value": distance_matrix[i, j] * 2.5})

data = {"nodes": nodes, "links": links}

with open("force_data.json", "w") as file:
    json.dump(data, file, indent=1)