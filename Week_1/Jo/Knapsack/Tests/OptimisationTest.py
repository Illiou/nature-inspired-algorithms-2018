import unittest
from Woche1.Jo.Knapsack import Optimisation


class OptimisationTest(unittest.TestCase):
    def setUp(self):
        self.knapsack = Optimisation.KnapsackProblem([Optimisation.Item(10, 1000),
                                                      Optimisation.Item(100, 2000),
                                                      Optimisation.Item(300, 4000),
                                                      Optimisation.Item(1, 5000),
                                                      Optimisation.Item(200, 5000)], 400)
        self.optimisation_small_hill = Optimisation.Optimisation(self.knapsack, False, False)
        self.optimisation_small_first = Optimisation.Optimisation(self.knapsack, False, True)
        self.optimisation_large_hill = Optimisation.Optimisation(self.knapsack, True, False)
        self.optimisation_large_first = Optimisation.Optimisation(self.knapsack, True, True)

    def test_improving_neighbour(self):
        assignment = [0, 1, 1, 0, 0]
        neighbour = self.optimisation_small_hill.improving_neighbour(assignment)
        self.assertEqual(None, neighbour)
        neighbour = self.optimisation_small_first.improving_neighbour(assignment)
        self.assertEqual(None, neighbour)
        neighbour = self.optimisation_large_hill.improving_neighbour(assignment)
        self.assertEqual([0, 0, 1, 1, 0], neighbour)
        neighbour = self.optimisation_large_first.improving_neighbour(assignment)
        self.assertEqual([0, 0, 1, 1, 0], neighbour)

        assignment = [1, 1, 0, 0, 0]
        neighbour = self.optimisation_small_hill.improving_neighbour(assignment)
        self.assertEqual([1, 1, 0, 1, 0], neighbour)
        neighbour = self.optimisation_small_first.improving_neighbour(assignment)
        self.assertEqual([1, 1, 0, 1, 0], neighbour)
        neighbour = self.optimisation_large_hill.improving_neighbour(assignment)
        self.assertEqual([1, 1, 0, 1, 1], neighbour)
        neighbour = self.optimisation_large_first.improving_neighbour(assignment)
        self.assertEqual([0, 1, 1, 0, 0], neighbour)

    def test_run(self):
        assignment = [1, 1, 0, 0, 0]
        iterations, time, assignment = self.optimisation_large_hill.run()
        self.assertEqual(2, iterations)
        self.assertEqual(13000, self.knapsack.value_for_assignment(assignment))
        self.assertEqual(311, self.knapsack.weight_for_assignment(assignment))


if __name__ == '__main__':
    unittest.main()
