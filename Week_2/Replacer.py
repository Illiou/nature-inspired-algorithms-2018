from Week_2.AbstractModules import AbstractReplacer
import random
from operator import attrgetter


class DeleteAllReplacer(AbstractReplacer):
    def replace(self, current_population, offspring):
        if len(offspring) < len(current_population):
            raise ValueError("Offspring needs to be at least as large as current population.")
        if len(offspring) == len(current_population):
            return offspring
        else:
            return random.sample(offspring, len(current_population))


class SteadyStateReplacer(AbstractReplacer):
    def __init__(self, n, replace_worst=False):
        self.n = n
        self.replace_worst = replace_worst

    def replace(self, current_population, offspring):
        if len(offspring) < self.n:
            raise ValueError("Offspring needs to be at least as large as the chosen n.")
        chosen_offspring = random.sample(offspring, self.n)
        nr_to_fill = len(current_population) - self.n
        if self.replace_worst:
            return chosen_offspring + sorted(current_population, key=attrgetter("fitness"), reverse=True)[:nr_to_fill]
        else:
            return chosen_offspring + random.sample(current_population, nr_to_fill)
