import unittest
from GeneticAlgorithm.SPA_genetic_algorithm import SPA_genetic_algorithm
from objects.data_reader import DataReader


class aspTests(unittest.TestCase):
    def load_data(self, localFilePathList: list):
        stu_data_path = localFilePathList[0]
        sup_data_path = localFilePathList[1]
        proj_data_path = localFilePathList[2]
        dataReader = DataReader(sup_data_path, stu_data_path, proj_data_path)
        proj_list = dataReader.getProjectList()
        sup_list = dataReader.getSupervisorList()
        stu_list = dataReader.getStudentList()
        return stu_list, sup_list, proj_list

    def test_fromDataFiles(self):
        path_list = []

        stu_data_path = str("../data/student_51.txt")
        sup_data_path = str("../data/supervisors.txt")
        proj_data_path = str("../data/projects.txt")

        path_list.append(stu_data_path)
        path_list.append(sup_data_path)
        path_list.append(proj_data_path)

        stu_list, sup_list, proj_list = self.load_data(path_list)
        GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list)
        bestIndividuals = GA.run(True)
        GA.displayIndividuals(bestIndividuals)

