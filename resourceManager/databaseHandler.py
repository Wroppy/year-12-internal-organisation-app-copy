import pyodbc
import random
from datetime import datetime


class CloudDataBase:
    def __init__(self):
        self.available = True
        self.cursor = None

    def hasConnection(self):
        return self.available

    def generateKeyCode(self):
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

    def addAssignmentToDataBase(self, userKeyCode: int, assignmentName: str):
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
            UPDATE assignments
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

    def changeCompleted(self, userKeyCode: int, assignmentKeyCode: int, completed: bool):
        """
        Changes the state of an assignment

        :param userKeyCode: int
        :param assignmentKeyCode: int
        """
        self.updateAssignmentTime(userKeyCode, assignmentKeyCode)

        command = f"""
            UPDATE assignments
            SET completed = {int(completed)}
            WHERE keyCode='{assignmentKeyCode}' AND userKey='{userKeyCode}'
        """

        self.cursor.execute(command)
        self.cursor.execute("Commit")

    def changeDeleted(self, userKeyCode: int, assignmentKeyCode: int):
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


if __name__ == '__main__':
    d = CloudDataBase()
    d.connectToDataBase()
    d.editAssignmentName(9876543210978765, 7362647131834739, "Updating using 2 functions")
