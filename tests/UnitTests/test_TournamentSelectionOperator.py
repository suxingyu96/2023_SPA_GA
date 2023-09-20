import unittest
from GeneticAlgorithm.Operators.TournamentSelectionOperator import TournamentSelectionOperator
from tests.UnitTests.unit_tests_helper import unit_tests_helper
from GeneticAlgorithm.ParetoFrontHelper import ParetoFrontHelper


class TournamentSelectionOperatorsTests(unittest.TestCase):
    def test_get_candidates_unique(self):
        pool = unit_tests_helper.get_population()

        for i in range(10):
            candidate_a, candidate_b = TournamentSelectionOperator.get_candidates(pool)
            self.assertNotEqual(candidate_a, candidate_b)

    def test_tournament_selection_by_rank(self):
        pool = unit_tests_helper.get_population()
        ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(pool)
        rival_1 = pool[0]
        rival_2 = pool[2]
        winner = TournamentSelectionOperator.tournamentSelection(rival_1, rival_2)
        self.assertEqual(rival_1, winner)

        winner = TournamentSelectionOperator.tournamentSelection(rival_2, rival_1)
        self.assertEqual(rival_1, winner)

    def test_tournament_selection_by_crowding_distance(self):
        pool = unit_tests_helper.get_population()
        ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(pool)
        rival_1 = pool[1]
        rival_2 = pool[0]
        winner = TournamentSelectionOperator.tournamentSelection(rival_1, rival_2)
        self.assertEqual(rival_1, winner)

        winner = TournamentSelectionOperator.tournamentSelection(rival_2, rival_1)
        self.assertEqual(rival_1, winner)


if __name__ == '__main__':
    unittest.main()
