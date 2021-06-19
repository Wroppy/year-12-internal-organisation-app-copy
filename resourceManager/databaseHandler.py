import pyodbc


class CloudDataBase:
    def __init__(self):
        self.available = True
        self.cursor = None

    def hasConnection(self):
        return self.available



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


if __name__ == '__main__':
    print(CloudDataBase().connectToDataBase())
