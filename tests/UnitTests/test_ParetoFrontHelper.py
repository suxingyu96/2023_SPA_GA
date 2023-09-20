import unittest
from math import inf

from GeneticAlgorithm.ParetoFrontHelper import ParetoFrontHelper
from tests.UnitTests.unit_tests_helper import unit_tests_helper


class ParetoFrontHelperTests(unittest.TestCase):
    def test_rank_calculation(self):
        pool = unit_tests_helper.get_population()
        ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(pool)
        self.assertEqual(pool[0].Rank, 1)
        self.assertEqual(pool[1].Rank, 1)
        self.assertEqual(pool[3].Rank, 1)
        self.assertEqual(pool[2].Rank, 2)

    def test_crowding_distance_calculation(self):
        pool = unit_tests_helper.get_population()
        ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(pool)
        epsilon = 0.00001

        self.assertEqual(inf, pool[1].CrowdingDistance)
        self.assertEqual(inf, pool[3].CrowdingDistance)
        self.assertEqual(inf, pool[2].CrowdingDistance)
        self.assertTrue(abs(0.7373417 - pool[0].CrowdingDistance) < epsilon)

    def test_isDominated(self):
        pool = unit_tests_helper.get_population()
        ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(pool)

        result_a = ParetoFrontHelper.isNotDominated(pool[0], pool)
        result_b = ParetoFrontHelper.isNotDominated(pool[0], pool)
        result_d = ParetoFrontHelper.isNotDominated(pool[0], pool)
        self.assertEquals(True, result_a, result_b)
        self.assertEquals(True, result_d)

        result_c = ParetoFrontHelper.isNotDominated(pool[2], pool)
        self.assertEqual(False, result_c)

    def test_slices_calculation(self):
        pool = unit_tests_helper.get_population()
        ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(pool)
        best_individuals = [pool[0], pool[1], pool[3]]
        sorted_bestIndividuals = sorted(best_individuals, key=lambda x: (x.Rank, x.SupervisorsFitness))
        sum_areas = ParetoFrontHelper.CalculateArea(sorted_bestIndividuals)

        expected_sum_area = 28

        self.assertEqual(expected_sum_area, sum_areas)


if __name__ == '__main__':
    unittest.main()
