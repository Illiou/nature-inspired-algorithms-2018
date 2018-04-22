import random
from Week_2.Problem import Individual

from Week_2.AbstractModules import AbstractRecombiner


class KPointCrossover(AbstractRecombiner):
    def __init__(self, crossover_point_count, parent_count):
        super().__init__(parent_count)
        self.k = crossover_point_count

    def recombine(self, parents):
        chromosome_length = len(parents[0].chromosome)
        crossover_points = [0] + [random.randint(1, chromosome_length) for _ in range(self.k)] + [chromosome_length]
        crossover_points.sort()
        print(crossover_points)

        children = []
        for i in range(len(parents)):
            new_child = []
            for j in range(self.k + 1):
                parent = parents[(i + j) % len(parents)]
                new_child.extend(parent[crossover_points[j]:crossover_points[j + 1]])
            children.append(Individual(parents[0].problem, new_child))

        return children


class UniformScanCrossover(AbstractRecombiner):

    def recombine(self, parents):
        chromosomes = [parent.chromosome for parent in parents]
        possibilities = [*zip(*chromosomes)]
        print(possibilities)

        children = []
        for i in range(len(parents)):
            new_child = [random.choice(possible) for possible in possibilities]
            children.append(Individual(parents[0].problem, new_child))

        return children
