from nia.Week_2.AbstractModules import AbstractMutator
import random


class BitFlipMutator(AbstractMutator):
    def mutate(self, chromosome):
        """Mutates the given chromosome by flipping a random allele"""
        for gene in range(len(chromosome)):
            if random.random() < self.mutation_probability:
                chromosome[gene] = random.randrange(0, self.allele_count)
        return chromosome


class SwapMutator(AbstractMutator):
    def mutate(self, chromosome):
        """Mutates the given chromosome by swapping random genes"""
        for gene in range(len(chromosome)):
            if random.random() < self.mutation_probability:
                next_gene = (gene + 1) % len(chromosome)
                chromosome[gene], chromosome[next_gene] = chromosome[next_gene], chromosome[gene]
        return chromosome
