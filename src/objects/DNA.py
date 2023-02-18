import random
import numpy.random
import copy

from objects.data_reader import DataReader
from objects.supervisor import Supervisor


class DNA:
    def __init__(self, num_stu: int, num_proj: int):
        self._num_stu = num_stu
        self._num_proj = num_proj
        self._dna: list = self.__generateDNA()
        self._fitness = float('-inf')

    def __generateDNA(self):
        random_dna = numpy.random.permutation(self._num_proj)
        dna = list(random_dna[:self._num_stu])
        return dna

    def getDNA(self):
        return self._dna

    def getFitness(self, stu_list, proj_list, sup_list: list):
        copy_of_sup_list = copy.deepcopy(sup_list)
        print('Before calculating the fitness:', self._fitness)
        print('dna: ', self._dna )
        if self._fitness != float('-inf'):
            return self._fitness

        self._fitness = 0
        for i in range(len(self._dna)):
            projIndex = self._dna[i]
            sup_id = proj_list[projIndex].supervisor_id
            print('checked here')
            if copy_of_sup_list[sup_id].quota == 0:
                # should assign a random available  proj
                self._fitness = 0
                return self._fitness
            else:
                copy_of_sup_list[sup_id].quota -= 1
                if self._checkProjChosen(i, projIndex, stu_list):
                    ans = self.__calculate_fitness(projIndex, i, stu_list, proj_list, sup_list)
                    self._fitness = self._fitness + ans
                    print('after, fitness:', self._fitness)
        print('before return the fitness:', self._fitness)
        return self._fitness

    def _checkProjChosen(self, student_id, project_id, student_list:list):
        set_stu_proj = set(student_list[student_id].getProjectList())
        if project_id in set_stu_proj:
            return True
        return False

    def __calculate_fitness(self, project_id, student_id, student_list: list, project_list: list, sup_list: list):
        project_preferences_of_stu = student_list[student_id].getProjectList()
        project_rank_stu = project_preferences_of_stu.index(project_id)
        weight_rank_stu = [20, 7, 3, 2, 1]
        sup = project_list[project_id].getSupervisor()
        project_rank_sup = sup_list[sup].projectList.index(project_id)+1
        res = pow(weight_rank_stu[project_rank_stu] * (1/project_rank_sup)*10, 2)
        return res

    def crossOver(self, partner):
        start = random.randint(0, len(self._dna)-1)
        end = random.randint(start+1, len(self._dna))
        new_dna = self._dna[start:end]
        partner_dna = partner.getDNA()
        len_partner_dna = len(partner_dna)
        for i in range(len_partner_dna):
            if partner_dna[i] not in new_dna:
                new_dna.append(partner_dna[i])
            if len(new_dna) == len(self._dna):
                break
        # return new_dna
        self._dna = new_dna
        return self

    def mutate(self, mutationRate):
        for i in self._dna:
            randomRate = random.uniform(0, 1)
            if randomRate < mutationRate:
                random_proj = i
                while random_proj in self._dna:
                    random_proj = random.randint(0, self._num_proj-1)
                index = self._dna.index(i)
                self._dna[index] = random_proj
        return self



