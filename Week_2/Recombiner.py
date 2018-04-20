from Week_2.AbstractModules import AbstractRecombiner
from Week_2.Problem import Individual
import random
from copy import deepcopy


class OnePointCrossoverRecombiner(AbstractRecombiner):
    def __init__(self, parent_count, crossover_probability):
        if parent_count != 2:
            raise AssertionError("Parent_count in OnePointCrossover must be 2")
        super().__init__(parent_count, crossover_probability)

    def recombine(self, parents):
        if len(parents) != self.parent_count:
            raise AssertionError("wrong number of parents")
        if random.random() >= self.crossover_probability:
            return deepcopy(parents)
        point = random.randint(1, len(parents[0].chromosome) - 1)
        child1 = parents[0].chromosome[:point] + parents[1].chromosome[point:]
        child2 = parents[1].chromosome[:point] + parents[0].chromosome[point:]
        return [Individual(parents[0].problem, child1), Individual(parents[0].problem, child2)]



