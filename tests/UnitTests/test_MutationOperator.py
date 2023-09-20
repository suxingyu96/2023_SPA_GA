import unittest
from GeneticAlgorithm.Operators.MutationOperators import MutationOperators


class MutationOperatorsTests(unittest.TestCase):
    def test_swap_mutation(self):
        chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        start = 1
        end = 5

        expected_chromosome = [1, 6, 3, 4, 5, 2, 7, 8, 9]
        chromosome_after_mutation = MutationOperators.swap_mutation(chromosome, start, end)

        self.assertEqual(len(chromosome), len(chromosome_after_mutation))
        self.assertEqual(expected_chromosome, chromosome_after_mutation)

    def test_inversion_mutation(self):
        chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        start = 2
        end = 5

        expected_chromosome = [1, 2, 6, 5, 4, 3, 7, 8, 9]
        chromosome_after_mutation = MutationOperators.inversion_mutation(chromosome, start, end)

        self.assertEqual(len(chromosome), len(chromosome_after_mutation))
        self.assertEqual(expected_chromosome, chromosome_after_mutation)

    def test_rotation_mutation(self):
        chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        start = 2
        end = 6

        expected_chromosome = [1, 2, 7, 6, 5, 4, 3, 8, 9]
        chromosome_after_mutation = MutationOperators.rotation_mutation(chromosome, start, end)

        self.assertEqual(len(chromosome), len(chromosome_after_mutation))
        self.assertEqual(expected_chromosome, chromosome_after_mutation)


if __name__ == '__main__':
    unittest.main()
