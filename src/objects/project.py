from objects.supervisor import Supervisor
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('../../logs/projects_data.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
class Project:
    def __init__(self, projectID, supervisor_id):
        self.projectID = projectID
        # self.student = student
        self.supervisor_id = supervisor_id
        logger.info('Project ID: ', self.projectID, ' Supervisor ID:', self.supervisor_id)

    def getSupervisor(self):
        return self.supervisor_id
