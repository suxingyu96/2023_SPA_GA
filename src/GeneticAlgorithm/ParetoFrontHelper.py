import copy
from itertools import groupby
from operator import attrgetter
from objects.Slice import Slice
from scipy.spatial import distance


class ParetoFrontHelper:

    @staticmethod
    def UpdatePopulationRankAndCrowdingDistance(pool):
        for individual in pool:
            individual.Rank = -1
            individual.CrowdingDistance = -1

        ParetoFrontHelper.NormalizeFitnessValues(pool)

        remainingToBeRanked = copy.deepcopy(pool)
        rank = 1
        while len(remainingToBeRanked) > 0:
            individualsInRank = []

            for i in range(len(remainingToBeRanked)):
                individual = remainingToBeRanked[i]

                if ParetoFrontHelper.isNotDominated(individual, remainingToBeRanked):
                    index = pool.index(individual)
                    pool[index].Rank = rank
                    individual.Rank = rank
                    individualsInRank.append(individual)

            for i in individualsInRank:
                remainingToBeRanked.remove(i)

            rank = rank + 1
        sorted_pool = sorted(pool, key=lambda x: x.Rank)

        ranks = []
        for k, g in groupby(sorted_pool, lambda x: x.Rank):
            ranks.append(list(g))
        for singleRank in ranks:
            ParetoFrontHelper.CalculateCrowdingDistance(singleRank)

        return sorted_pool

    @staticmethod
    def NormalizeFitnessValues(pool):
        maxStudentsFitness = max(pool, key=attrgetter('StudentsFitness')).StudentsFitness
        maxSupervisorFitness = max(pool, key=attrgetter('SupervisorsFitness')).SupervisorsFitness

        for individual in pool:
            individual.NormalizedStudentsFitness = individual.StudentsFitness / maxStudentsFitness
            individual.NormalizedSupervisorsFitness = individual.SupervisorsFitness / maxSupervisorFitness

    @staticmethod
    def isNotDominated(individual, remainingToBeRanked):
        for anotherIndividual in remainingToBeRanked:
            # if anotherIndividual.StudentsFitness > individual.StudentsFitness:
            #         if the 'anotherIndividual' is better than 'individual' at least one objective
            #         and equal in other objectives
            if (anotherIndividual.StudentsFitness > individual.StudentsFitness
                and anotherIndividual.SupervisorsFitness >= individual.SupervisorsFitness) \
                    or (anotherIndividual.StudentsFitness >= individual.StudentsFitness
                        and anotherIndividual.SupervisorsFitness > individual.SupervisorsFitness):
                return False
        return True

    @staticmethod
    def CalculateCrowdingDistance(singleRank):
        def CalculateEuclideanDistance(pointA, pointB):
            return distance.euclidean((pointA.NormalizedStudentsFitness,
                                       pointA.NormalizedSupervisorsFitness),
                                      (pointB.NormalizedStudentsFitness,
                                       pointB.NormalizedSupervisorsFitness))

        sortedIndividuals = sorted(singleRank, key=lambda individual: individual.NormalizedStudentsFitness)
        individualsInFront = len(sortedIndividuals)

        for i in range(individualsInFront):
            # if the individual is the first one or the last one, it should have infinite crowding distance
            if i == 0 or i == individualsInFront - 1:
                sortedIndividuals[i].CrowdingDistance = float('inf')
            else:
                currentIndividual = sortedIndividuals[i]
                leftIndividual = sortedIndividuals[i - 1]
                rightIndividual = sortedIndividuals[i + 1]

                # Get the position on the fitness graph where studentFitness is the X axis,
                # supervisorsFitness is the Y axis
                distanceLeft = CalculateEuclideanDistance(leftIndividual, currentIndividual)
                distanceRight = CalculateEuclideanDistance(rightIndividual, currentIndividual)
                crowding_distance = distanceLeft + distanceRight
                sortedIndividuals[i].CrowdingDistance = crowding_distance

    @staticmethod
    def CalculateArea(bestIndividuals):
        slice_list = ParetoFrontHelper.getSlices(bestIndividuals)
        sum_area = 0
        for slice in slice_list:
            sum_area += slice.Area

        return sum_area

    @staticmethod
    def getSlices(Individuals):
        preSlice = Slice(0, 0, 0, 0)
        slices = []

        for i in Individuals:
            preSlice = Slice(i.SupervisorsFitness, preSlice.XUpper, i.StudentsFitness, 0)
            slices.append(preSlice)

        return slices
