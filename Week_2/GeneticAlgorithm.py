import random
import time
from copy import copy
from operator import attrgetter
from statistics import median

import matplotlib.pyplot as plt
from numpy import mean

import Week_2.Initializer as Initializer
import Week_2.Mutator as Mutator
import Week_2.Recombiner as Recombiner
import Week_2.Replacer as Replacer
import Week_2.Selector as Selector
from Week_2.Problem import Problem


def current_milli_time():
    return int(round(time.time() * 1000))


class GeneticAlgorithm:
    def __init__(self, initializer, selector, recombiner, mutator, replacer, generation_count=100):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.replacer = replacer
        self.generation_count = generation_count
        self.generation_results = []

    def run(self, iterations=10):
        self.generation_results = []
        for i in range(iterations):
            self.generation_results.append([])
            population = self.initializer.initialized_population()

            for j in range(self.generation_count):
                start_time = current_milli_time()

                mating_pool = self.selector.select_chromosomes(population)

                parent_count = self.recombiner.parent_count
                all_parents = [mating_pool[i:i+parent_count] for i in range(0, len(mating_pool), parent_count)]
                while len(all_parents[-1]) < self.recombiner.parent_count:
                    all_parents[-1].append(copy(all_parents[-1][0]))
                offspring = []
                for parents in all_parents:
                    offspring += self.recombiner.recombine(parents)
                for offspring_chromosome in offspring:
                    offspring_chromosome.mutate(self.mutator)
                population = self.replacer.replace(population, offspring)

                max1 = max(population, key=attrgetter("fitness"))
                highest_fitness = max1.fitness
                generation_median = median(i.fitness for i in population)
                current_time = current_milli_time()
                needed_time = current_time - start_time
                self.generation_results[i].append([highest_fitness, generation_median, needed_time])
                if (j + 1) % 10 == 0:
                    print("In the {} iteration after {} generations the highest fitness is {}".format(i+1, j+1,
                                                                                                      highest_fitness))

    def plot_result(self, position=None, rows=2, columns=2):
        # calculate the mean of all iterations for every generation_step for highest_fitness, generation median and time
        # np.transpose(T) instead of zip
        highest_fitness, generation_median, needed_time = mean(self.generation_results, 0).T
        x = range(len(self.generation_results[0]))
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        if position is not None:
            plt.subplot(rows, columns, position)
        plt.plot(x, highest_fitness, label='Best candidate')
        plt.plot(x, generation_median, label='Generation mean')
        plt.legend()
        print("nedded_time_mean for {} is: {}".format(position, mean(needed_time)))
        # plt.plot(x, [1 - 1 / machines] * len(x), linewidth=0.5)


if __name__ == '__main__':
    jobs1 = [random.randint(10, 1000) for _ in range(200)]
    jobs1 += [random.randint(100, 300) for _ in range(100)]
    problem1 = Problem(jobs1, 20)

    jobs2 = [random.randint(10, 1000) for _ in range(150)]
    jobs2 += [random.randint(400, 700) for _ in range(150)]
    problem2 = Problem(jobs2, 20)

    jobs3 = [50] * 3
    jobs3 += [int(i/2) for i in range(51*2, 100*2)]
    problem3 = Problem(jobs3, 50)

    population_count = 50
    recombination_parent_count = 3
    crossover_point_count = 2
    selection_size = population_count
    crossover_probability = 0.6
    mutation_probability = 0.1

    algorithm1 = GeneticAlgorithm(Initializer.ZeroInitializer(problem1, population_count),
                                  Selector.RouletteSelector(selection_size),
                                  Recombiner.KPointCrossover(recombination_parent_count,
                                                             crossover_probability,
                                                             crossover_point_count),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm2 = GeneticAlgorithm(Initializer.RandomInitializer(problem2, population_count),
                                  Selector.RouletteSelector(selection_size),
                                  Recombiner.KPointCrossover(recombination_parent_count,
                                                             crossover_probability,
                                                             crossover_point_count),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm3 = GeneticAlgorithm(Initializer.RandomInitializer(problem3, population_count),
                                  Selector.RouletteSelector(selection_size),
                                  Recombiner.KPointCrossover(recombination_parent_count,
                                                             crossover_probability,
                                                             crossover_point_count),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm4 = GeneticAlgorithm(Initializer.RandomInitializer(problem3, population_count),
                                  Selector.TournamentSelector(selection_size),
                                  Recombiner.UniformScanCrossover(30, crossover_probability),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm1.run()
    # algorithm2.run()
    # algorithm3.run()
    # algorithm4.run()
    algorithm1.plot_result()
    # algorithm2.plot_result(2)
    # algorithm3.plot_result(3)
    # algorithm4.plot_result(4)
    plt.show()
