import random


class Individual:
    def __init__(self, problem, chromosome):
        self.problem = problem
        self.chromosome = chromosome
        self.fitness = self._calculate_fitness()

    def _calculate_fitness(self):
        machine_time = [0] * self.problem.machine_count
        for gene, allele in enumerate(self.chromosome):
            machine_time[allele] += self.problem.jobs[gene]
        fitness = (sum(self.problem.jobs) - max(machine_time)) / sum(self.problem.jobs)
        return fitness

    def mutate(self, mutator):
        self.chromosome = mutator.mutate(self.chromosome)
        self.fitness = self._calculate_fitness()


class Problem:
    def __init__(self, jobs, machine_count):
        self.jobs = jobs
        self.machine_count = machine_count


class GeneticAlgorithm:
    def __init__(self, initializer, selector, recombiner, mutator, replacer, generation_count=5000):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.replacer = replacer
        self.generation_count = generation_count

    def run(self):
        population = self.initializer.initialized_population()

        for i in range(self.generation_count):
            mating_pool = self.selector.select_chromosomes(population)

            parent_count = self.recombiner.parent_count
            all_parents = [mating_pool[i:i+parent_count] for i in range(0, len(mating_pool), parent_count)]
            offspring = []
            for parents in all_parents:
                offspring.append(self.recombiner.recombine(parents))
            for offspring_chromosome in offspring:
                offspring_chromosome.mutate()
            population = self.replacer.replace(population)

            highest_fitness = max(map(lambda individual: individual.fitness, population))
            print("After {} generations the highest fitness is {}".format(i, highest_fitness))


if __name__ == '__main__':
    pass
    jobs1 = [random.randint(10, 1000) for _ in range(200)]
    jobs1 += [random.randint(100, 300) for _ in range(100)]
    problem1 = Problem(jobs1, 20)
    jobs2 = [random.randint(10, 1000) for _ in range(150)]
    jobs2 += [random.randint(400, 700) for _ in range(150)]
    problem2 = Problem(jobs2, 20)
    jobs3 = [50] * 3
    jobs3 += [int(i/2) for i in range(51*2, 100*2)]
    problem3 = Problem(jobs3, 50)
    # GeneticAlgorithm(ZeroInitializer(), , , BitFlipMutator(), ) TODO
