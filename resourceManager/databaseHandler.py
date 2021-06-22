import pyodbc
import random
from display.timetableWidget.classClass import Class
from datetime import datetime
from typing import *
import time


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

    def generateKeyCode(self) -> int:
        """
        Returns a randomly generated key code

        :return: int
        """
        return int("".join(str(random.randint(1, 9)) for i in range(16)))

    def connectToDataBase(self) -> bool:
        """
        Attempts to connect to the database and returns a boolean variable

        :returns: bool
        """
        try:
            connection = pyodbc.connect(
                'driver={SQL Server};  Server=3.25.137.79; Database=OrgApp; Trusted_Connection=no; UID=supermoon; PWD=Bluesky*99')

            self.cursor = connection.cursor()

            return True
        except (pyodbc.OperationalError, pyodbc.Error) as e:
            print(e)
            return False

    def addUserToDataBase(self, username: str, password: int):
        """
        Adds a user to the database

        :param username: str
        :param password: int
        :return: None
        """
        try:
            command = f"""
            INSERT INTO userAccounts (username, password, userKey)
            VALUES ('{username}', '{password}')
            
            """

            self.cursor.execute(command)
            self.cursor.execute("commit")

        except (pyodbc.OperationalError, pyodbc.Error):
            self.setAvailableFalse()

    def isUserInDataBase(self, username, password) -> bool:
        """
        Returns a boolean variable to check if the user and password match

        :param username: str
        :param password: hash(password) -> int
        :return: bool
        """
        try:
            command = f"""
                SELECT * FROM userAccounts
                WHERE username='{username}'
            """

            self.cursor.execute(command)

            for user in self.cursor:
                if user[1] == password:
                    return True

            return False

        except (pyodbc.Error, pyodbc.OperationalError):
            return False

    def getUserKeyCode(self):
        try:
            pass
        except (pyodbc.OperationalError, pyodbc.Error):
            self.setAvailableFalse()

    def addAssignmentToDataBase(self, userKeyCode: int, assignmentName: str):
        """
        Creates a new assignment in the data base

        :param userKeyCode: int
        :param assignmentName: str
        :return: None
        """
        customKeyCode = self.generateKeyCode()
        completed = int(False)
        removed = int(False)

        # Gets the current time
        currentTime = datetime.now()
        year = currentTime.year
        month = currentTime.month
        day = currentTime.day
        hour = currentTime.hour
        minute = currentTime.minute
        second = currentTime.second

        command = f"""
            INSERT INTO assignments (keyCode, assignmentName, userKey, completed, removed, yearUpdated, monthUpdated, dayUpdated, hourUpdated, minuteUpdated, secondUpdated)
            values ({customKeyCode}, '{assignmentName}', {userKeyCode}, {completed}, {removed}, {year}, {month}, {day}, {hour}, {minute}, {second})
        """
        self.cursor.execute(command)
        self.cursor.execute("COMMIT")

    def editAssignmentName(self, userKeyCode: int, assignmentKeyCode: int, assignmentName: str):
        """
        Adds an assignment to the database

        :param userKeyCode: int
        :param assignmentKeyCode: int
        :param assignmentName: str

        """

        self.updateAssignmentTime(userKeyCode, assignmentKeyCode)

        command = f"""
            UPDATE assignments;
            SET assignmentName = '{assignmentName}'
            WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
        """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def updateAssignmentTime(self, userKeyCode: int, assignmentKeyCode: int):
        """
        Given the 2 keys, it updates the assignment's last accessed date
        Note that this still requires committing

        :param userKeyCode: int
        :param assignmentKeyCode: int
        """
        # Gets the current time
        currentTime = datetime.now()
        year = currentTime.year
        month = currentTime.month
        day = currentTime.day
        hour = currentTime.hour
        minute = currentTime.minute
        second = currentTime.second

        command = f"""
                    UPDATE assignments
                    SET yearUpdated={year}, monthUpdated={month}, dayUpdated={day}, hourUpdated={hour}, minuteUpdated={minute}, secondUpdated={second}
                    WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
                """

        self.cursor.execute(command)

    def changeAssignmentCompleted(self, userKeyCode: int, assignmentKeyCode: int, completed: bool):
        """
        Changes the state of an assignment

        :param userKeyCode: int
        :param assignmentKeyCode: int
        """
        self.updateAssignmentTime(userKeyCode, assignmentKeyCode)

        command = f"""
            UPDATE assignments;
            SET completed = {int(completed)}
            WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
        """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def changeAssignmentDeleted(self, userKeyCode: int, assignmentKeyCode: int):
        """
        Changes the delete state of an assignment

        :param userKeyCode: int
        :param assignmentKeyCode: int
        """

        self.updateAssignmentTime(userKeyCode, assignmentKeyCode)

        command = f"""
            UPDATE assignments
            SET deleted = {int(True)}
            WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
        """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def updateTimetableUpdateTime(self, userKeyCode: int):
        """
        Given the 2 keys, it updates the assignment's last accessed date
        Note that this still requires committing

        :param userKeyCode: int
        """
        # Gets the current time
        currentTime = datetime.now()
        year = currentTime.year
        month = currentTime.month
        day = currentTime.day
        hour = currentTime.hour
        minute = currentTime.minute
        second = currentTime.second

        command = f"""
                    UPDATE timetables
                    SET yearUpdated={year}, monthUpdated={month}, dayUpdated={day}, hourUpdated={hour}, minuteUpdated={minute}, secondUpdated={second}
                    WHERE userKey={userKeyCode}
                """

        self.cursor.execute(command)

    def changeTimetable(self, userKeyCode: int, userTimetable: List[List[Class]]):
        """
        Changes the timetable of a user in the database

        :param userKeyCode: int
        :param userTimetable: List[List[Assignment]]
        :return: None
        """

        # Deletes everything from the user's timetable
        deleteCommand = f"""
        DELETE FROM timetables 
        where userCode={userKeyCode}
        """

        self.cursor.execute(deleteCommand)

        # Pushes each class to the database
        for day in userTimetable:
            for i in range(len(day)):
                _class = day[i]
                insertCommand = f"""
                    INSERT INTO timetable (class, day, startTime, endTime)
                    VALUES ('{_class.timetableClass}', {i}, {_class.beginningTime}, {_class.endingTime})
                    WHERE userKey = '{userKeyCode}'
                """
                self.cursor.execute(insertCommand)

        # Finally commits it
        self.cursor.execute("commit")

    def loadTimetable(self, userKeyCode: int):
        command = f"""
            SELECT * from timetable
            WHERE userKey={userKeyCode}
        """

        self.cursor.execute(command)

        return self.cursor




if __name__ == '__main__':
    d = CloudDataBase()
    d.connectToDataBase()
