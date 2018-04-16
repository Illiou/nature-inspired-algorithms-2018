from Week_2.AbstractModules import AbstractInitializer
from Week_2.Genetic_Algorithm import Individual
import random


class ZeroInitializer(AbstractInitializer):

    def initialized_population(self):
        population = []
        chromosome_size = len(self.problem.jobs)
        for i in range(self.population_size):
            chromosome = [0] * chromosome_size
            population.append(Individual(self.problem, chromosome))
        return population


class RandomInitializer(AbstractInitializer):

    def initialized_population(self):
        population = []
        chromosome_size = len(self.problem.jobs)
        for i in range(self.population_size):
            chromosome = [random.randint(0, self.problem.machine_count-1) for _ in range(chromosome_size)]
            population.append(Individual(self.problem, chromosome))
        return population
