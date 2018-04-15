import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model


class Individual:
    def __init__(self, problem, chromosome):
        self.problem = problem
        self.chromosome = chromosome
        self.age = 0
        self.fitness = 0
        self.update_fitness()

    def __str__(self):
        return str(self.chromosome)

    def update_fitness(self):
        machine_time = [0] * self.problem.machines
        for allele, gene in enumerate(self.chromosome):
            machine_time[gene] += self.problem.jobs[allele]
        self.fitness = (sum(self.problem.jobs) - max(machine_time)) / sum(self.problem.jobs)

    def mutate(self, probability=0.01):
        for index, _gene in enumerate(self.chromosome):
            if random.random() < probability:
                self.chromosome[index] = random.randrange(0, self.problem.machines)
        self.update_fitness()


class Population:
    def __init__(self, problem, pop_size):
        self.pop_size = pop_size
        self.problem = problem
        self.population = self.population_initializer()

    def population_initializer(self):
        population = []
        for i in range(self.pop_size):
            population.append(self.random_individual())
        return population

    def random_individual(self):
        # chromosome = [0]*self.problem.job_count
        # chromosome[0] = random.randrange(1, self.problem.machines)
        for gene in range(self.problem.job_count):
            chromosome.append(random.randrange(0, self.problem.machines))
        return Individual(self.problem, chromosome)

    def evolve(self, stop_criterion=100):
        gen = 0
        while gen < stop_criterion:
            self.next_generation()
            best = self.best_candidate()
            print("{:0.4f}".format(best.fitness))
            gen += 1

    def best_candidate(self):
        return max(self.population, key=lambda item: item.fitness)

    def next_generation(self):
        # PARAMETERS
        number_selected = int((1 / 3) * len(self.population))
        number_of_children = len(self.population) - number_selected
        selection_type = "roulette"
        mutation_probability = 0.005

        save_the_best = self.best_candidate()
        parent_generation = self.selection(number_selected, selection_type)
        children = self.recombine(number_of_children, parent_generation)
        next_generation = parent_generation + children
        found = False
        for individual in next_generation:
            if individual == save_the_best:
                found = True
            else:
                individual.mutate(mutation_probability)
        if not found:
            if next_generation[0].fitness < save_the_best.fitness:
                next_generation[0] = save_the_best
        self.population = next_generation

        fit = []
        for i in pop.population:
            fit.append(i.fitness)

        return self.best_candidate(), np.mean(fit)

    def selection(self, number_of_candidates, kind="roulette"):
        population_fitness = []
        for individual in self.population:
            population_fitness.append(individual.fitness)
        total_fitness = sum(population_fitness)

        if kind == "roulette":
            slots = []
            for fitness in population_fitness:
                slots.append(fitness / total_fitness)
                # Calculate the cumulative distribution
                if len(slots) > 1:
                    slots[len(slots) - 1] = slots[len(slots) - 1] + slots[len(slots) - 2]

            parent_generation = []
            for _c in range(number_of_candidates):
                rand = random.random()
                for index, slot in enumerate(slots):
                    if slot > rand:
                        parent_generation.append(self.population[index - 1])
                        break
            return parent_generation

        # TODO ordinal selection

    def recombine(self, number_of_children, parents):
        # TODO implement probability of mating at all (crossover probability)
        children = []
        for child in range(number_of_children // 2):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            while parent1 == parent2:
                parent2 = random.choice(parents)
            children.extend(self.one_point_crossover(parent1, parent2))
        # TODO Check if this makes sense. Might also use copy of a Parent
        while len(children) < number_of_children:
            children.append(self.random_individual())
        return children

    def one_point_crossover(self, parent1, parent2):
        point = random.randint(1, self.problem.job_count - 1)
        child1 = parent1.chromosome[:point]
        child1.extend(parent2.chromosome[point:])
        child2 = parent2.chromosome[:point]
        child2.extend(parent1.chromosome[point:])
        return Individual(self.problem, child1), Individual(self.problem, child2)


class Problem:
    def __init__(self, machines_, job_count_, min_working_time=1, max_working_time=20):
        self.machines = machines_
        self.job_count = job_count_
        self.jobs = self.job_initializer(min_working_time, max_working_time)

    def job_initializer(self, min_working_time=1, max_working_time=20):
        jobs = []
        for _job in range(self.job_count):
            jobs.append(random.randint(min_working_time, max_working_time))
        return jobs


if __name__ == '__main__':
    # PARAMETERS
    runs = 50000
    machines = 40
    job_count = 300
    population_size = 40

    p = Problem(machines, job_count, 1, 100)
    pop = Population(p, population_size)

    generations = 0
    best_candidates_fitness = []
    generation_mean = []

    while generations < runs:
        best_cand, mean_fit = pop.next_generation()

        best_candidates_fitness.append(best_cand.fitness)
        generation_mean.append(mean_fit)
        generations += 1
        if generations % 10 == 0:
            print(".", end="")
            if generations % 800 == 0:
                print("\t", generations)

    x = range(generations)
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.plot(x, best_candidates_fitness, label='Best candidate')
    plt.plot(x, generation_mean, label='Generation mean')
    plt.plot(x,[1-1/machines]*len(x), linewidth=0.5)

    X, y = np.array(x).reshape(-1, 1), np.array(generation_mean).reshape(-1, 1)
    regression = linear_model.LinearRegression()
    regression.fit(X, y)
    line_points = [[0], [generations]]
    line_prediction = regression.predict(line_points)
    plt.plot(line_points, line_prediction, label="{:0.8f}".format(regression.coef_[0, 0]))
    print("\n", regression.coef_[0,0])

    plt.legend(loc='lower center')
    plt.show()
