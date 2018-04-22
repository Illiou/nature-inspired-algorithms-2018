class Individual:
    def __init__(self, problem, chromosome, fitness=None):
        self.problem = problem
        self.chromosome = chromosome
        if fitness is None:
            self.fitness = self._calculate_fitness()
        else:
            self.fitness = fitness

    def __copy__(self):
        # to improve performance by not recalculating fitness each time a deepcopy gets made
        return Individual(self.problem, self.chromosome.copy(), self.fitness)

    def _calculate_fitness(self):
        machine_time = [0] * self.problem.machine_count
        for gene, allele in enumerate(self.chromosome):
            machine_time[allele] += self.problem.jobs[gene]
        return (self.problem.jobs_sum - max(machine_time)) / self.problem.jobs_sum

    def mutate(self, mutator):
        self.chromosome = mutator.mutate(self.chromosome)
        self.fitness = self._calculate_fitness()


class Problem:
    def __init__(self, jobs, machine_count):
        self.jobs = jobs
        self.machine_count = machine_count
        self.jobs_sum = sum(jobs)