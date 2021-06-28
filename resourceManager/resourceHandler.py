from resourceManager.internalDataHandler import *
from resourceManager.databaseConnector import *
from display.timetableWidget.classClass import Class
from display.assignmentWidget.assignment import Assignment
from datetime import datetime, time
from resourceManager.threadHandler import ThreadHandler


class ResourceHandler:
    def __init__(self):
        self.loggedIn = False
        self.userAccountKey = ""

    def generateKeyCode(self) -> str:
        """
        Returns a randomly generated key code

        :return: str
        """
        return "".join(str(random.randint(1, 9)) for _ in range(16))

    def returnAssignments(self) -> List[Assignment]:
        """
        Returns a list of assignments

        :return: List[Assignments]
        """
        assignmentsData = loadJsonFile("data\\assignments")

        assignments = []
        # Adds the data the an array then returns it
        for key in assignmentsData.keys():
            if not assignmentsData[key]["deleted"]:
                a = Assignment(assignmentsData[key]["assignmentName"], assignmentsData[key]["completed"], key)
                assignments.append(a)

        return assignments

    def addAssignment(self, assignmentName: str, completed: bool, keyCode: str):
        """
        Adds an assignment to the file system

        :param assignmentName: str
        :param completed: bool
        :param keyCode: stsr
        :return: None
        """

        currentTime = datetime.now()

        assignments = loadJsonFile("data\\assignments")
        assignment = {
            "assignmentName": assignmentName,
            "completed": completed,
            "deleted": False,
            "lastUpdated": {
                "year": currentTime.year,
                "month": currentTime.month,
                "day": currentTime.day,
                "hour": currentTime.hour,
                "minute": currentTime.minute,
                "second": currentTime.second
            }
        }

        assignments[keyCode] = assignment
        writeJsonFile("data\\assignments", assignments)

    def updateAssignmentCompleted(self, keyCode: str, checked: bool):
        """
        Updated an assignment's completed state

        :param index: str
        :param checked: bool
        :return: None
        """
        assignments = loadJsonFile("data\\assignments")

        assignments[keyCode]["completed"] = checked

        currentTime = datetime.now()
        assignments[keyCode]["lastUpdated"] = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }

        writeJsonFile("data\\assignments", assignments)

    def deleteAssignment(self, keyCode: str):
        """
        Deletes an assignment from the internal database

        :param index: int
        :return: None
        """

        assignments = loadJsonFile("data\\assignments")

        assignments[keyCode]["deleted"] = True
        print(assignments[keyCode]["deleted"])
        print(assignments[keyCode])
        currentTime = datetime.now()
        assignments[keyCode]["lastUpdated"] = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }

        print(assignments)

        writeJsonFile("data\\assignments", assignments)

    def returnClasses(self) -> List[List[Class]]:
        """
        Returns the classes from the internal database

        :return: List[List[Class]]
        """

        data = loadJsonFile("data\\timetable")
        timetable = data["classes"]

        # Creates a datetime class of the time it was last updated
        key = "lastUpdated"
        lastUpdated = datetime(
                    year=data[key]["year"],
                    month=data[key]["month"],
                    day=data[key]["day"],
                    hour=data[key]["hour"],
                    minute=data[key]["minute"],
                    second=data[key]["second"]
                )

        # Adds it in a 2D array
        newTimetable = []
        for day in timetable:
            timetableDay = []
            for _class in day:


                # Creates the starting time class
                startingTime = time(_class["startingTime"]["hour"], _class["startingTime"]["minute"])

                # Creates the ending time class
                endingTime = time(_class["endingTime"]["hour"], _class["endingTime"]["minute"])

                _classObj = Class(_class["className"], startingTime, endingTime, lastUpdated)
                timetableDay.append(_classObj)
            newTimetable.append(timetableDay)

        # returns [[Classes], [], [], [], [] ]
        return newTimetable

    def deleteClassFromfile(self, day: int, index: int, currentTime: datetime):
        """
        Deletes a class from the file given the day and its index

        :param day: int
        :param index: int
        :return: None
        """
        timetable = loadJsonFile("data\\timetable")

        timetable["classes"][day].pop(index)

        timetable["lastUpdated"] = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }

        writeJsonFile("data\\timetable", timetable)

    def addClassToFile(self, day: int, className: str, startingTime: time, endingTime: time, currentTime: datetime):
        """
        Adds a class to the file given the day and its index

        :param day: int
        :param className: str
        :param startingTime: int
        :param endingTime: int
        :param currentTime: datetime
        :return: None
        """
        timetable = loadJsonFile("data\\timetable")

        _class = {
            "className": className,
            "startingTime": {
                "hour": startingTime.hour,
                "minute": startingTime.minute
            },
            "endingTime": {
                "hour": endingTime.hour,
                "minute": endingTime.minute
            }
        }

        timetable["classes"][day].append(_class)

        timetable["lastUpdated"] = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }

        writeJsonFile("data\\timetable", timetable)

    def loadClassFromDatabase(self, userKeyCode: int):
        loadedTimetable = self.dataBaseHandler.loadTimetable(userKeyCode)

        timetable = [[], [], [], [], []]

        for row in loadedTimetable:
            day = row

            className = row[0]
            beginningTime = row[1]
            endingTime = row[2]

            yearUpdated = row[3]
            monthUpdated = row[4]
            dayUpdated = row[5]
            hourUpdated = row[6]
            minuteUpdated = row[7]
            secondUpdated = row[8]

            timeUpdated = datetime(yearUpdated, monthUpdated, dayUpdated, hourUpdated, minuteUpdated, secondUpdated)

    def isLoggedIn(self):
        return self.loggedIn

    def loggedInFalse(self):
        self.loggedIn = False

    def loggedInTrue(self):
        self.loggedIn = True

    def getAccountKey(self):
        userAccountKey = loadJsonFile("data\\account")["accountKey"]

        if userAccountKey != None:
            self.userAccountKey = userAccountKey


    def logIn(self, username: str, password: str):
        pass


if __name__ == '__main__':
    r = ResourceHandler()
    r.returnClasses()
