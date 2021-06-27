from PySide6.QtCore import QThreadPool
from resourceManager.workerThread import Worker


class ThreadHandler:
    def __init__(self, threadPool: QThreadPool):
        self.threadPool = threadPool
