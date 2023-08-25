class DataWriter:
    def getResultFile(self, res_list: list, sup_list: list, proj_list: list, stu_list: list, output_path: str):
        file = open(output_path, "w")
        satisfied_levels = ['Extremly satisfied', 'Very satisfied', 'Satisfied', 'Good', 'Not bad', 'Unsatisfied']
        satisfied_levels_stat = [0, 0, 0, 0, 0, 0]
        for sup in sup_list:
            print("initial quota:", sup.quota)

        for i in range(len(res_list)):
            proj = res_list[i]
            sup = proj_list[proj].supervisor_id
            sup_list[sup].quota -= 1
            if proj in stu_list[i].getProjectList():
                rank = stu_list[i].getProjectList().index(proj)
                satisfied_level = satisfied_levels[rank]
                satisfied_levels_stat[rank] = satisfied_levels_stat[stu_list[i].getProjectList().index(proj)] + 1
            else:
                satisfied_level = satisfied_levels[5]
                satisfied_levels_stat[5] += 1
            content = "student:{0} is assigned project:{1} and the supervisor is: {2}, level: {3} \n" \
                .format(i, res_list[i], sup_list[sup].name, satisfied_level)
            file.write(content)

        for i in range(len(satisfied_levels)):
            stat = "{0}: {1}\n".format(satisfied_levels[i], ": ", str(satisfied_levels_stat[i]))
            file.write(stat)

        for i in range(len(sup_list)):
            content = "{0}'s quota left: {1}\n".format(sup_list[i].name, sup_list[i].quota)
            file.write(content)
        file.close()
