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