import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('../../logs/students_data.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Student:

    def __init__(self, name, stuID, projectList: list, project_id=None):
        self.__name = name
        self.__stuID = stuID
        self.__projectList = projectList
        self.__project_id = None
        logger.info(self.__stuID, ' ', self.__name, ' ', self.__projectList)

    def getStudentName(self):
        return self.__name

    def getStudentID(self):
        return self.__stuID

    def getProjectList(self):
        return self.__projectList
