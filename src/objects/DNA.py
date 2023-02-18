import random
import numpy.random

from objects.data_reader import DataReader


class DNA:
    def __init__(self, num_stu: int, num_proj: int):
        self._num_stu = num_stu
        self._num_proj = num_proj
        self._dna: list = self._generateDNA()
        self._fitness = -1

    def __generateDNA(self):
        random_dna = numpy.random.permutation(self._num_proj)
        dna = list(random_dna[:self._num_stu])
        return dna

    def getDNA(self):
        return self._dna

    def getFitness(self, stu_list, proj_list, sup_list):
        if self._fitness != -1:
            return self._fitness

        self._fitness = 0
        for i in range(len(self._dna)):
            projIndex = self._dna[i]
            sup_id = proj_list[projIndex].supervisor_id
            if sup_list[sup_id].quota == 0:
                self._fitness = 0
                return self._fitness
            else:
                sup_list[sup_id].quota -= 1
                if self._checkProjChosen(i, projIndex, stu_list):
                    self._fitness += self.__calculate_fitness(projIndex, i, stu_list, proj_list, sup_list)
        return self._fitness

    def __checkProjChosen(self, student_id, project_id, student_list:list):
        set_stu_proj = set(student_list[student_id].projectList)
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
        print(start, end)
        new_dna = self._dna[start:end]
        partner_dna = partner.getDNA()
        len_partner_dna = len(partner_dna)
        for i in range(len_partner_dna):
            if partner_dna[i] not in new_dna:
                new_dna.append(partner_dna[i])
            if len(new_dna) == len(self._dna):
                break;
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
# stu_data_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/students.txt"
# sup_data_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/supervisors.txt"
# proj_data_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/projects.txt"
# dataReader = DataReader(sup_data_path, stu_data_path, proj_data_path)
# stu_list = dataReader.getStudentList()
# proj_list = dataReader.getProjectList()
# sup_list = dataReader.getSupervisorList()


