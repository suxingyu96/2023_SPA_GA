import random
import logging
from objects.DNA import DNA

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('../logs/GA.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class GA:
    def __init__(self, population_size: int, generation: int, stu_list, proj_list, sup_list):
        self._stu_list = stu_list
        self._proj_list = proj_list
        self._sup_list = sup_list
        self._num_stu = len(self._stu_list)
        self._num_proj = len(self._proj_list)
        self._population_size = population_size
        # self._population = self._initiate(population_size, len(self._stu_list), len(self._proj_list))
        self._population = self.initiate()
        self._generation = 1
        first_best_DNA = self.calculateFitness()
        self._bestDNA = first_best_DNA[0]
        self._bestDNA_fitness = first_best_DNA[1]


    def initiate(self):
        logger.info('Initializing the first generation...')
        population = []
        for i in range(self._population_size):
            population.append(DNA(self._num_stu, self._num_proj))
        logger.info('The first generation of the population is generated successfully!')
        return population
        # return population

    def getPopulation(self):
        return self._population

    def getGeneration(self):
        return self._generation

    def calculateFitness(self):
        currentBestDNA = None
        currentBestDNA_fitness = -1
        for i in self._population:
            fitness = i.getFitness(self._stu_list, self._proj_list, self._sup_list)
            if self._generation != 1:
                if fitness > self._bestDNA_fitness:
                    self._bestDNA_fitness = fitness
                    self._bestDNA = i
            if fitness > currentBestDNA_fitness:
                currentBestDNA = i
                currentBestDNA_fitness = fitness
                # log_info = 'The best solution ever is: ' + str(self._bestDNA), ' the best fitness is: ' + str(self._bestDNA_fitness)
                # logger.info(log_info)
        logger.info('The current best solution ever is: ' + str(currentBestDNA) + str(' the current best fitness is: ')
                    + str(currentBestDNA_fitness))
        return currentBestDNA, currentBestDNA_fitness

    def nextGeneration(self):
        newPopulation = []
        tour_size = 3
        for i in range(self._population_size):
            parent1 = self._tournament_selection(tour_size)
            parent2 = self._tournament_selection(tour_size)
            new_DNA = parent1.crossOver(parent2)
            new_DNA.mutate(0.1)
            newPopulation.append(new_DNA)
        self._generation += 1
        self._population = newPopulation
        log_info = 'The no.' + str(self._generation) + ' generation of the population is generated'
        self.calculateFitness()
        logger.info(log_info)

    def _tournament_selection(self, tour_size):
        population_len = len(self._population)
        best_candidate_index = -1
        best_candidate_fitness = -1
        for i in range(tour_size):
            candidate_index = random.randint(0, population_len - 1)
            if self._population[candidate_index].getFitness(self._stu_list, self._proj_list,
                                                            self._sup_list) > best_candidate_fitness:
                best_candidate_fitness = self._population[candidate_index].getFitness(self._stu_list, self._proj_list,
                                                                                      self._sup_list)
                best_candidate_index = candidate_index
        return self._population[best_candidate_index]

    def getBestDNA(self):
        return self._bestDNA, self._bestDNA_fitness
