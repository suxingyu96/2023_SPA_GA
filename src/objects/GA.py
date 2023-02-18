import random
import logging
from objects.DNA import DNA

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('../../logs/GA.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class GA:
    def __init__(self, population_size: int, generation: int, num_stu: int, num_proj: int):
        self._population = self._initiate(population_size, num_stu, num_proj)
        self._generation = generation
        self._bestDNA = None
        self._bestDNA_fitness = -1

    def _initiate(self, population_size, num_stu, num_proj):
        logger.info('Initializing the first generation...')
        population = []
        for i in range(population_size):
            population.append(DNA(num_stu, num_proj))
        logger.info('The first generation of the population is generated successfully!')
        return population

    def getPopulation(self):
        return self._population

    def getGeneration(self):
        return self._generation

    def calculateFitness(self):
        currentBestDNA = None
        currentBestDNA_fitness = -1
        for i in self._population:
            fitness = i.getFitness()
            if fitness > self._bestDNA_fitness:
                self._bestDNA_fitness = fitness
                self._bestDNA = i
            if fitness > currentBestDNA_fitness:
                currentBestDNA = i
                currentBestDNA_fitness = fitness
        logger.info('The best solution ever is: ', self._bestDNA, ' the best fitness is: ', self._bestDNA_fitness)
        logger.info('The current best solution ever is: ', currentBestDNA, ' the current best fitness is: ',
                    currentBestDNA_fitness)
        return currentBestDNA, currentBestDNA_fitness

    def nextGeneration(self):
        newPopulation = []
        tour_size = 3
        for i in len(self._population):
            parent1 = self._tournament_selection(tour_size)
            parent2 = self._tournament_selection(tour_size)
            new_DNA = parent1.crossOver(parent2)
            new_DNA.mutate(0.1)
            newPopulation[i] = new_DNA
        self._generation += 1
        self._population = newPopulation
        logger.info('The no.', self._generation, 'generation of the population is generated')

    def _tournament_selection(self, tour_size):
        population_len = len(self._population)
        best_candidate_index = None
        best_candidate_fitness = -1
        for i in tour_size:
            candidate_index = random.randint(0, population_len - 1)
            if self._population[candidate_index].getFitness() > best_candidate_fitness:
                best_candidate_fitness = self._population[candidate_index].getFitness()
                best_candidate_index = candidate_index
        return self._population[best_candidate_index]


ga = GA(100, 20, 5, 40)
for dna in ga.getPopulation():
    print(dna.getDNA())
