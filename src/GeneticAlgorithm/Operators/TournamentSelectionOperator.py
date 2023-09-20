import random


class TournamentSelectionOperator:
    @staticmethod
    def get_candidates(pool):
        total_nums = len(pool) - 1
        index_1 = random.randint(0, total_nums)
        index_2 = random.randint(0, total_nums)
        while index_2 == index_1:
            index_2 = random.randint(0, total_nums)

        rival_1 = pool[index_1]
        rival_2 = pool[index_2]

        return rival_1, rival_2

    @staticmethod
    def tournamentSelection(rival_1, rival_2):
        if rival_1.Rank < rival_2.Rank:
            return rival_1
        elif rival_1.Rank == rival_2.Rank:
            if rival_1.CrowdingDistance > rival_2.CrowdingDistance:
                return rival_1
            else:
                return rival_2
        else:
            return rival_2