import copy
import statistics
import sys
import time

from DataAnalysisHelper import DataAnalysisHelper
from GeneticAlgorithm.SPA_genetic_algorithm import SPA_genetic_algorithm


class Benchmark:
    @staticmethod
    def initial_GA(stu_list, sup_list, proj_list, pool_size, mutation_rate,
                   crossover_rate, max_generations, max_noImprovementCount):
        print("benchmark run initialized")
        GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, pool_size, mutation_rate,
                                   crossover_rate, max_generations, max_noImprovementCount)
        first_population = GA.generate_first_population()
        return first_population

    @staticmethod
    def run_mutation_rates(stu_list, sup_list, proj_list, pool_size, mutation_rates,
                           crossover_rate, max_generations, max_noImprovementCount):
        title = "GA convergence with different mutation rates"
        y_labels = ["StudentsFitness", "SupervisorsFitness"]
        legend_title = "mutation rate"
        timings = []
        stdout = sys.stdout
        first_population = Benchmark.initial_GA(stu_list, sup_list, proj_list, pool_size, mutation_rates[0],
                                                crossover_rate, max_generations, max_noImprovementCount)
        print(first_population)
        # run 3 times and check the average performance and deviation
        results_statistics = {}
        for i in range(len(mutation_rates)):
            pool = copy.deepcopy(first_population)
            # sys.stdout = NullWriter()
            startTime = time.time()
            # new_function = function(stu_list, proj_list, sup_list, pool_size, mutation_rate, crossover_rate)
            print("benchmark run initialized")
            GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, pool_size, mutation_rates[i], crossover_rate,
                                       max_generations, max_noImprovementCount)
            GA.run(False, pool)
            print("benchmark run end!")
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            students_fitness_record, supervisors_fitness_record = GA.get_records()
            results_statistics.update({mutation_rates[i]: [students_fitness_record, supervisors_fitness_record]})
            print(seconds)
            # mean = statistics.mean(timings)
            # if i < 10 or i % 10 == 9:
            #     print("{0} {1:3.2f} {2:3.2f}".format(1 + i, mean,
            #                                          statistics.stdev(timings, mean) if i > 1 else 0))

        DataAnalysisHelper.show_convergence(results_statistics, title, y_labels, legend_title, timings)

    @staticmethod
    def run_crossover_rates(stu_list, sup_list, proj_list, pool_size, mutation_rate,
                            crossover_rates, max_generations, max_noImprovementCount):
        title = "GA convergence with different crossover rates"
        y_labels = ["StudentsFitness", "SupervisorsFitness"]
        legend_title = "crossover rate"
        timings = []
        stdout = sys.stdout
        print("benchmark run initialized")
        # run 3 times and check the average performance and deviation
        results_statistics = {}
        first_population = Benchmark.initial_GA(stu_list, sup_list, proj_list, pool_size, mutation_rate,
                                                crossover_rates[0], max_generations, max_noImprovementCount)
        print(first_population)
        for i in range(len(crossover_rates)):
            pool = copy.deepcopy(first_population)
            # sys.stdout = NullWriter()
            startTime = time.time()
            # new_function = function(stu_list, proj_list, sup_list, pool_size, mutation_rate, crossover_rate)
            print("benchmark run initialized")
            GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, pool_size, mutation_rate,
                                       crossover_rates[i], max_generations, max_noImprovementCount)
            GA.run(False, pool)
            print("benchmark run end!")
            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            students_fitness_record, supervisors_fitness_record = GA.get_records()
            results_statistics.update({crossover_rates[i]: [students_fitness_record, supervisors_fitness_record]})
            print(seconds)
            # mean = statistics.mean(timings)
            # if i < 10 or i % 10 == 9:
            #     print("{0} {1:3.2f} {2:3.2f}".format(1 + i, mean,
            #                                          statistics.stdev(timings, mean) if i > 1 else 0))

        DataAnalysisHelper.show_convergence(results_statistics, title, y_labels, legend_title, timings)

    @staticmethod
    def run_population_sizes(stu_list, sup_list, proj_list, pool_sizes, mutation_rate,
                             crossover_rate, max_generations, max_noImprovementCount):
        timings = []
        stdout = sys.stdout
        title = "GA convergence with different population sizes"
        y_labels = ["StudentsFitness", "SupervisorsFitness"]
        legend_title = "pool size"
        # run 3 times and check the average performance and deviation
        results_statistics = {}
        for i in range(len(pool_sizes)):
            # pool = copy.deepcopy(first_population)
            # sys.stdout = NullWriter()
            startTime = time.time()

            GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, pool_sizes[i], mutation_rate,
                                       crossover_rate, max_generations, max_noImprovementCount)
            GA.run(False)

            seconds = time.time() - startTime
            sys.stdout = stdout
            timings.append(seconds)
            students_fitness_record, supervisors_fitness_record = GA.get_records()
            results_statistics.update({pool_sizes[i]: [students_fitness_record, supervisors_fitness_record]})

        DataAnalysisHelper.show_convergence(results_statistics, title, y_labels, legend_title, timings)


class NullWriter():
    def getvalue(self):
        pass

    def write(self, s):
        pass
