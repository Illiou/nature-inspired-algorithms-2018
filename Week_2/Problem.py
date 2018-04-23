class Individual:
    def __init__(self, problem, chromosome, fitness=None):
        """
        An individual of the population

        Args:
            problem(Problem): The according problem
            chromosome(list): the chromosome of the individual
            fitness(float): a already computed fitness value, which will be newly computed if None
        """
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
        return (self.problem.jobs_count - max(machine_time)) / self.problem.jobs_count

    def mutate(self, mutator):
        """
        Mutates the individuals`s chromosome by using the given mutator
        Args:
            mutator: the mutator used for mutation
        """
        self.chromosome = mutator.mutate(self.chromosome)
        self.fitness = self._calculate_fitness()


class Problem:
    def __init__(self, jobs, machine_count):
        """
        A problem consisting of jobs and a machine_count
        Args:
            jobs(list): a list of time-values the jobs are needing
            machine_count: the number of machines in the problem
        """
        self.jobs = jobs
        self.machine_count = machine_count
        self.jobs_count = sum(jobs)
