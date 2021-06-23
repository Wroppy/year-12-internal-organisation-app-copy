from resourceManager.internalDataHandler import *
from resourceManager.databaseHandler import *
from display.timetableWidget.classClass import Class
from display.assignmentWidget.assignment import Assignment
from datetime import datetime, time


class ResourceHandler:
    def __init__(self):
        self.loggedIn = False
        self.userAccountKey = ""
        self.dataBaseHandler = CloudDataBase()

    def generateKeyCode(self) -> int:
        """
        Returns a randomly generated key code

        :return: int
        """
        return int("".join(str(random.randint(1, 9)) for _ in range(16)))

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
            if not assignment["deleted"]:
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

        currentTime = datetime.now()
        assignments["assignments"][index]["lastUpdated"] = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }

        writeJsonFile("data\\assignments", assignments)

    def deleteAssignment(self, index: int):
        """
        Deletes an assignment from the internal database

        :param index: int
        :return: None
        """


        assignments = loadJsonFile("data\\assignments")

        assignments["assignments"][index]["deleted"] = True

        currentTime = datetime.now()
        assignments["assignments"][index]["lastUpdated"] = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }

        writeJsonFile("data\\assignments", assignments)

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
                # Creates a datetime class of the time it was last updated
                key = "timeUpdated"
                timetableUpdated = datetime(
                    year=_class[key]["year"],
                    month=_class[key]["month"],
                    day=_class[key]["day"],
                    hour=_class[key]["hour"],
                    minute=_class[key]["minute"],
                    second=_class[key]["second"]
                )

                # Creates the starting time class
                startingTime = time(_class["startingTime"]["hour"], _class["startingTime"]["minute"])

                # Creates the ending time class
                endingTime = time(_class["endingTime"]["hour"], _class["endingTime"]["minute"])

                _classObj = Class(_class["className"], startingTime, endingTime, timetableUpdated)
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

    def databaseRunning(self) -> bool:
        return self.dataBaseHandler.available


if __name__ == '__main__':
    r = ResourceHandler()
    r.returnClasses()
