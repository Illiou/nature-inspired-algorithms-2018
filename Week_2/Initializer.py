from nia.Week_2.AbstractModules import AbstractInitializer, AbstractInitializer
from nia.Week_2.Problem import Individual
import random


class ZeroInitializer(AbstractInitializer):
    def initialized_population(self):
        """Initializes the population with zeros only"""
        chromosome_size = self.problem.chromosome_size()
        return [self.problem.create_individual([0] * chromosome_size) for _ in range(self.population_size)]


class RandomInitializer(AbstractInitializer):

    def initialized_population(self):
        """Initializes the population randomly"""
        population = []
        chromosome_size = self.problem.chromosome_size()
        for i in range(self.population_size):
            chromosome = [random.randint(0, self.problem.allele_count() - 1) for _ in range(chromosome_size)]
            population.append(self.problem.create_individual(chromosome))
        return population
