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

    def addAssignment(self, assignment: Assignment):
        """
        Adds an assignment to the file system

        :param assignment: assignment
        :return: None
        """

        currentTime = datetime.now()

        assignments = loadJsonFile("data\\assignments")

        title = assignment.title
        completed = assignment.completed
        keyCode = assignment.keyCode

        assignmentDict = {
            "assignmentName": title,
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

        assignments[keyCode] = assignmentDict
        writeJsonFile("data\\assignments", assignments)

        # Adds the assignment to the database
        worker = Worker(self.database.addAssignmentToDatabase, userKeyCode=self.userAccountKey,
                        assignmentKeyCode=keyCode, assignmentName=title, timeStamp=currentTime, completed=completed,
                        deleted=False)
        self.threadPool.start(worker)

    def updateAssignmentCompleted(self, keyCode: str, checked: bool):
        """
        Updated an assignment's completed state

        :param keyCode: str
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

        print(assignments[keyCode]["assignmentName"])

        writeJsonFile("data\\assignments", assignments)

        # Updates the database
        worker = Worker(self.database.changeAssignmentCompleted, userKeyCode=self.userAccountKey,
                        assignmentKeyCode=keyCode, completed=checked, timeStamp=currentTime)
        self.threadPool.start(worker)

    def deleteAssignment(self, assignment: Assignment):
        """
        Deletes an assignment from the internal database and the database

        :param assignment: Assignment
        :return: None
        """

        keyCode = assignment.keyCode

        assignments = loadJsonFile("data\\assignments")

        assignments[keyCode]["deleted"] = True
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

        # Deletes from the database
        worker = Worker(self.database.changeAssignmentDeleted, userKeyCode=self.userAccountKey,
                        assignmentKeyCode=keyCode, completed=assignment.completed, timeStamp=currentTime)

        self.threadPool.start(worker)

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

                _classObj = Class(_class["className"], startingTime, endingTime)
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

        self.addClassToDatabase(timetable["classes"], currentTime)

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

        self.addClassToDatabase(timetable["classes"], currentTime)

    def addClassToDatabase(self, timetable: List[List[dict]], currentTime: datetime):
        worker = Worker(self.database.changeTimetable, userKeyCode=self.userAccountKey, userTimetable=timetable,
                        timeStamp=currentTime)
        self.threadPool.start(worker)

    def addEvent(self, eventName: str, notifyTime: datetime, keyCode: str):

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

        # Adds the event to the database
        worker = Worker(self.database.addEvent, userKeyCode=self.userAccountKey, eventKeyCode=keyCode,
                        eventName=eventName, notifyTime=notifyTime, deleted=False, notified=False,
                        timeStamp=currentTime)
        self.threadPool.start(worker)

    def deleteEvent(self, keyCode: str):
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
        events[keyCode]["deleted"] = True

        writeJsonFile("data\\events", events)

        # Deleted the event from the database
        worker = Worker(self.database.changeEventDeleted, userKeyCode=self.userAccountKey, eventKeyCode=keyCode,
                        timeStamp=currentTime)
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

    def returnEvents(self) -> List[Event]:
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
        events = self.returnEvents()

        eventsData = []
        for event in events:
            # Checks if the time has not already passed
            if event.notifyTime >= datetime.now():
                eventsData.append(event)

        return eventsData

    def loadClassFromDatabase(self):

        self.createTableReturnWorker()
        self.threadPool.start(self.worker)

    def returnClassesFromDatabase(self, databaseStuff):
        print(databaseStuff)

    def createTableReturnWorker(self):
        self.worker = Worker(self.database.returnTimetable, userKeyCode=self.userAccountKey)
        self.worker.signals.result.connect(self.returnClassesFromDatabase)


if __name__ == '__main__':
    r = ResourceHandler()
    a = r.returnNotifyEvents()
