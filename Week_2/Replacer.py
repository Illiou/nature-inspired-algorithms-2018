from nia.Week_2.AbstractModules import AbstractReplacer
import random
from operator import attrgetter


class DeleteAllReplacer(AbstractReplacer):
    def replace(self, current_population, offspring):
        """Replaces the current_population with an equal number of the offspring chromosomes keeping only the best"""
        if len(offspring) < len(current_population):
            raise ValueError("Offspring needs to be at least as large as current population.")
        best_performing_individual = max(current_population, key=attrgetter("fitness"))
        if len(offspring) == len(current_population):
            new_population = offspring
        else:
            new_population = random.sample(offspring, len(current_population))
        new_population[-1] = best_performing_individual
        return new_population


class SteadyStateReplacer(AbstractReplacer):
    def __init__(self, n, replace_worst=False):
        self.n = n
        self.replace_worst = replace_worst

    def replace(self, current_population, offspring):
        """Replaces only a random number of the current-population`s individuals with some of the offspring"""
        if len(offspring) < self.n:
            raise ValueError("Offspring needs to be at least as large as the chosen n.")
        best_performing_individual = max(current_population, key=attrgetter("fitness"))
        chosen_offspring = random.sample(offspring, self.n)
        nr_to_fill = len(current_population) - self.n
        if self.replace_worst:
            new_population = chosen_offspring + sorted(current_population, key=attrgetter("fitness"), reverse=True)[:nr_to_fill]
        else:
            new_population = chosen_offspring + random.sample(current_population, nr_to_fill)
        new_population[-1] = best_performing_individual
        return new_population
