import pyodbc
import random
from display.timetableWidget.classClass import Class
from PySide6.QtCore import QThreadPool, QObject
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
import datetime as dt
from typing import *
import time
from resourceManager.workerThread import Worker


class CloudDataBase:
    def __init__(self):
        self.available = True
        self.cursor = None

    def setAvailableFalse(self):
        self.available = False

    def setAvailableTrue(self):
        self.available = True

    def hasConnection(self) -> bool:
        """
        Returns the database's connection

        :return: bool
        """
        return self.available

    def connectToDataBase(self):
        """
        Attempts to connect to the database and returns a boolean variable

        :returns: bool
        """
        connection = pyodbc.connect(
            'driver={SQL Server};  Server=3.25.137.79; Database=OrgApp; Trusted_Connection=no; UID=supermoon; PWD=Bluesky*99')

        self.cursor = connection.cursor()

    def addUserToDataBase(self, username: str, password: str, userKeyCode: str):
        """
        Adds a user to the database

        :param username: str
        :param password: str
        :param userKeyCode: str
        :return: None
        """
        command = f"""
        INSERT INTO userAccounts (username, password, userKey)
        VALUES ('{username}', '{password}', '{userKeyCode}')
        """

        self.cursor.execute(command)
        self.cursor.execute("commit")

    def isUserPasswordMatch(self, username: str, password: str) -> bool:
        """
        Returns a boolean variable to check if the user and password match

        :param username: str
        :param password: hash(password) -> str
        :return: bool
        """
        command = f"""
            SELECT * FROM userAccounts
            WHERE username='{username}' and password='{password}'
        """

        self.cursor.execute(command)

        return len(self.cursor) != 0

    def isKeyTaken(self, key: str) -> bool:
        """
        When a user makes an account, this function is run
        Returns a boolean value to check is the userKey is taken already

        :param key: str
        :return: bool
        """

        command = f"""
            SELECT * FROM accounts
            WHERE userKeyCode = '{key}'
            
        """

        self.cursor.execute(command)

        return len(self.cursor) != 0

    def getUserKeyCode(self, username: str, password: str) -> str:
        """
        Returns the user's keycode given the username and password

        :param username: str
        :param password: str
        :return: str
        """

        command = f"""
            SELECT * FROM accounts
            WHERE username='{username}' AND password='{password}'
        """

        self.cursor.execute(command)

        for row in command:
            return row[2]

    def addAssignmentToDataBase(self, userKeyCode: str, assignmentKeyCode: str, assignmentName: str,
                                timeStamp: dt.datetime,
                                completed: bool, deleted: bool):
        """
        Creates a new assignment in the database

        :param userKeyCode: str
        :param assignmentKeyCode: str
        :param assignmentName: str
        :param timeStamp: datetime class
        :param completed: bool
        :param deleted: bool
        :return: None
        """
        completed = int(completed)
        deleted = int(deleted)

        # Gets the current time
        year = timeStamp.year
        month = timeStamp.month
        day = timeStamp.day
        hour = timeStamp.hour
        minute = timeStamp.minute
        second = timeStamp.second

        command = f"""
            INSERT INTO assignments (keyCode, assignmentName, userKey, completed, removed, yearUpdated, monthUpdated, dayUpdated, hourUpdated, minuteUpdated, secondUpdated)
            values ({assignmentKeyCode}, '{assignmentName}', {userKeyCode}, {completed}, {deleted}, {year}, {month}, {day}, {hour}, {minute}, {second})
        """
        self.cursor.execute(command)
        self.cursor.execute("COMMIT")

    def editAssignmentName(self, userKeyCode: str, assignmentKeyCode: str, assignmentName: str, timeStamp: dt.datetime):
        """
        Adds an assignment to the database

        :param userKeyCode: str
        :param assignmentKeyCode: str
        :param assignmentName: str
        :param timeStamp: datetime

        """

        self.updateAssignmentTime(userKeyCode, assignmentKeyCode, timeStamp)

        command = f"""
            UPDATE assignments;
            SET assignmentName = '{assignmentName}'
            WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
        """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def updateAssignmentTime(self, userKeyCode: str, assignmentKeyCode: str, timeStamp: dt.datetime):
        """
        Given the 2 keys, it updates the assignment's last accessed date
        Note that this still requires committing

        :param userKeyCode: str
        :param assignmentKeyCode: str
        :param timeStamp: datetime
        """
        # Gets the current time
        year = timeStamp.year
        month = timeStamp.month
        day = timeStamp.day
        hour = timeStamp.hour
        minute = timeStamp.minute
        second = timeStamp.second
        command = f"""
                    UPDATE assignments
                    SET yearUpdated={year}, monthUpdated={month}, dayUpdated={day}, hourUpdated={hour}, minuteUpdated={minute}, secondUpdated={second}
                    WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
                """

        self.cursor.execute(command)

    def changeAssignmentCompleted(self, userKeyCode: str, assignmentKeyCode: str, completed: bool,
                                  timeStamp: dt.datetime):
        """
        Changes the state of an assignment

        :param userKeyCode: str
        :param assignmentKeyCode: str
        :param completed: bool
        :param timeStamp: datetime
        """
        self.updateAssignmentTime(userKeyCode, assignmentKeyCode, timeStamp)

        command = f"""
            UPDATE assignments
            SET completed = {int(completed)}
            WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
        """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def changeAssignmentDeleted(self, userKeyCode: str, assignmentKeyCode: str, timeStamp: dt.datetime):
        """
        Changes the delete state of an assignment

        :param userKeyCode: str
        :param assignmentKeyCode: str
        :param timeStamp: datetime
        """

        self.updateAssignmentTime(userKeyCode, assignmentKeyCode, timeStamp)

        command = f"""
            UPDATE assignments
            SET removed= {int(True)}
            WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
        """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def addEvent(self, userKeyCode: str, eventKeyCode: str, eventName: str, notifyTime: dt.datetime, deleted: bool,
                 notified: bool, timeStamp: dt.datetime):
        """
        Adds an event to the database


        """

        deleted = int(deleted)
        notified = int(notified)

        # Gets the current time
        yearUpdated = timeStamp.year
        monthUpdated = timeStamp.month
        dayUpdated = timeStamp.day
        hourUpdated = timeStamp.hour
        minuteUpdated = timeStamp.minute
        secondUpdated = timeStamp.second

        notifyYear = notifyTime.year
        notifyMonth = notifyTime.month
        notifyDay = notifyTime.day
        notifyHour = notifyTime.hour
        notifyMinute = notifyTime.minute

        command = f"""
            INSERT INTO events (userKeyCode, eventKeyCode, eventName, notifyYear, notifyMonth, notifyDay, notifyHour, notifyMinute, deleted, notified, yearUpdated, monthUpdated, dayUpdated, hourUpdated, minuteUpdated, secondUpdated)
            values ('{userKeyCode}', '{eventKeyCode}', '{eventName}', {notifyYear}, {notifyMonth}, {notifyDay}, {notifyHour}, {notifyMinute}, {deleted}, {notified}, {yearUpdated}, {monthUpdated}, {dayUpdated}, {hourUpdated}, {minuteUpdated}, {secondUpdated})
        """

        self.cursor.execute(command)
        self.cursor.execute("COMMIT")

    def updateEventTime(self, userKeyCode: str, eventKeyCode: str, timeStamp: dt.datetime):
        """
        Changes the update time from the database


        """

        # Gets the current time
        year = timeStamp.year
        month = timeStamp.month
        day = timeStamp.day
        hour = timeStamp.hour
        minute = timeStamp.minute
        second = timeStamp.second
        command = f"""
                    UPDATE events
                    SET yearUpdated={year}, monthUpdated={month}, dayUpdated={day}, hourUpdated={hour}, minuteUpdated={minute}, secondUpdated={second}
                    WHERE eventKeyCode='{eventKeyCode}' AND userKeyCode='{userKeyCode}'
                """

        self.cursor.execute(command)

    def changeEventDeleted(self, userKeyCode: str, eventKeyCode: str, timeStamp: dt.datetime):
        self.updateEventTime(userKeyCode, eventKeyCode, timeStamp)

        command = f"""
                    UPDATE events
                    SET deleted= {int(True)}
                    WHERE eventKeyCode='{eventKeyCode}' AND userKeyCode='{userKeyCode}'
                """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def updateTimetableUpdateTime(self, userKeyCode: str, timeStamp: dt.datetime):
        """
        Given the 2 keys, it updates the assignment's last accessed date
        Note that this still requires committing

        :param userKeyCode: str
        :param timeStamp: datetime
        """
        # Gets the current time
        year = timeStamp.year
        month = timeStamp.month
        day = timeStamp.day
        hour = timeStamp.hour
        minute = timeStamp.minute
        second = timeStamp.second

        self.deleteTimetableUpdateTime(userKeyCode)

        command = f"""
                    INSERT INTO timetable_last_updated (accountKey, year, month, day, hour, minute, second)
                    VALUES ('{userKeyCode}', '{year}', '{month}', '{day}', '{hour}', '{minute}', '{second}')    
                
                """

        self.cursor.execute(command)

    def deleteTimetableUpdateTime(self, userKeyCode: str):
        """
        Deletes all of the timetable last updated from a table given the userKeyCode

        :param userKeyCode: str
        :return: None
        """
        deleteCommand = f"""
        DELETE FROM timetable_last_updated
        WHERE accountKey='{userKeyCode}'
        """

        self.cursor.execute(deleteCommand)

    def deleteTimetableTable(self, userKeyCode: str):
        """
        Deletes all of the timetable from a table given the userKeyCode

        :param userKeyCode: str
        :return: None
        """
        deleteCommand = f"""
        DELETE FROM timetable
        WHERE accountKey='{userKeyCode}'
        """

        self.cursor.execute(deleteCommand)

    def changeTimetable(self, userKeyCode: str, userTimetable: List[List[Class]], timeStamp: dt.datetime):
        """
        Changes the timetable of a user in the database

        :param userKeyCode: str
        :param userTimetable: List[List[Class]]
        :param timeStamp: datetime
        :return: None
        """
        self.deleteTimetableTable(userKeyCode)
        self.updateTimetableUpdateTime(userKeyCode, timeStamp)

        # Pushes each class to the database
        for day in range(len(userTimetable)):
            for i in range(len(userTimetable[day])):
                _class = userTimetable[day][i]
                insertCommand = f"""
                    INSERT INTO timetable (accountKey, className, day, startHour, startMinute, endHour, endMinute)
                    VALUES ('{userKeyCode}', '{_class.timetableClass}', {day}, {_class.beginningTime.hour}, {_class.beginningTime.minute}, {_class.endingTime.hour}, {_class.endingTime.minute})
                """
                self.cursor.execute(insertCommand)

        # Finally commits it
        self.cursor.execute("commit")


if __name__ == '__main__':
    d = CloudDataBase()
    d.connectToDataBase()
    currentTime = dt.datetime.now()

    classes = [
        [
            Class("digi", dt.time(10, 30), dt.time(11, 30), currentTime),
            Class("English", dt.time(11, 30), dt.time(12, 30), currentTime)
        ], [

        ], [
            Class("Chemistry", dt.time(11, 30), dt.time(12, 30), currentTime)
        ], [

        ], [

        ]
    ]

    d.changeTimetable("1234567890123456", classes, currentTime)
