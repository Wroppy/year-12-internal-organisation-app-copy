from PySide6.QtCore import QThreadPool
from resourceManager.databaseHandler import CloudDataBase
from resourceManager.workerThread import Worker


class DatabaseHandler:
    def __init__(self, threadPool: QThreadPool):
        self.threadPool = threadPool
        self.database = CloudDataBase(self.threadPool)



