import unittest
import Week_2.Mutator as Mutator
import random


class InitializerTest(unittest.TestCase):
    """Test for testing the mutators"""
    def setUp(self):
        self.mutation_probability = 0.5
        self.machine_count = 5
        self.chromosome = [3, 3, 0, 2, 4, 3, 3]

    def testBitFlipMutator(self):
        random.seed(0)
        mutated_gene = Mutator.BitFlipMutator(self.mutation_probability, self.machine_count).mutate(self.chromosome)
        self.assertEqual(len(self.chromosome), len(mutated_gene))
        self.assertEqual([3, 3, 2, 2, 2, 3, 1], mutated_gene)

    def testSwapMutator(self):
        random.seed(0)
        mutated_gene = Mutator.SwapMutator(self.mutation_probability, self.machine_count).mutate(self.chromosome)
        self.assertEqual(len(self.chromosome), len(mutated_gene))
        self.assertEqual([3, 3, 2, 4, 0, 3, 3], mutated_gene)


if __name__ == '__main__':
    unittest.main()
