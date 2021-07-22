from resourceManager.internalDataHandler import *
from resourceManager.databaseHandler import DatabaseHandler
from resourceManager.databaseConnector import CloudDataBase
from display.timetableWidget.classClass import Class
from display.assignmentWidget.assignment import Assignment
from display.eventsWidget.event import Event
from datetime import datetime, time
import random
from PySide6.QtCore import QThreadPool
from resourceManager.workerThread import Worker
import time as t

from display.timetableWidget.timetableDisplay import TimetableDisplay


class ResourceHandler:
    def __init__(self, threadPool: QThreadPool):
        self.loggedIn = False
        self.userAccountKey = "5124718414712951"

        self.threadPool = threadPool
        self.database = DatabaseHandler()
        self.connectToDatabase()

    def connectToDatabase(self):
        """
        Attempts to establish a connection to the database

        :return: None
        """

        worker = Worker(self.database.connectToDatabase)
        self.threadPool.start(worker)
        worker.signals.result.connect(self.updateDisplay)

    def generateKeyCode(self) -> str:
        """
        Returns a randomly generated key code

        :return: str
        """
        return "".join(str(random.randint(1, 9)) for _ in range(16))

    def returnAssignmentsFromFile(self) -> List[Assignment]:
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

    def updateDisplay(self, **kwargs):
        """
        Updates the display with data pulled from the database

        """
        print("gone")
        self.returnAssignments(self.userAccountKey)

    def addAssignmentToFile(self, assignment: Assignment):
        """
        Adds an assignment to the file system

        :param assignment: assignment
        :return: None
        """

        timeStamp = datetime.now()

        assignments = loadJsonFile("data\\assignments")

        title = assignment.title
        completed = assignment.completed
        keyCode = assignment.keyCode

        assignmentDict = {
            "assignmentName": title,
            "completed": completed,
            "deleted": False,
            "lastUpdated": {
                "year": timeStamp.year,
                "month": timeStamp.month,
                "day": timeStamp.day,
                "hour": timeStamp.hour,
                "minute": timeStamp.minute,
                "second": timeStamp.second
            }
        }

        assignments[keyCode] = assignmentDict
        writeJsonFile("data\\assignments", assignments)

    def addAssignmentToDatabase(self, assignment: Assignment, timeStamp: datetime):
        title = assignment.title
        completed = assignment.completed
        keyCode = assignment.keyCode

        # Adds the assignment to the database
        worker = Worker(self.database.addAssignmentToDatabase, userKeyCode=self.userAccountKey,
                        assignmentKeyCode=keyCode, assignmentName=title, timeStamp=timeStamp, completed=completed,
                        deleted=False)
        self.threadPool.start(worker)

    def updateAssignmentCompletedFile(self, keyCode: str, checked: bool):
        """
        Updated an assignment's completed state

        :param keyCode: str
        :param checked: bool
        :return: None
        """
        assignments = loadJsonFile("data\\assignments")

        assignments[keyCode]["completed"] = checked

        timeStamp = datetime.now()
        assignments[keyCode]["lastUpdated"] = {
            "year": timeStamp.year,
            "month": timeStamp.month,
            "day": timeStamp.day,
            "hour": timeStamp.hour,
            "minute": timeStamp.minute,
            "second": timeStamp.second
        }

        print(assignments[keyCode]["assignmentName"])

        writeJsonFile("data\\assignments", assignments)

    def updateAssignmentCompletedDatabase(self, keyCode: str, checked: bool, timeStamp: datetime):

        # Updates the database
        worker = Worker(self.database.changeAssignmentCompleted, userKeyCode=self.userAccountKey,
                        assignmentKeyCode=keyCode, completed=checked, timeStamp=timeStamp)
        self.threadPool.start(worker)

    def deleteAssignmentFromFile(self, assignment: Assignment):
        """
        Deletes an assignment from the internal database and the database

        :param assignment: Assignment
        :return: None
        """

        keyCode = assignment.keyCode

        assignments = loadJsonFile("data\\assignments")

        assignments[keyCode]["deleted"] = True
        timeStamp = datetime.now()
        assignments[keyCode]["lastUpdated"] = {
            "year": timeStamp.year,
            "month": timeStamp.month,
            "day": timeStamp.day,
            "hour": timeStamp.hour,
            "minute": timeStamp.minute,
            "second": timeStamp.second
        }

        writeJsonFile("data\\assignments", assignments)

    def deleteAssignmentFromDatabase(self, assignment: Assignment, timeStamp):
        keyCode = assignment.keyCode
        completed = assignment.completed

        # Deletes from the database
        worker = Worker(self.database.changeAssignmentDeleted, userKeyCode=self.userAccountKey,
                        assignmentKeyCode=keyCode, completed=completed, timeStamp=timeStamp)

        self.threadPool.start(worker)

    def returnClassesFromFile(self) -> tuple[list[list[Class]], datetime]:
        """
        Returns the classes from the internal database

        :return: tuple[list[list[Class]], datetime]
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

                _classObj = Class(_class["className"], startingTime, endingTime)
                timetableDay.append(_classObj)
            newTimetable.append(timetableDay)

        # returns [[Classes], [], [], [], [] ]
        return newTimetable, lastUpdated

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

        self.changeTimetableDatabase(timetable["classes"], currentTime)

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

        self.changeTimetableDatabase(timetable["classes"], currentTime)

    def changeTimetableDatabase(self, timetable: List[List[dict]], currentTime: datetime):
        worker = Worker(self.database.changeTimetable, userKeyCode=self.userAccountKey, userTimetable=timetable,
                        timeStamp=currentTime)
        self.threadPool.start(worker)

    def addEventToFile(self, eventName: str, notifyTime: datetime, keyCode: str):

        events = loadJsonFile("data\\events")

        timeStamp = datetime.now()
        lastUpdated = {
            "year": timeStamp.year,
            "month": timeStamp.month,
            "day": timeStamp.day,
            "hour": timeStamp.hour,
            "minute": timeStamp.minute,
            "second": timeStamp.second
        }
        eventData = {
            "eventName": eventName,
            "notifyTime": {
                "year": notifyTime.year,
                "month": notifyTime.month,
                "day": notifyTime.day,
                "hour": notifyTime.hour,
                "minute": notifyTime.minute
            },
            "deleted": False,
            "notified": False,
            "lastUpdated": lastUpdated
        }
        events[keyCode] = eventData

        writeJsonFile("data\\events", events)

    def addEventToDatabase(self, eventName: str, notifyTime: datetime, keyCode: str, timeStamp: datetime):
        # Adds the event to the database
        worker = Worker(self.database.addEvent, userKeyCode=self.userAccountKey, eventKeyCode=keyCode,
                        eventName=eventName, notifyTime=notifyTime, deleted=False, notified=False,
                        timeStamp=timeStamp)
        self.threadPool.start(worker)

    def deleteEventFromFile(self, keyCode: str):
        events = loadJsonFile("data\\events")

        timeStamp = datetime.now()
        lastUpdated = {
            "year": timeStamp.year,
            "month": timeStamp.month,
            "day": timeStamp.day,
            "hour": timeStamp.hour,
            "minute": timeStamp.minute,
            "second": timeStamp.second
        }

        events[keyCode]["lastUpdated"] = lastUpdated
        events[keyCode]["deleted"] = True

        writeJsonFile("data\\events", events)

    def deleteEventFromDatabase(self, keyCode: str, timeStamp: datetime):
        # Deleted the event from the database
        worker = Worker(self.database.changeEventDeleted, userKeyCode=self.userAccountKey, eventKeyCode=keyCode,
                        timeStamp=timeStamp)
        self.threadPool.start(worker)

    def changeEventNotified(self, keyCode: str):
        events = loadJsonFile("data\\events")

        currentTime = datetime.now()
        lastUpdated = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }

        events[keyCode]["lastUpdated"] = lastUpdated
        events[keyCode]["notified"] = True

        writeJsonFile("data\\events", events)

    def returnEventsFromFile(self) -> List[Event]:
        """
        Returns all of the events in

        """
        events = loadJsonFile("data\\events")

        eventData = []
        for keyCode in events.keys():
            # Checks if the event has already been deleted
            if not events[keyCode]["deleted"]:
                eventName = events[keyCode]["eventName"]

                notifyTime = datetime(
                    year=events[keyCode]["notifyTime"]["year"],
                    month=events[keyCode]["notifyTime"]["month"],
                    day=events[keyCode]["notifyTime"]["day"],
                    hour=events[keyCode]["notifyTime"]["hour"],
                    minute=events[keyCode]["notifyTime"]["minute"]
                )

                event = Event(eventName, notifyTime, keyCode)

                eventData.append(event)

        return eventData

    def returnNotifyEvents(self) -> List[Event]:
        """
        Loops through each event and checks if they have a chance of notifying the user

        :return: List[Event]
        """
        events = self.returnEventsFromFile()

        eventsData = []
        for event in events:
            # Checks if the time has not already passed
            if event.notifyTime >= datetime.now():
                eventsData.append(event)

        return eventsData

    def loadClassFromDatabase(self):
        worker = Worker(self.database.returnTimetable, userKeyCode=self.userAccountKey)
        worker.signals.result.connect(self.updateTimetableDisplayDatabase)

        self.threadPool.start(worker)

    def updateTimetableDisplayDatabase(self, timetableDatabase: Tuple[List[Tuple[Any]], Tuple[Any]]):
        """
        Updates the timetable displayed when the worker thread has finished without an error

        """

        classes, timeStamp = timetableDatabase

        sortedClasses, sortedTimeStamp = self.sortTimetableFromDatabase(classes, timeStamp)

        print(sortedClasses)
        print(sortedTimeStamp)

        sortedTimetable = self.sortTimetable(sortedClasses, sortedTimeStamp)

        TimetableDisplay().setTimetable(sortedTimetable)
        TimetableDisplay().updateTimetable()

    def sortTimetableFromDatabase(self, classes, timeStamp) -> Tuple[List[List[Class]], datetime]:

        print(f"Classes: {classes}")
        print(f"Time Stamp: {timeStamp}")

        sortedClasses = [[] for _ in range(5)]

        for _class in classes:
            startingTime = time(_class[1], _class[2])
            endingTime = time(_class[3], _class[4])
            className = _class[5]

            c = Class(className, startingTime, endingTime)

            day = _class[6]

            sortedClasses[day].append(c)

        year = timeStamp[0]
        month = timeStamp[1]
        day = timeStamp[2]
        hour = timeStamp[3]
        minute = timeStamp[4]
        second = timeStamp[5]

        sortedTimeStamp = datetime(year, month, day, hour, minute, second)

        return sortedClasses, sortedTimeStamp

    def sortTimetable(self, timetableDatabase: List[List[Class]], timeStampDatabase: datetime) -> List[List[Class]]:
        """
        Given the 2 timestamps of the timetables,
        returns the most recently updated timetable

        :param timetableDatabase:  List[List[Any]]
        :param timeStampDatabase: datetime
        """
        timetableFile, timeStampFile = self.returnClassesFromFile()

        # Checks if the database's timetable has been updated more recently
        if timeStampDatabase > timeStampFile:
            self.writeClassesToFile(timetableDatabase, timeStampDatabase)

            return timetableDatabase

        # Checks if the timestamps are the same
        # If they are, then there is no need to change the data internally, and externally
        # If there is a difference, then the database must be updated
        if timeStampDatabase != timeStampFile:
            print("Needs to change")
            self.changeTimetableDatabase(self.returnSortedDictTimetable(timetableFile), timeStampFile)

        return timetableFile

    def writeClassesToFile(self, classes: List[List[Class]], timeStamp: datetime):
        """
        Writes a list of classes to a file, given the a list of classes, and a timeStamp

        :param classes: List[List[Class]]
        :param timeStamp: datetime
        """

        timetable = self.returnSortedDictTimetable(classes)

        lastUpdated = self.returnDatetimeDict(timeStamp)

        classData = {
            "classes": timetable,
            "lastUpdated": lastUpdated
        }

        print(str(classData).replace("'", '"'))

        writeJsonFile("data\\timetable", classData)

    def returnDatetimeDict(self, timeStamp: datetime) -> dict:
        return {
            "year": timeStamp.year,
            "month": timeStamp.month,
            "day": timeStamp.day,
            "hour": timeStamp.hour,
            "minute": timeStamp.minute,
            "second": timeStamp.second
        }

    def returnSortedDictTimetable(self, classes: List[List[Class]]):
        timetable = []
        for day in classes:
            classesDay = []
            for _class in day:
                c = {
                    "className": _class.timetableClass,
                    "startingTime": {
                        "hour": _class.beginningTime.hour,
                        "minute": _class.beginningTime.minute
                    },
                    "endingTime": {
                        "hour": _class.endingTime.hour,
                        "minute": _class.endingTime.minute
                    }
                }

                classesDay.append(c)
            timetable.append(classesDay)

        return timetable

    def returnAssignments(self, userKeyCode: str):
        worker = Worker(self.database.returnAssignments, userKeyCode=userKeyCode)
        self.threadPool.start(worker)
        worker.signals.result.connect(self.assignmentsReturnedFromDatabase)

    def assignmentsReturnedFromDatabase(self, assignments: List[Tuple[Any]]):
        internalData = loadJsonFile("data\\assignments")
        assignmentsDict = self.sortAssignmentsReturnedFromDatabaseToDict(assignments)
        print(f"AssignmentDict {assignmentsDict}")
        mergedAssignments = self.mergeDatabaseFileData(internalData, assignmentsDict)

        print(len(mergedAssignments))

        print(f"Merged Assignments {mergedAssignments}")

        # Updates the file
        writeJsonFile("data\\assignments", mergedAssignments)

        assignmentList = self.sortAssignmentsDictToClass(mergedAssignments)

        print(assignmentList)

    def sortAssignmentsReturnedFromDatabaseToDict(self, assignments: List[Tuple[Any]]) -> Dict[str, Any]:
        """
        Sorts the assignments from a tuple, to a dictionary

        :param assignments: List[Tuple[Any]]
        :return: Dict[str, any]
        """

        assignmentDict = {}
        for assignment in assignments:
            key = assignment[0]
            print(key)
            name = assignment[1]
            completed = bool(assignment[3])
            deleted = bool(assignment[4])

            lastUpdated = {
                "year": assignment[5],
                "month": assignment[6],
                "day": assignment[7],
                "hour": assignment[8],
                "minute": assignment[9],
                "second": assignment[10]
            }

            assignmentDict[key] = {
                "assignmentName": name,
                "completed": completed,
                "deleted": deleted,
                "lastUpdated": lastUpdated
            }

        return assignmentDict

    def sortAssignmentsDictToClass(self, assignments: Dict[str, Any]) -> List[Assignment]:
        assignmentList = []
        for key in assignments.keys():
            assignment = assignments[key]
            # Checks if the assignment has been deleted first
            if not assignment["deleted"]:
                a = Assignment(assignment["assignmentName"], assignment["completed"], key)
                assignmentList.append(a)

        return assignmentList

    def mergeDatabaseFileData(self, internalData: Dict[str, Any], databaseData: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merges the internal and external data together into one dictionary

        :param internalData: dict[str, any]
        :param databaseData: dict[str, any]
        :return: dict[str, any]
        """

        updatedData = {}

        # Loops through each internal
        for key in internalData:
            # Checks if the item in the database
            if key in databaseData.keys():
                dataBaseTimeStamp = datetime(
                    year=databaseData[key]["lastUpdated"]["year"],
                    month=databaseData[key]["lastUpdated"]["month"],
                    day=databaseData[key]["lastUpdated"]["day"],
                    hour=databaseData[key]["lastUpdated"]["hour"],
                    minute=databaseData[key]["lastUpdated"]["minute"],
                    second=databaseData[key]["lastUpdated"]["second"]

                )

                internalTimeStamp = datetime(
                    year=internalData[key]["lastUpdated"]["year"],
                    month=internalData[key]["lastUpdated"]["month"],
                    day=internalData[key]["lastUpdated"]["day"],
                    hour=internalData[key]["lastUpdated"]["hour"],
                    minute=internalData[key]["lastUpdated"]["minute"],
                    second=internalData[key]["lastUpdated"]["second"]
                )

                # Checks if the database is more recent
                if dataBaseTimeStamp > internalTimeStamp:
                    updatedData[key] = databaseData[key]
                    continue

            updatedData[key] = internalData[key]

        print(updatedData.keys())
        for key in databaseData.keys():
            print(key)
            if key not in updatedData.keys():
                updatedData[key] = databaseData[key]
                print("True")

        return updatedData


if __name__ == '__main__':
    r = ResourceHandler()
    a = r.returnNotifyEvents()
