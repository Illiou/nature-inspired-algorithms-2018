from Week_2.AbstractModules import AbstractRecombiner
from Week_2.Problem import Individual
import random


class OnePointCrossoverRecombiner(AbstractRecombiner):
    def __init__(self, parent_count):
        if parent_count != 2:
            raise AssertionError("Parent_count in OnePointCrossover must be 2")
        super().__init__(parent_count)

    def recombine(self, parents):
        point = random.randint(1, len(parents) - 1)
        child1 = parents[0].chromosome[:point]
        child1.extend(parents[1].chromosome[point:])
        child2 = parents[1].chromosome[:point]
        child2.extend(parents[0].chromosome[point:])
        return [Individual(parents[0].problem, child1), Individual(parents[0].problem, child2)]



