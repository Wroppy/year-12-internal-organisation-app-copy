"""
This file converts all of the CloudDataBase class's functions
into functions that can be used in multithreading

"""

from resourceManager.databaseConnector import CloudDataBase


class DatabaseHandler:
    def __init__(self):
        self.database = CloudDataBase()

    def isDatabaseActive(self) -> bool:
        return self.database.hasConnection()

    def setDatabaseActive(self):
        self.database.setAvailableTrue()

    def setDatabaseUnActive(self):
        self.database.setAvailableFalse()

    def connectToDoDatabase(self, **kwargs):
        self.database.connectToDataBase()

    def addUserToDatabase(self, **kwargs):
        self.database.addUserToDataBase(kwargs["username"], kwargs["password"], kwargs["userKeyCode"])

    def isUserPasswordMatch(self, **kwargs) -> bool:
        return self.database.isUserPasswordMatch(kwargs["username"], kwargs["password"])

    def isKeyTaken(self, **kwargs) -> bool:
        return self.database.isKeyTaken(kwargs["key"])

    def getUserKeyCode(self, **kwargs) -> str:
        return self.database.getUserKeyCode(kwargs["username"], kwargs["password"])

    def addAssignmentToDatabase(self, **kwargs):
        self.database.addAssignmentToDataBase(kwargs["userKeyCode"], kwargs["assignmentKeyCode"],
                                              kwargs["assignmentName"], kwargs["timeStamp"], kwargs["completed"],
                                              kwargs["deleted"])

    def editAssignmentName(self, **kwargs):
        self.database.editAssignmentName(kwargs["userKeyCode"], kwargs["assignmentKeyCode"], kwargs["assignmentName"],
                                         kwargs["timeStamp"])

    def updateAssignmentTime(self, **kwargs):
        self.database.updateAssignmentTime(kwargs["userKeyCode"], kwargs["assignmentKeyCode"], kwargs["timeStamp"])

    def changeAssignmentCompleted(self, **kwargs):
        self.database.changeAssignmentCompleted(kwargs["userKeyCode"], kwargs["assignmentKeyCode"], kwargs["completed"],
                                                kwargs["timeStamp"])

    def changeAssignmentDeleted(self, **kwargs):
        self.database.changeAssignmentDeleted(kwargs["userKeyCode"], kwargs["assignmentKeyCode"], kwargs["timeStamp"])

    def updateTimetableTime(self, **kwargs):
        self.database.updateTimetableUpdateTime(kwargs["userKeyCode"], kwargs["timeStamp"])

    def deleteTimetableUpdateTime(self, **kwargs):
        self.database.deleteTimetableUpdateTime(kwargs["userKeyCode"])

    def deleteTimetable(self, **kwargs):
        self.database.deleteTimetableTable(kwargs["userKeyCode"])

    def changeTimetable(self, **kwargs):
        self.database.changeTimetable(kwargs["userKeyCode"], kwargs["userTimetable"], kwargs["timeStamp"])
