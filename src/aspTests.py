import unittest
from GeneticAlgorithm.SPA_genetic_algorithm import SPA_genetic_algorithm
from objects.data_reader import DataReader


class aspTests(unittest.TestCase):

    def test_fromDataFiles(self):
        stu_data_path = str("../data/student_51.txt")
        sup_data_path = str("../data/supervisors.txt")
        proj_data_path = str("../data/projects.txt")

        dataReader = DataReader(sup_data_path, stu_data_path, proj_data_path)
        proj_list = dataReader.getProjectList()
        sup_list = dataReader.getSupervisorList()
        stu_list = dataReader.getStudentList()

        pool_size = 500
        mutation_rate = 1/(500 * 7)
        GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, pool_size, mutation_rate)
        bestIndividuals = GA.run(False)
        GA.displayIndividuals(bestIndividuals)
