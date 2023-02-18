import numpy
import random
from deap import base
from deap import creator
from deap import algorithms
from deap import tools

from objects.DNA import DNA
from objects.data_reader import DataReader
# from objects.data_writer import DataWriter
from objects.data_writer import DataWriter
from objects.project import Project
from objects.student import Student
from objects.supervisor import Supervisor

stu_data_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/students.txt"
sup_data_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/supervisors.txt"
proj_data_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/projects.txt"
dataReader = DataReader(sup_data_path, stu_data_path, proj_data_path)

# def main():
#



def fitness(solution):
    stu_list = dataReader.getStudentList()
    proj_list = dataReader.getProjectList()
    sup_list = dataReader.getSupervisorList()
    solution = solution[:len(stu_list)]
    sum = 0
    set_list = set(solution)
    if len(set_list) != len(solution):
        sum=-1
        return sum,

    for i in range(len(stu_list)):
        projIndex = solution[i]
        sup_id = proj_list[projIndex].supervisor_id
        if sup_list[sup_id].quota == 0:
            sum = -1
            return sum,
        else:
            sup_list[sup_id].quota -= 1
            if checkProjChosen(i, projIndex, stu_list):
                sum += calculateValue(projIndex, i, stu_list, proj_list, sup_list)
    return sum,

def checkProjChosen(studentID, projectID, studentList:list):
    set_stu_proj = set(studentList[studentID].projectList)
    if projectID in set_stu_proj:
        return True
    return False

def calculateValue(projectID, studentID, studentList: list, projectList: list, sup_list: list):
     projectPreference_stu = studentList[studentID].getProjectList()
     projectRank_stu = projectPreference_stu.index(projectID)
     weightRank_stu = [20, 7, 3, 2, 1]
     sup = projectList[projectID].getSupervisor()
     projectRank_sup = sup_list[sup].projectList.index(projectID)+1
     res = pow(weightRank_stu[projectRank_stu] * (1/projectRank_sup)*10, 2)
     return res




# GA Implementeed with DEAP
creator.create('FitnessMax', base.Fitness, weights=(1.0,))
creator.create('Individual', list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
IND_SIZE = 74
toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.indices)

# toolbox.register('attr_int', random.randint, a=0, b=4)
# toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attr_int, n=5)
toolbox.register('population', tools.initRepeat, list, toolbox.individual)
toolbox.register('evaluate', fitness)
toolbox.register('mate', tools.cxOnePoint)
toolbox.register('mutate', tools.mutUniformInt, low = 0, up = 73, indpb = 0.1)
toolbox.register('select', tools.selTournament, tournsize = 3)
population = toolbox.population(n=400)
crossover_probability = 0.5
mutation_probability = 0.1
number_of_generations = 30

statistics = tools.Statistics(key=lambda individual: individual.fitness.values)
statistics.register("max", numpy.max)
statistics.register("min", numpy.min)
statistics.register("med", numpy.mean)
statistics.register("std", numpy.std)

population, info = algorithms.eaSimple(population, toolbox,
                                       crossover_probability, mutation_probability,
                                       number_of_generations, statistics)
best_solution = tools.selBest(population, 1)
res_list = None
for individual in best_solution:
    print("The best:")
    print(individual[:31])
    res_list = individual[:31]
    print(individual.fitness)
stu_list = dataReader.getStudentList()
proj_list = dataReader.getProjectList()
sup_list = dataReader.getSupervisorList()
res_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/result.txt"
dataWriter = DataWriter()
dataWriter.getResultFile(res_list, sup_list, proj_list, stu_list, res_path)
# stu_list = dataReader.getStudentList()
# proj_list = dataReader.getProjectList()
# sup_list = dataReader.getSupervisorList()
# res_list = []
# for item in individual[:31]:
#     res_list.append(int(item))
# output_path = "/Users/suxingyu/Desktop/2nd project files/23_SPA_GA_Implementation/data/results.txt"
# dataWriter = DataWriter().getResultFile(res_list, sup_list, proj_list, output_path)


# def getData():
#     studentList = []
#     studentList.append(Student("Alex", 0, [13, 5, 3, 4, 2]))
#     studentList.append(Student("Lisa", 1, [1, 12, 7, 9, 3]))
#     studentList.append(Student("Linda", 2, [2, 11, 0, 3, 6]))
#     studentList.append(Student("Tom", 3, [11, 1, 7, 8, 9]))
#     studentList.append(Student("John", 4, [8, 7, 5, 12, 3]))
#
#     supervisorList = []
#     supervisorList.append(Supervisor("Robert", 0, [0, 1, 6, 7, 10], 5))
#     supervisorList.append(Supervisor("Ken", 1, [2, 5, 8, 11], 1))
#     supervisorList.append(Supervisor("Kelly", 2, [3, 4, 9, 12, 13], 4))
#
#     projectList = []
#     projectList.append(Project("0", supervisorList[0]))
#     projectList.append(Project("1", supervisorList[0]))
#     projectList.append(Project("2", supervisorList[1]))
#     projectList.append(Project("3", supervisorList[2]))
#     projectList.append(Project("4", supervisorList[2]))
#     projectList.append(Project("5", supervisorList[1]))
#     projectList.append(Project("6", supervisorList[0]))
#     projectList.append(Project("7", supervisorList[0]))
#     projectList.append(Project("8", supervisorList[1]))
#     projectList.append(Project("9", supervisorList[2]))
#     projectList.append(Project("10", supervisorList[0]))
#     projectList.append(Project("11", supervisorList[1]))
#     projectList.append(Project("12", supervisorList[2]))
#     projectList.append(Project("13", supervisorList[2]))
#
#     return studentList, supervisorList, projectList