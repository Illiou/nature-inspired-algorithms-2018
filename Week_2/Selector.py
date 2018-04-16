from AbstractModules import AbstractSelector
import random

class Roulette_Selector(AbstractSelector):
        
    def select_chromosomes(self, population):
        """
        Select assignments from population according to self.selection_size
        - Roulette Wheel variation: assign cummulative probability to all the individuals,
                                    then choose n randomly, according to the cummulated probability
            
        Args:
            population(list): a list of individuals
        Returns:
            a list of the selected assignments
        """
        
        fitness = [individual.fitness for individual in population]
        total_fitness = sum(fitness)
        
        cummulated = []
        
        # create cummulated list
        for i, value in enumerate(fitness):
            if i == 0:
                cummulated.append(value/total_fitness)
            else:
                cummulated.append(cummulated[i-1] + value/total_fitness)
        
        pool = []
        
        # get a random r between 0 and 1 and pick the individual with the closest
        # bigger cummulated probability
        
        for i in range(self.selection_size):
            r = random.uniform(0,1)
            
            if r < cummulated[0]:
                pool.append(population[0])
            
            else:
                for j, value in enumerate(cummulated):
                    if j != 0:
                        if r < value and r > cummulated[j-1]:
                            pool.append(population[j-1])
                            break
        
        return pool
        
    

class Tournament_Selector(AbstractSelector):
    
    def __init__(self,selection_size,s):
        """
        Initialize the Selector

        Args:
            selection_size(int): the number of selected chromosomes
            s(int): number of candidates in the selection tournament
        """
    
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
        indixes = []
        pool = []
        
        for i in range(self.selection_size):
            for j in range(self.s):
                # pick s random individuals, collect them
                rndm = random.randint(0,len(population)-1)
                candidates.append(population[rndm].fitness)
                indixes.append(rndm)
            
            # find the fittest individual out of the random collection, append to mating pool
            pool.append(population[indixes[candidates.index(max(candidates))]])
              
            candidates = []     
            indixes = []
        
        return pool
    

class Individual():
    
    def __init__(self,fitness):
        
        self.fitness = fitness

population = []

for i in range(10):
    population.append(Individual(i))

for indi in population:
    print(indi.fitness)



selector = Tournament_Selector(3,2)

pool = selector.select_chromosomes(population) 

print("drdr")

for indi in pool:
    print(indi.fitness)
