class Individual:
    def __init__(self, problem, chromosome):
        self.problem = problem
        self.chromosome = chromosome
        self.fitness = self._calculate_fitness()

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