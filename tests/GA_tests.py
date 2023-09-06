import unittest
from MultiObjectiveHelper.MultiObjectiveHelper import MultiObjectiveHelper
from tests.GA_tests_helper import GA_tests_helper


class MyTestCase(unittest.TestCase):

    def test_crossover_PMX(self):
        GA = GA_tests_helper.get_GA()
        start = 2
        end = 8
        # chromosome_a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chromosome_a = [147, 12, 9, 125, 39, 73, 89, 30, 98, 19, 127, 140, 129, 14, 54, 17, 67, 66, 126, 86, 101, 59, 11]
        chromosome_b = [125, 92, 147, 141, 25, 24, 108, 43, 84, 115, 62, 5, 56, 113, 112, 114, 75, 99, 39, 96, 31, 69, 83]

        # chromosome_b = [9, 3, 7, 8, 2, 6, 5, 1, 4]

        childs = GA.crossover_PMX(chromosome_a, chromosome_b, start, end)
        print(childs[1])
        expected_child = [9, 3, 2, 4, 5, 6, 7, 1, 8]
        self.assertEqual(len(chromosome_a), len(childs[0]))
        self.assertEqual(expected_child, childs[0])

    def test_swap_mutation(self):
        GA = GA_tests_helper.get_GA()
        chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        start = 1
        end = 5

        expected_chromosome = [1, 6, 3, 4, 5, 2, 7, 8, 9]
        chromosome_after_mutation = GA.swap_mutation(chromosome, start, end)

        self.assertEqual(len(chromosome), len(chromosome_after_mutation))
        self.assertEqual(expected_chromosome, chromosome_after_mutation)

    def test_inversion_mutation(self):
        GA = GA_tests_helper.get_GA()
        chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        start = 2
        end = 5

        expected_chromosome = [1, 2, 6, 5, 4, 3, 7, 8, 9]
        chromosome_after_mutation = GA.inversion_mutation(chromosome, start, end)

        self.assertEqual(len(chromosome), len(chromosome_after_mutation))
        self.assertEqual(expected_chromosome, chromosome_after_mutation)

    def test_rotation_mutation(self):
        GA = GA_tests_helper.get_GA()
        chromosome = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        start = 2
        end = 6

        expected_chromosome = [1, 2, 7, 6, 5, 4, 3, 8, 9]
        chromosome_after_mutation = GA.rotation_mutation(chromosome, start, end)

        self.assertEqual(len(chromosome), len(chromosome_after_mutation))
        self.assertEqual(expected_chromosome, chromosome_after_mutation)

    def test_get_candidates_unique(self):
        GA = GA_tests_helper.get_GA()
        pool = GA_tests_helper.get_population()

        for i in range(10):
            candidate_a, candidate_b = GA.get_candidates(pool)
            self.assertNotEqual(candidate_a, candidate_b)

    def test_tournament_selection_by_rank(self):
        GA = GA_tests_helper.get_GA()
        pool = GA_tests_helper.get_population()
        MultiObjectiveHelper.UpdatePopulationFitness(pool)
        rival_1 = pool[0]
        rival_2 = pool[2]
        winner = GA.tournamentSelection(rival_1, rival_2)
        self.assertEqual(rival_1, winner)

        winner = GA.tournamentSelection(rival_2, rival_1)
        self.assertEqual(rival_1, winner)

    def test_tournament_selection_by_crowding_distance(self):
        GA = GA_tests_helper.get_GA()
        pool = GA_tests_helper.get_population()
        MultiObjectiveHelper.UpdatePopulationFitness(pool)
        rival_1 = pool[1]
        rival_2 = pool[0]
        winner = GA.tournamentSelection(rival_1, rival_2)
        self.assertEqual(rival_1, winner)

        winner = GA.tournamentSelection(rival_2, rival_1)
        self.assertEqual(rival_1, winner)

    def test_get_best_individuals(self):
        GA = GA_tests_helper.get_GA()
        pool = GA_tests_helper.get_population()
        MultiObjectiveHelper.UpdatePopulationFitness(pool)
        best_individuals = GA.getBestIndividuals(pool)

        expected_best_individuals = [pool[0], pool[1], pool[3]]
        self.assertEqual(len(expected_best_individuals), len(best_individuals))

        for individual in expected_best_individuals:
            self.assertIn(individual, best_individuals)

if __name__ == '__main__':
    unittest.main()
