from PySide6.QtCore import QThreadPool
from resourceManager.workerThread import Worker
from PySide6.QtWidgets import *
from resourceManager.databaseHandler import DatabaseHandler


class ThreadHandler:
    def __init__(self, threadPool: QThreadPool):
        self.threadPool = threadPool
        self.databaseHandler = DatabaseHandler()

    def startThread(self, func, **kwargs):
        """
        Starts a new thread given the function and its parameters

        :param :

        """
        if not self.databaseHandler.isDatabaseActive():
            return

        worker = Worker(func)
        self.threadPool.start(worker)

    def connectToDatabase(self):
        worker = Worker(self.databaseHandler.connectToDoDatabase)

        worker.signals.error.connect(self.connectionFailed)
        worker.signals.result.connect(self.connectionSuccess)

        self.threadPool.start(worker)

    def connectionFailed(self):
        self.databaseHandler.setDatabaseUnActive()
        self.connectToDatabase()
        print("Fail")

    def connectionSuccess(self):
        self.databaseHandler.setDatabaseActive()
        print("Success")

    def addUserToDatabase(self, username: str, password: str, userKeyCode: str):

        worker = Worker(
            self.databaseHandler.addUserToDatabase(username=username, password=password, userKeyCode=userKeyCode))
        worker.signals.error.connect(self.connectionFailed)
        worker.signals.result.connect(self.connectionSuccess)
        self.threadPool.start(worker)

    def isUserPasswordMatch(self, username: str, password: str) -> bool:
        pass


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        threadPool = QThreadPool()
        self.threadHandler = ThreadHandler(threadPool)

        self.threadHandler.connectToDatabase()


if __name__ == '__main__':
    app = QApplication()
    display = TestWindow()
    display.show()

    app.exec()
