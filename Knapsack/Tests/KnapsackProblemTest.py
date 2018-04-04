import unittest
import random
from Knapsack.KnapsackProblem import KnapsackProblem, Item


class KnapsackProblemTest(unittest.TestCase):
    def setUp(self):
        self.knapsack = KnapsackProblem([Item(10, 1000),
                                         Item(100, 2000),
                                         Item(300, 4000),
                                         Item(1, 5000),
                                         Item(200, 5000)], 400)

    def test_random_assignment(self):
        random.seed(0)
        assignment = self.knapsack.random_assignment()
        self.assertEqual(assignment, [1, 1, 0, 1, 1])
        self.assertLessEqual(self.knapsack.weight_for_assignment(assignment), 400)

    def test_is_feasible(self):
        assignment = [0, 0, 1, 0, 1]
        self.assertFalse(self.knapsack.is_feasible(assignment))
        assignment = [0, 1, 1, 0, 0]
        self.assertTrue(self.knapsack.is_feasible(assignment))

    def test_value_for_assignment(self):
        assignment = [0, 0, 1, 0, 1]
        self.assertEqual(9000, self.knapsack.value_for_assignment(assignment))
        assignment = [0, 1, 1, 0, 0]
        self.assertEqual(6000, self.knapsack.value_for_assignment(assignment))

    def test_small_neighbourhood(self):
        assignment = [0, 1, 1, 0, 0]
        neighbourhood = self.knapsack.small_neighbourhood(assignment)
        expected_neighbourhood = [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0]]
        self.assertEqual(expected_neighbourhood, neighbourhood)

    def test_large_neighbourhood(self):
        assignment = [0, 1, 1, 0, 0]
        neighbourhood = self.knapsack.large_neighbourhood(assignment)
        expected_neighbourhood = [[1, 0, 1, 0, 0], [1, 1, 0, 0, 0], [0, 0, 0, 0, 0],
                                  [0, 0, 1, 1, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1]]
        self.assertEqual(expected_neighbourhood, neighbourhood)


if __name__ == '__main__':
    unittest.main()
