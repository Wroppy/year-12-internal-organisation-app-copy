"""
Will not be used for the internal

"""

from datetime import datetime


class Notification:
    def __init__(self, title: str, message: str, year: int, month: int, day: int, hour: int, minute: int):
        """
        Constructor for the notifications

        :param title: str
        :param message: str
        :param year: int
        :param month: int
        :param day: int
        :param hour: int
        :param minute: int
        """

        self.title = title
        self.message = message

        self.notificationTime = datetime(year, month, day, hour, minute)
