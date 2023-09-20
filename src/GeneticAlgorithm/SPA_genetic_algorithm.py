import copy
import random
import time
import numpy as np
from itertools import groupby

from GeneticAlgorithm.Operators.CrossoverOperators import CrossoverOperators
from GeneticAlgorithm.Operators.MutationOperators import MutationOperators
from GeneticAlgorithm.Operators.TournamentSelectionOperator import TournamentSelectionOperator
from GeneticAlgorithm.ParetoFrontHelper import ParetoFrontHelper
from objects.Chromosome import Chromosome
from objects.ParetoVisualScreen import ParetoVisualScreen


class SPA_genetic_algorithm:
    def __init__(self, stu_list, proj_list, sup_list, pool_size, mutate_rate,
                 crossover_rate, max_generations, max_noImprovementCount):
        self._numParents = pool_size
        self._mutate_rate = mutate_rate
        self._stu_list = stu_list
        self._proj_list = proj_list
        self._sup_list = sup_list
        self._geneSet = self.__create_gene_set()
        self._pool = self.generate_first_population()
        self._max_generations = max_generations
        self._max_noImprovementCount = max_noImprovementCount
        self._crossover_rate = crossover_rate
        self._best_students_fitness_record = []
        self._best_supervisors_fitness_record = []
        self._generation = 0
        self._bestIndividuals = []

    def generate_first_population(self):
        pool = []
        while len(pool) < self._numParents:
            genes = self.generate_parent()
            if genes not in pool:
                pool.append(genes)

        for i in range(len(pool)):
            genes = pool[i]
            individual = Chromosome(genes)
            pool[i] = individual
        return pool

    def run(self, paretoScreen=False, pool=None):
        if pool is not None:
            print(pool)
            self._pool = pool
        print('generation', self._generation)
        self.CalculateStudentsFitness(self._pool)
        self.CalculateSupervisorsFitness(self._pool)
        self._pool = ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(self._pool)

        if paretoScreen:
            paretoFrontWindow = ParetoVisualScreen()

        # Termination Condition
        isConverged = False
        NoImprovementCount = 0
        preConvergenceArea = 0

        while not isConverged:
            if paretoScreen:
                paretoFrontWindow.Update(self._pool, self._generation)
                time.sleep(1)

            self._bestIndividuals = self.getBestIndividuals()
            if self._generation % 4 == 0:
                self.__record_current_best_fitness()

            print("No.{0} Generation:".format(self._generation),
                  'total num:', len(self._pool),
                  'mutation rate', self._mutate_rate)
            print('The bests:', len(self._bestIndividuals))
            self.displayIndividuals(self._bestIndividuals)

            # produce offspring
            offspring = self.generateOffspring()
            self._pool.extend(offspring)
            self._pool = ParetoFrontHelper.UpdatePopulationRankAndCrowdingDistance(self._pool)

            # Sort all individuals and produce new population
            newPopulation = []
            sorted_pool = sorted(self._pool, key=lambda x: (x.Rank, 0 - x.CrowdingDistance))
            for i in sorted_pool:
                if i not in newPopulation and i.CrowdingDistance != 0:
                    newPopulation.append(i)
                if len(newPopulation) >= 0.9 * self._numParents:
                    break

            while len(newPopulation) < self._numParents:
                randomIndividual = random.choice(sorted_pool)
                if randomIndividual not in newPopulation and randomIndividual.Rank != -1:
                    newPopulation.append(randomIndividual)

            self._pool.clear()
            self._pool = newPopulation
            self._generation += 1
            NoImprovementCount, preConvergenceArea = self.__update_no_improvement_count_and_area \
                (NoImprovementCount, preConvergenceArea)
            isConverged = self._generation >= self._max_generations or NoImprovementCount > self._max_noImprovementCount
        return self._bestIndividuals

    def __update_no_improvement_count_and_area(self, NoImprovementCount, preConvergenceArea):
        sorted_bestIndividuals = sorted(self._bestIndividuals, key=lambda x: x.SupervisorsFitness)
        curArea = ParetoFrontHelper.CalculateArea(sorted_bestIndividuals)
        if abs(curArea - preConvergenceArea) < 0.01 * preConvergenceArea:
            NoImprovementCount += 1
        else:
            NoImprovementCount = 0
            preConvergenceArea = curArea
        return NoImprovementCount, preConvergenceArea

    def __record_current_best_fitness(self):
        if len(self._bestIndividuals) < 2:
            individual_a, individual_b = self._bestIndividuals[0]
        else:
            individual_a, individual_b = self._bestIndividuals[0], self._bestIndividuals[1]

        best_supervisors_fitness = max(individual_a.SupervisorsFitness, individual_b.SupervisorsFitness)
        best_students_fitness = max(individual_a.StudentsFitness, individual_b.StudentsFitness)
        self._best_supervisors_fitness_record.append(best_supervisors_fitness)
        self._best_students_fitness_record.append(best_students_fitness)

    def get_records(self):
        return self._best_students_fitness_record, self._best_supervisors_fitness_record

    def __create_gene_set(self):
        geneSet = []
        for i in self._proj_list:
            project_id = i.projectID
            geneSet.append(project_id)

        return geneSet

    def generate_parent(self):
        len_of_genes = len(self._stu_list)
        return random.sample(self._geneSet, len_of_genes)

    def generateOffspring(self):
        offspring = []

        while len(offspring) < 0.95 * len(self._pool):
            children_genes = []

            parent, donor = self.generate_parent_and_donor()

            rate = random.uniform(0, 1)
            if rate < self._crossover_rate:
                children_gene_a = self.DoCrossover(parent, donor)
            else:
                child = TournamentSelectionOperator.tournamentSelection(parent, donor)
                children_gene_a = copy.deepcopy(child.getGenes())

            children_genes.append(children_gene_a)

            for child_genes in children_genes:
                self.DoMutation(child_genes)
                child_chromosome = Chromosome(child_genes)
                while not self.__is_child_acceptable(child_chromosome, offspring):
                    self.DoMutation(child_genes)
                    child_chromosome = Chromosome(child_genes)
                offspring.append(child_chromosome)

        self.CalculateStudentsFitness(offspring)
        self.CalculateSupervisorsFitness(offspring)
        return offspring

    def generate_parent_and_donor(self):
        candidate_a, candidate_b = TournamentSelectionOperator.get_candidates(self._pool)
        parent = TournamentSelectionOperator.tournamentSelection(candidate_a, candidate_b)
        candidate_a, candidate_b = TournamentSelectionOperator.get_candidates(self._pool)
        donor = TournamentSelectionOperator.tournamentSelection(candidate_a, candidate_b)
        while parent == donor:
            candidate_a, candidate_b = TournamentSelectionOperator.get_candidates(self._pool)
            donor = TournamentSelectionOperator.tournamentSelection(candidate_a, candidate_b)
        return parent, donor

    def __is_child_acceptable(self, child, offspring):
        if child in self._pool or child in offspring:
            return False
        return True

    def CalculateStudentsFitness(self, pool):
        for individual in pool:
            selectedProjectsRank = [0, 0, 0, 0, 0]
            individual_genes = individual.getGenes()
            for i in range(len(individual_genes)):
                stu_proj_preference_list = self._stu_list[i].getProjectList()
                #         check if the student chose this project and get the rank
                if individual_genes[i] in stu_proj_preference_list:
                    proj_rank = stu_proj_preference_list.index(individual_genes[i])
                    selectedProjectsRank[proj_rank] += 1
            individual.All_Project_Ranks = selectedProjectsRank
            studentFitness = 25 * selectedProjectsRank[0] \
                             + 16 * selectedProjectsRank[1] \
                             + 9 * selectedProjectsRank[2] + \
                             4 * selectedProjectsRank[3] \
                             + 1 * selectedProjectsRank[4]
            individual.StudentsFitness = studentFitness + 1

    def CalculateSupervisorsFitness(self, pool):
        for individual in pool:
            selectedSupervisorsAndNum = {}
            individual_genes = individual.getGenes()
            oversubscribedProjectIDAndSupervisors = {}
            for i in range(len(individual_genes)):
                sup_id = self._proj_list[individual_genes[i]].getSupervisor()
                if sup_id not in selectedSupervisorsAndNum:
                    selectedSupervisorsAndNum.update({sup_id: [individual_genes[i]]})
                else:
                    existing_projectlist = selectedSupervisorsAndNum[sup_id]
                    existing_projectlist.append(individual_genes[i])
                    selectedSupervisorsAndNum.update({sup_id: existing_projectlist})
                cur_num = len(selectedSupervisorsAndNum[sup_id])
                quota = self._sup_list[sup_id].quota
                if cur_num > quota:
                    if sup_id not in oversubscribedProjectIDAndSupervisors.keys():
                        oversubscribedProjectIDAndSupervisors.update({sup_id: [sup_id]})

            fitness_workload = 0
            fitness_satisfaction = 0
            if len(oversubscribedProjectIDAndSupervisors) > 0:
                individual.SupervisorsFitness = 0 - len(oversubscribedProjectIDAndSupervisors)
                continue
            else:
                for sup, selected_proj_list in selectedSupervisorsAndNum.items():
                    quota = self._sup_list[sup].getQuota()
                    cur_stu_num = len(selected_proj_list)
                    if cur_stu_num > quota:
                        fitness_workload = 0 - len(oversubscribedProjectIDAndSupervisors)
                        break
                    else:
                        fitness_workload = fitness_workload + (quota - cur_stu_num) * 2 ^ 2
                        sup_preference_list = self._sup_list[sup].getProjectList()

                        for proj in selected_proj_list:
                            rank = sup_preference_list.index(proj)
                            fitness_satisfaction = fitness_satisfaction + (5 - rank) ^ 2
            individual.SupervisorsFitness = fitness_satisfaction + fitness_workload
            sorted_list_selectedSupervisorsAndNum = sorted(selectedSupervisorsAndNum.items())
            sorted_selectedSupervisorsAndNum = dict(sorted_list_selectedSupervisorsAndNum)
            individual.SelectedSupervisorsAndProjects = sorted_selectedSupervisorsAndNum

    def DoMutation(self, child_genes):
        for i in range(len(child_genes)):
            rate = random.uniform(0, 1)
            self._mutate_rate = 1 - self._generation / self._max_generations
            if rate < self._mutate_rate:
                child_genes = self.mutate(child_genes)

    def DoCrossover(self, parent, donor):
        start, end = self._generate_two_points()
        child_gene = CrossoverOperators.crossover_PMX(parent.getGenes(), donor.getGenes(), start, end)
        return child_gene

    def getBestIndividuals(self):
        sorted_pool = sorted(self._pool, key=lambda x: (x.Rank, 0 - x.CrowdingDistance))
        ranks = []
        for k, g in groupby(sorted_pool, lambda x: x.Rank):
            ranks.append(list(g))
        return ranks[0]

    def mutate(self, genes):
        mutation_strategies = ['inversion', 'rotation', 'scramble', 'swap']
        mutation_strategy = random.choice(mutation_strategies)
        start, end = self._generate_two_points()
        if mutation_strategy is 'rotation':
            return MutationOperators.rotation_mutation(genes, start, end)
        elif mutation_strategy is 'inversion':
            return MutationOperators.inversion_mutation(genes, start, end)
        elif mutation_strategy is 'scramble':
            return MutationOperators.scramble_mutation(genes, start, end)
        elif mutation_strategy is 'swap':
            return MutationOperators.swap_mutation(genes, start, end)

    def _generate_two_points(self):
        range_of_points = len(self._stu_list)
        point_1, point_2 = np.random.choice(range_of_points, 2)
        while point_1 == point_2:
            point_1, point_2 = np.random.choice(range_of_points, 2)
        start, end = min([point_1, point_2]), max([point_1, point_2])
        return start, end

    def displayIndividuals(self, individuals):
        for i in individuals:
            print(i.getGenes())
            print('Rank', i.Rank)
            print('i', i.All_Project_Ranks)
            print(i.CrowdingDistance)
            sup = i.SelectedSupervisorsAndProjects
            # num_list = []
            # for projs in sup.values():
            #     num_list.append(len(projs))
            print('supervisors:', sup)
            # selectedlist_supAndproj = i.SelectedSupervisorsAndProjects
            # for k, v in selectedlist_supAndproj.items():
            #     print('sup: ', k, ' num: ', len(v))
            # print(i.StudentsFitness)
            print('Supervisors:', i.SupervisorsFitness)
            print('Students:', i.StudentsFitness)
        print('---------------------------------------------')
