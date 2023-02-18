import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('../../logs/supervisors_data.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Supervisor:

    def __init__(self, name, supID, projectList: list, quota: int):
        self.name = name
        self.supID = supID
        self.projectList = projectList
        self.quota = quota
        logger.info(self.supID, ' ', self.name, ' ', self.quota, ' ', self.projectList)

    def getSupervisorName(self):
        return self.name

    def getSupervisorID(self):
        return self.supID

    def getProjectList(self):
        return self.projectList

    def getQuota(self):
        return self.quota
