from Week_2.AbstractModules import AbstractRecombiner
from Week_2.Genetic_Algorithm import Individual
import random


class OnePointCrossoverRecombiner(AbstractRecombiner):

    def recombine(self, parents):
        point = random.randint(1, len(parents) - 1)
        child1 = parents[0].chromosome[:point]
        child1.extend(parents[1].chromosome[point:])
        child2 = parents[1].chromosome[:point]
        child2.extend(parents[0].chromosome[point:])
        return Individual(parents[0].problem, child1), Individual(parents[0].problem, child2)



