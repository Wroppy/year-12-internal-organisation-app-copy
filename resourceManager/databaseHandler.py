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



if __name__ == '__main__':
    print(int(False))
    d = CloudDataBase()
    d.connectToDataBase()
    d.addAssignmentToDataBase(9876543210978765, "First Test")
