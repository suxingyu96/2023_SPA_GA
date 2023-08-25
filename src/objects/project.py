class Project:
    def __init__(self, projectID, supervisor_id):
        self.projectID = projectID
        # self.student = student
        self.supervisor_id = supervisor_id


    def getSupervisor(self):
        return self.supervisor_id

    def __str__(self):
        return str(self.projectID)