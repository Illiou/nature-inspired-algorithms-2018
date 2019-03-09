import random
from copy import copy
from nia.Week_2.AbstractModules import AbstractRecombiner


class KPointCrossover(AbstractRecombiner):
    def __init__(self, parent_count, crossover_probability, crossover_point_count):
        """
        Args:
            crossover_point_count: the number of crossover-points
        """
        super().__init__(parent_count, crossover_probability)
        self.k = crossover_point_count

    def recombine(self, parents):
        """Recombines the given parents to get offspring using the k-crossover method"""
        if random.random() > self.crossover_probability:
            return [copy(parent) for parent in parents]
        chromosome_length = len(parents[0].chromosome)
        crossover_points = [0] + [random.randint(1, chromosome_length) for _ in range(self.k)] + [chromosome_length]
        crossover_points.sort()

        children = []
        for i in range(len(parents)):
            new_child = []
            for j in range(self.k + 1):
                parent = parents[(i + j) % len(parents)]
                new_child.extend(parent.chromosome[crossover_points[j]:crossover_points[j + 1]])
            problem = parents[0].problem
            children.append(problem.create_individual(new_child))

        return children


class UniformScanCrossover(AbstractRecombiner):

    def recombine(self, parents):
        """Recombines the given parents to get offspring sing the Uniform-scan-crossover method"""
        if random.random() > self.crossover_probability:
            return [copy(parent) for parent in parents]
        chromosomes = [parent.chromosome for parent in parents]
        possibilities = [*zip(*chromosomes)]

        children = []
        for i in range(len(parents)):
            new_child = [random.choice(possible) for possible in possibilities]
            problem = parents[0].problem
            children.append(problem.create_individual(new_child))

        return children
