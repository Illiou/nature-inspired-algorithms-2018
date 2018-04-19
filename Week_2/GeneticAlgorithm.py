import random
import matplotlib.pyplot as plt
import Week_2.Initializer as Initializer
import Week_2.Selector as Selector
import Week_2.Recombiner as Recombiner
import Week_2.Mutator as Mutator
import Week_2.Replacer as Replacer
from Week_2.Problem import Problem


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

        highest_fitness_list = []
        for i in range(self.generation_count):
            mating_pool = self.selector.select_chromosomes(population)

            parent_count = self.recombiner.parent_count
            all_parents = [mating_pool[i:i+parent_count] for i in range(0, len(mating_pool), parent_count)]
            offspring = []
            for parents in all_parents:
                offspring += self.recombiner.recombine(parents)
            for offspring_chromosome in offspring:
                offspring_chromosome.mutate(self.mutator)
            population = self.replacer.replace(population, offspring)

            highest_fitness = max(map(lambda individual: individual.fitness, population))
            highest_fitness_list.append(highest_fitness)
            if i % 100 == 0:
                print("After {} generations the highest fitness is {}".format(i, highest_fitness))

        x = range(self.generation_count)
        plt.xlabel('Generations')
        plt.ylabel('Fitness')
        plt.plot(x, highest_fitness_list, label='Best candidate')
        # plt.plot(x, generation_mean, label='Generation mean')
        # plt.plot(x, [1 - 1 / machines] * len(x), linewidth=0.5)
        plt.show()


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

    population_count = 40
    selection_size = 5
    recombination_parent_count = 2
    mutation_probability = 0.1

    algorithm1 = GeneticAlgorithm(Initializer.ZeroInitializer(problem1, population_count),
                                  Selector.RouletteSelector(selection_size),
                                  Recombiner.OnePointCrossoverRecombiner(recombination_parent_count),
                                  Mutator.BitFlipMutator(mutation_probability, problem1.machine_count),
                                  Replacer.PseudoReplacer())
    algorithm1.run()
