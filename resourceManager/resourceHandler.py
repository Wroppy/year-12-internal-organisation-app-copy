from resourceManager.internalDataHandler import *
from resourceManager.databaseHandler import *
from display.timetableWidget.classClass import Class
from display.assignmentWidget.assignment import Assignment


class ResourceHandler:
    def __init__(self):
        dataBaseHandler = CloudDataBase()

    def returnAssignments(self) -> List[Assignment]:
        """
        Returns a list of assignments

        :return: List[Assignments]
        """
        data = loadJsonFile("data\\assignments")
        assignmentData = data["assignments"]

        # Adds the data the an array then returns it
        assignments = []
        for assignment in assignmentData:
            a = Assignment(assignment["assignmentName"], assignment["completed"])
            assignments.append(a)

        return assignments

    def addAssignment(self, assignmentName: str, completed: bool):
        """
        Adds an assignment to the file system

        :param assignmentName: str
        :param completed: bool
        :return: None
        """

        assignments = loadJsonFile("data\\assignments")
        assignment = {
            "assignmentName": assignmentName,
            "completed": completed
        }
        assignments["assignments"].append(assignment)
        writeJsonFile("data\\assignments", assignments)

    def updateAssignmentCompleted(self, index: int, checked: bool):
        """
        Updated an assignment's completed state

        :param index: int
        :param checked: bool
        :return: None
        """
        assignments = loadJsonFile("data\\assignments")

        assignments["assignments"][index]["completed"] = checked

        writeJsonFile("data\\assignments", assignments)

    def deleteAssignment(self, index: int):
        """
        Deletes an assignment from the internal database

        :param index: int
        :return: None
        """
        assigments = loadJsonFile("data\\assignments")

        assigments["assignments"].pop(index)

        writeJsonFile("data\\assignments", assigments)

    def returnClasses(self) -> List[List[Class]]:
        """
        Returns the classes from the internal database

        :return: List[List[Class]]
        """

        data = loadJsonFile("data\\timetable")
        timetable = data["classes"]

        # Adds it in a 2D array
        newTimetable = []
        for day in timetable:
            timetableDay = []
            for _class in day:
                _classObj = Class(_class["className"], _class["startingTime"], _class["endingTime"])
                timetableDay.append(_classObj)
            newTimetable.append(timetableDay)

        # returns [[Classes], [], [], [], [] ]
        return newTimetable

    def deleteClassFromfile(self, day: int, index: int):
        """
        Deletes a class from the file given the day and its index

        :param day: int
        :param index: int
        :return: None
        """
        timetable = loadJsonFile("data\\timetable")

        timetable["classes"][day].pop(index)

        writeJsonFile("data\\timetable", timetable)

    def addClassToFile(self, day: int, className: str, startingTime: int, endingTime: int):
        """
        Adds a class to the file given the day and its index

        :param day: int
        :param className: str
        :param startingTime: int
        :param endingTime: int
        :return: None
        """
        timetable = loadJsonFile("data\\timetable")

        _class = {
            "className": className,
            "startingTime": startingTime,
            "endingTime": endingTime
        }

        timetable["classes"][day].append(_class)

        writeJsonFile("data\\timetable", timetable)


if __name__ == '__main__':
    r = ResourceHandler()
    r.returnClasses()
