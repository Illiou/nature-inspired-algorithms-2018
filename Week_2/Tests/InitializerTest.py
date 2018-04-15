import unittest
import Week_2.Initializer as Initializer
from Week_2.Genetic_Algorithm import Problem
import random


class InitializerTest(unittest.TestCase):
    def setUp(self):
        jobs = [10, 20, 13, 15, 10, 23, 14]
        self.problem = Problem(jobs, 5)

    def testRandomInitializer(self):
        random.seed(0)
        population = Initializer.RandomInitializer(self.problem, 10).initialized_population()
        self.assertEqual(10, len(population))
        self.assertEqual([[3, 3, 0, 2, 4, 3, 3],
                          [2, 3, 2, 4, 1, 4, 1],
                          [2, 1, 0, 4, 2, 4, 4],
                          [1, 2, 0, 0, 2, 3, 4]], [individual.chromosome for individual in population[0:4]])

    def testZeroInitializer(self):
        population = Initializer.ZeroInitializer(self.problem, 10).initialized_population()
        self.assertEqual(10, len(population))
        self.assertEqual([[0]*7 for _ in range(10)], [individual.chromosome for individual in population])


if __name__ == '__main__':
    unittest.main()
