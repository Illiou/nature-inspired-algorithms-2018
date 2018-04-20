from Week_2.AbstractModules import AbstractSelector
import random
from operator import attrgetter


class RouletteSelector(AbstractSelector):
    def select_chromosomes(self, population):
        """
        Select assignments from population according to self.selection_size
        - Roulette Wheel variation: assign cumulative probability to all the individuals,
                                    then choose n randomly, according to the cumulated probability

        Args:
            population(list): a list of individuals
        Returns:
            a list of the selected assignments
        """

        fitness = [individual.fitness for individual in population]
        if sum(fitness) == 0:
            fitness = None
        return random.choices(population, weights=fitness, k=self.selection_size)


class TournamentSelector(AbstractSelector):

    def __init__(self, selection_size, s=2):
        """
        Initialize the Selector

        Args:
            selection_size(int): the number of selected chromosomes
            s(int): number of candidates in the selection tournament
        """

        super().__init__(selection_size)
        self.s = s

    def select_chromosomes(self, population):
        """
        Select assignments from population according to self.selection_size
        - Tournament variation: pick s individuals randomly, put the fittest in the mating pool

        Args:
            population(list): a list of individuals
        Returns:
            a list of the selected assignments
        """

        pool = []
        for _ in range(self.selection_size):
            candidates = random.sample(population, self.s)
            pool.append(max(candidates, key=attrgetter("fitness")))
        return pool
