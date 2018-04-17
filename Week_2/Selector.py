from Week_2.AbstractModules import AbstractSelector
import random


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
        total_fitness = sum(fitness)

        # avoid division by zero if all individual have a fitness of 0
        if total_fitness == 0:
                fitness = [1 for _ in fitness]
                total_fitness = sum(fitness)
                
        cumulated = []

        # create cumulated list
        for i, value in enumerate(fitness):
            if i == 0:
                cumulated.append(value/total_fitness)
            else:
                cumulated.append(cumulated[i-1] + value/total_fitness)

        pool = []

        # get a random r between 0 and 1 and pick the individual with the closest
        # bigger cumulated probability

        for i in range(self.selection_size):
            r = random.uniform(0,1)

            if r < cumulated[0]:
                pool.append(population[0])

            else:
                for j, value in enumerate(cumulated):
                    if j != 0:
                        if r < value and r > cumulated[j-1]:
                            pool.append(population[j-1])
                            break

        return pool


class TournamentSelector(AbstractSelector):

    def __init__(self, selection_size, s):
        """
        Initialize the Selector

        Args:
            selection_size(int): the number of selected chromosomes
            s(int): number of candidates in the selection tournament
        """

        super().__init__(selection_size)
        self.selection_size = selection_size
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

        candidates = []
        indices = []
        pool = []

        for i in range(self.selection_size):
            for j in range(self.s):
                # pick s random individuals, collect them
                rndm = random.randint(0,len(population)-1)
                candidates.append(population[rndm].fitness)
                indices.append(rndm)

            # find the fittest individual out of the random collection, append to mating pool
            pool.append(population[indices[candidates.index(max(candidates))]])

            candidates = []
            indices = []

        return pool
