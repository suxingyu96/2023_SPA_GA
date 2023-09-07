import unittest

from Benchmark import Benchmark
from GeneticAlgorithm.SPA_genetic_algorithm import SPA_genetic_algorithm
from objects.data_reader import DataReader


class aspTests(unittest.TestCase):

    def initialize_data(self):
        stu_data_path = str("../data/student_51.txt")
        sup_data_path = str("../data/supervisors.txt")
        proj_data_path = str("../data/projects.txt")

        dataReader = DataReader(sup_data_path, stu_data_path, proj_data_path)
        proj_list = dataReader.getProjectList()
        sup_list = dataReader.getSupervisorList()
        stu_list = dataReader.getStudentList()

        return stu_list, sup_list, proj_list

    def test_fromDataFiles(self):
        stu_list, sup_list, proj_list = self.initialize_data()
        # DataAnalysisHelper.selected_supervisor_analysis(stu_list, proj_list)
        # DataAnalysisHelper.selected_project_analysis(stu_list)
        # DataAnalysis.show_top_10_selected_projects(stu_list)
        pool_size = 600
        # mutation_rate = 1/(500 * 7)
        mutation_rate = 0.01
        crossover_rate = 0.8
        max_generations = 1000
        max_noImprovementCount = 100
        GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, pool_size, mutation_rate,
                                   crossover_rate, max_generations, max_noImprovementCount)
        bestIndividuals = GA.run(False)
        GA.displayIndividuals(bestIndividuals)

    def test_mutation_rates_fromBenchmark(self):
        stu_list, sup_list, proj_list = self.initialize_data()

        pool_size = 600
        mutation_rate_list = [float("{:.5f}".format(1 / (pool_size * 7))), 0.01, 0.05, 0.1]
        # mutation_rate_list = [float("{:.5f}".format(1/(700*7))), 0.01]
        pool_size = 500
        crossover_rate = 0.8
        max_generations = 500
        max_noImprovementCount = 20

        # running_times = 3
        title = "GA convergence with different mutation rates"
        y_labels = ["StudentsFitness", "SupervisorsFitness"]

        Benchmark.run_mutation_rates(stu_list, sup_list, proj_list, pool_size, mutation_rate_list,
                                     crossover_rate, max_generations, max_noImprovementCount)

    def test_crossover_rates_fromBenchmark(self):
        stu_list, sup_list, proj_list = self.initialize_data()

        pool_size = 600
        mutation_rate = 0.01
        # mutation_rate_list = [float("{:.5f}".format(1/(700*7))), 0.01]
        crossover_rates_list = [0.5, 0.8, 1]
        max_generations = 500
        max_noImprovementCount = 50

        Benchmark.run_crossover_rates(stu_list, sup_list, proj_list, pool_size, mutation_rate,
                                      crossover_rates_list, max_generations, max_noImprovementCount)

    def test_pool_sizes_fromBenchmark(self):
        stu_list, sup_list, proj_list = self.initialize_data()

        pool_sizes = [300, 600, 1000]

        mutation_rate = 0.01
        # mutation_rate_list = [float("{:.5f}".format(1/(700*7))), 0.01]
        crossover_rate = 0.8
        max_generations = 500
        max_noImprovementCount = 50

        Benchmark.run_population_sizes(stu_list, sup_list, proj_list, pool_sizes, mutation_rate,
                                       crossover_rate, max_generations, max_noImprovementCount)
