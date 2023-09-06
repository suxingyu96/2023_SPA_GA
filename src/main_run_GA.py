from Config import Config
from GeneticAlgorithm.SPA_genetic_algorithm import SPA_genetic_algorithm
from objects.data_reader import DataReader

def main():
    print('executing the main function')
    stu_data_path = Config.students_file_path
    sup_data_path = Config.supervisors_file_path
    proj_data_path = Config.projects_file_path

    dataReader = DataReader(sup_data_path, stu_data_path, proj_data_path)
    proj_list = dataReader.getProjectList()
    sup_list = dataReader.getSupervisorList()
    stu_list = dataReader.getStudentList()

    pool_size = Config.population_size
    mutation_rate = Config.mutation_rate
    crossover_rate = Config.crossover_rate
    visualize_data_screen = Config.data_visualization
    GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, pool_size, mutation_rate, crossover_rate)
    bestIndividuals = GA.run(visualize_data_screen)
    GA.displayIndividuals(bestIndividuals)


if __name__ == "__main__":
    main()