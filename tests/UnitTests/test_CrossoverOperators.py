import unittest
from GeneticAlgorithm.Operators.CrossoverOperators import CrossoverOperators


class CrossoverOperatorsTests(unittest.TestCase):
    def test_crossover_PMX(self):
        start = 2
        end = 8
        # chromosome_a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chromosome_a = [147, 12, 9, 125, 39, 73, 89, 30, 98, 19, 127, 140, 129, 14, 54, 17, 67, 66, 126, 86, 101, 59,
                        11]
        chromosome_b = [125, 92, 147, 141, 25, 24, 108, 43, 84, 115, 62, 5, 56, 113, 112, 114, 75, 99, 39, 96, 31, 69,
                        83]

        # chromosome_b = [9, 3, 7, 8, 2, 6, 5, 1, 4]

        child = CrossoverOperators.crossover_PMX(chromosome_a, chromosome_b, start, end)
        expected_child = [9, 12, 147, 141, 25, 24, 108,
                          43, 98, 19, 127, 140, 129, 14, 54, 17, 67, 66, 126, 86, 101, 59, 11]
        self.assertEqual(len(chromosome_a), len(child))
        self.assertEqual(expected_child, child)


if __name__ == '__main__':
    unittest.main()
