"""
Will not be used for the internal

"""

from datetime import datetime


class Notification:
    def __init__(self, title: str, message: str, notificationTime: datetime):
        """
        Constructor for the notifications

        :param title: str
        :param message: str
        :param notificationTime: datetime
        """

        self.title = title
        self.message = message

        self.notificationTime = notificationTime
