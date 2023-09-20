from GeneticAlgorithm.SPA_genetic_algorithm import SPA_genetic_algorithm
from objects.Chromosome import Chromosome


class unit_tests_helper:
    @staticmethod
    def get_GA():
        stu_list = []
        proj_list = []
        sup_list = []
        max_generations = 50
        max_noImprovementCount =5
        GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, 0, 0.01, 1, max_generations, max_noImprovementCount)
        return GA

    @staticmethod
    def get_population():
        chromosome_a = Chromosome([1])
        chromosome_a.StudentsFitness = 5
        chromosome_a.SupervisorsFitness = 4

        chromosome_b = Chromosome([2])
        chromosome_b.StudentsFitness = 7
        chromosome_b.SupervisorsFitness = 2

        chromosome_c = Chromosome([3])
        chromosome_c.StudentsFitness = 2
        chromosome_c.SupervisorsFitness = 1

        chromosome_d = Chromosome([4])
        chromosome_d.StudentsFitness = 4
        chromosome_d.SupervisorsFitness = 5

        pool = [chromosome_a, chromosome_b, chromosome_c, chromosome_d]
        return pool

