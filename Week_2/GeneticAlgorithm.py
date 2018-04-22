import random
from operator import attrgetter
from statistics import median
from copy import copy
import time
from numpy import mean, argmax

import matplotlib.pyplot as plt

import Week_2.Initializer as Initializer
import Week_2.Mutator as Mutator
import Week_2.Recombiner as Recombiner
import Week_2.Replacer as Replacer
import Week_2.Selector as Selector
from Week_2.Problem import Problem


def current_milli_time():
    return int(round(time.time() * 1000))


class GeneticAlgorithm:
    def __init__(self, initializer, selector, recombiner, mutator, replacer, generation_count=200):
        self.initializer = initializer
        self.selector = selector
        self.recombiner = recombiner
        self.mutator = mutator
        self.replacer = replacer
        self.generation_count = generation_count
        self.generation_results = []

    def run(self):
        population = self.initializer.initialized_population()

        self.generation_results = []
        convergence_counter = 0
        for i in range(self.generation_count):
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
            gain_ratio = highest_fitness**2 / (i + 1) * 10
            if i > 0 and self.generation_results[i-1][0] == highest_fitness:
                convergence_counter += 1
            self.generation_results.append((highest_fitness, generation_median, needed_time, gain_ratio))
            if i % 10 == 0:
                print("After {} generations the highest fitness is {}".format(i, highest_fitness))
            if convergence_counter == 20:
                return

    def plot_result(self, position, title):
        highest_fitness, generation_median, needed_time, gain_ratio = zip(*self.generation_results)
        x = range(len(self.generation_results))
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.subplot(2, 2, position)
        plt.title(title)
        plt.plot(x, highest_fitness, label='Best candidate')
        plt.plot(x, generation_median, label='Generation mean')
        # plt.plot(x, gain_ratio, label='gain ratio')
        plt.legend()
        print("nedded_time_mean for {} is: {}".format(position, mean(needed_time)))
        print("you should stop after {} generations".format(argmax(gain_ratio)))
        # plt.plot(x, [1 - 1 / machines] * len(x), linewidth=0.5)

    def __str__(self):
        return type(self.initializer).__name__


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
                                                             crossover_point_count),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm2 = GeneticAlgorithm(Initializer.ZeroInitializer(problem2, population_count),
                                  Selector.RouletteSelector(selection_size),
                                  Recombiner.KPointCrossover(recombination_parent_count,
                                                             crossover_point_count),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm3 = GeneticAlgorithm(Initializer.ZeroInitializer(problem3, population_count),
                                  Selector.RouletteSelector(selection_size),
                                  Recombiner.KPointCrossover(recombination_parent_count,
                                                             crossover_point_count),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm4 = GeneticAlgorithm(Initializer.RandomInitializer(problem3, population_count),
                                  Selector.TournamentSelector(selection_size),
                                  Recombiner.UniformScanCrossover(30),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.DeleteAllReplacer())

    algorithm1.run()
    algorithm2.run()
    algorithm3.run()
    algorithm4.run()
    algorithm1.plot_result(1, str(algorithm1))
    algorithm2.plot_result(2, str(algorithm2))
    algorithm3.plot_result(3, str(algorithm3))
    algorithm4.plot_result(4, str(algorithm4))
    plt.show()
