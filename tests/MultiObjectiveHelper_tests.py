import unittest
from math import inf
from MultiObjectiveHelper.MultiObjectiveHelper import MultiObjectiveHelper
from tests.GA_tests_helper import GA_tests_helper


class MyTestCase(unittest.TestCase):
    def test_rank_calculation(self):
        pool = GA_tests_helper.get_population()
        MultiObjectiveHelper.UpdatePopulationFitness(pool)
        self.assertEqual(pool[0].Rank, 1)
        self.assertEqual(pool[1].Rank, 1)
        self.assertEqual(pool[3].Rank, 1)
        self.assertEqual(pool[2].Rank, 2)

    def test_crowding_distance_calculation(self):
        pool = GA_tests_helper.get_population()
        MultiObjectiveHelper.UpdatePopulationFitness(pool)
        epsilon = 0.00001

        self.assertEqual(inf, pool[1].CrowdingDistance)
        self.assertEqual(inf, pool[3].CrowdingDistance)
        self.assertEqual(inf, pool[2].CrowdingDistance)
        self.assertTrue(abs(0.7373417 - pool[0].CrowdingDistance) < epsilon)

    def test_isDominated(self):
        pool = GA_tests_helper.get_population()
        MultiObjectiveHelper.UpdatePopulationFitness(pool)

        result_a = MultiObjectiveHelper.isNotDominated(pool[0], pool)
        result_b = MultiObjectiveHelper.isNotDominated(pool[0], pool)
        result_d = MultiObjectiveHelper.isNotDominated(pool[0], pool)
        self.assertEquals(True, result_a, result_b)
        self.assertEquals(True, result_d)

        result_c = MultiObjectiveHelper.isNotDominated(pool[2], pool)
        self.assertEqual(False, result_c)

    def test_slices_calculation(self):
        pool = GA_tests_helper.get_population()
        MultiObjectiveHelper.UpdatePopulationFitness(pool)
        best_individuals = [pool[0], pool[1], pool[3]]
        sorted_bestIndividuals = sorted(best_individuals, key=lambda x: (x.Rank, x.SupervisorsFitness))
        sum_ares = MultiObjectiveHelper.CalculateArea(sorted_bestIndividuals)

        expected_sum_area = 28

        self.assertEqual(expected_sum_area, sum_ares)


if __name__ == '__main__':
    unittest.main()
