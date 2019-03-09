from nia.Week_2.AbstractModules import AbstractProblem, AbstractIndividual


class Individual(AbstractIndividual):
    def _calculate_fitness(self):
        machine_time = [0] * self.problem.machine_count
        for gene, allele in enumerate(self.chromosome):
            machine_time[allele] += self.problem.jobs[gene]
        return (self.problem.jobs_count - max(machine_time)) / self.problem.jobs_count


class Problem(AbstractProblem):
    def create_individual(self, chromosome, fitness=None):
        return Individual(self, chromosome, fitness)

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

    def chromosome_size(self):
        return len(self.jobs)

    def allele_count(self):
        return self.machine_count

