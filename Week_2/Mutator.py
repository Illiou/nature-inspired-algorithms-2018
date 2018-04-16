from AbstractModules import AbstractMutator
import random


class BitFlipMutator(AbstractMutator):

    def mutate(self, chromosome):
        for index, _gene in enumerate(chromosome):
            if random.random() < self.mutation_probability:
                chromosome[index] = random.randrange(0, self.machine_count)
        return chromosome


class SwapMutator(AbstractMutator):

    def mutate(self, chromosome):
        for index, allele in enumerate(chromosome):
            if random.random() < self.mutation_probability:
                chromosome[index] = chromosome[(index + 1) % len(chromosome)]
                chromosome[(index + 1) % len(chromosome)] = allele
        return chromosome
