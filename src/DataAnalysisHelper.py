import time

from matplotlib import pyplot as plt
import numpy as np


class DataAnalysisHelper:
    @staticmethod
    def selected_project_analysis(stu_list):
        rank_to_projects = {}
        for student in stu_list:
            preference_list = student.getProjectList()

            for index in range(len(preference_list)):
                project = preference_list[index]
                rank = index + 1
                if rank in rank_to_projects:
                    current_projects = rank_to_projects[rank]
                    if project not in current_projects:
                        current_projects.append(project)
                        rank_to_projects.update({rank: current_projects})
                else:
                    rank_to_projects.update({rank: [project]})

        x = rank_to_projects.keys()
        y = []
        for projects in rank_to_projects.values():
            y.append(len(projects))

        title = "The distribution of selected projects"
        x_label = "Ranking"
        y_label = "Number of projects"
        DataAnalysisHelper.bar_chart_update(x, y, title, x_label, y_label)

    @staticmethod
    def bar_chart_update(x, y, title, x_label, y_label):
        plt.figure(figsize=(10, 6))
        plt.bar(x, y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        file_name = str(title) + str('.png')
        print(file_name)
        plt.savefig(file_name)
        # plt.show()


    @staticmethod
    def show_top_10_selected_projects(stu_list):
        selected_projects_to_num = {}
        for student in stu_list:
            preference_list = student.getProjectList()
            for project_id in preference_list:
                project = str(project_id)
                if project in selected_projects_to_num:
                    cur_num = selected_projects_to_num[project]
                    cur_num = cur_num + 1
                    selected_projects_to_num.update({project: cur_num})
                else:
                    selected_projects_to_num.update({project: 1})

        sorted_projects_to_num = sorted(selected_projects_to_num.items(), key=lambda x: x[1], reverse=True)
        top_10_projects = sorted_projects_to_num[:10]
        dict_top_10_projects = dict(top_10_projects)
        print(dict_top_10_projects)
        x = dict_top_10_projects.keys()
        for project in x:
            project = str(project)

        y = dict_top_10_projects.values()

        title = "The top 10 selected projects"
        x_label = "Project_id"
        y_label = "Number of students"
        DataAnalysisHelper.bar_chart_update(x, y, title, x_label, y_label)

    # @staticmethod
    # def __show_top_10_projects(projects_to_num):
    #
    #     plt.bar(x, y)
    #     plt.title("The top 10 selected projects")
    #     plt.xlabel('Project')
    #     plt.ylabel('Number of students')
    #     plt.show()

    @staticmethod
    def selected_supervisor_analysis(stu_list, proj_list):
        sup_to_stu_num = {}
        for student in stu_list:
            preference_list = student.getProjectList()
            sup_set = set()
            for project in preference_list:
                sup = proj_list[project].getSupervisor()
                sup = str(sup)
                if sup in sup_set:
                    continue
                else:
                    sup_set.add(sup)
                if sup not in sup_to_stu_num:
                    sup_to_stu_num.update({sup: 1})
                else:
                    cur_stu_num = sup_to_stu_num[sup]
                    cur_stu_num = cur_stu_num + 1
                    sup_to_stu_num.update({sup: cur_stu_num})

        sorted_sup_to_num = sorted(sup_to_stu_num.items(), key=lambda x: x[1], reverse=True)
        # sorted_sup_to_num_top_10 = sorted_sup_to_num[: 10]
        dict_sorted_sup_to_num = dict(sorted_sup_to_num)
        print(sorted_sup_to_num)
        x = dict_sorted_sup_to_num.keys()
        y = dict_sorted_sup_to_num.values()
        title = "The distribution of selected supervisors"
        x_label = "Supervisor id"
        y_label = "Number of students"
        DataAnalysisHelper.bar_chart_update(x, y, title, x_label, y_label)

    @staticmethod
    def show_convergence(results, title, y_labels, legend_title, timings):
        fig = plt.figure(figsize=(10, 6))
        fig.suptitle(title)
        ax_students = fig.add_subplot(2, 1, 1)
        ax_supervisors = fig.add_subplot(2, 1, 2)
        record_students = []
        record_supervisors = []
        parameters = []

        x_length = 0
        for records in results.values():
            x_length = max(x_length, len(records[0]))

        for parameter, timing in zip(results.keys(), timings):
            records = results[parameter]
            time_in_minutes = time.strftime("%M:%S", time.gmtime(timing))
            label = str(parameter) + "(" + str(time_in_minutes) + ")"
            parameters.append(str(label))
            for record in records:
                if len(record) < x_length:
                    last_one = record[-1]
                    while len(record) < x_length:
                        record.append(last_one)
            record_students.append(records[0])
            record_supervisors.append(records[1])

        x = np.arange(0, x_length * 5, 5)

        for i in range(len(record_students)):
            y_students_fitness = record_students[i]
            ax_students.plot(x, y_students_fitness)
            y_supervisors_fitness = record_supervisors[i]
            ax_supervisors.plot(x, y_supervisors_fitness)

        fig.legend(parameters, title=legend_title)
        # ax_supervisors.legend(parameters, title=legend_title)
        # ax_supervisors.legend(parameters)
        ax_students.set_xlabel("generation")
        ax_students.set_ylabel(y_labels[0])
        ax_supervisors.set_xlabel("generation")
        ax_supervisors.set_ylabel(y_labels[1])
        file_name = str(title) + str('.png')
        plt.savefig(file_name)
        plt.show()
