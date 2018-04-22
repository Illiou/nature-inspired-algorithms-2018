from Week_2.AbstractModules import AbstractMutator
import random


class BitFlipMutator(AbstractMutator):

    def mutate(self, chromosome):
        for gene in range(len(chromosome)):
            if random.random() < self.mutation_probability:
                chromosome[gene] = random.randrange(0, self.machine_count)
        return chromosome


class SwapMutator(AbstractMutator):

    def mutate(self, chromosome):
        for gene in range(len(chromosome)):
            if random.random() < self.mutation_probability:
                next_gene = (gene + 1) % len(chromosome)
                chromosome[gene], chromosome[next_gene] = chromosome[next_gene], chromosome[gene]
        return chromosome
