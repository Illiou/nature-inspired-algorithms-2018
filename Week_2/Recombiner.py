from AbstractModules import AbstractRecombiner
import random

class KPointCrossover(AbstractRecombiner):

    def recombine(parents):
        k = 2
        crossover_points = [0]
        crossover_points.append(random.randint(0, k-1))

        children = []
        for i in range(1, len(crossover_points)):
            new_child = []
            for j in range(len(crossover_points+1)):
                parent = parents[j%len(parents)]
                new_child.append(parent[crossover_points[i-1]:crossover_points[i]])
            children.append(new_child)

        return children
