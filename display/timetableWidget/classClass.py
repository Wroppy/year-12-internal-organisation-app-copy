"""
This class contains the class Class.

"""

import datetime
from dataclasses import dataclass


@ dataclass()
class Class:
    timetableClass: str
    beginningTime: datetime.time
    endingTime: datetime.time

    def formatClassTime(self) -> str:
        """
        Returns the classes time in a format suitable for viewing

        :return: str
        """

        beginningTime = self.beginningTime.strftime("%X")[:-3]
        endingTime = self.endingTime.strftime("%X")[:-3]

        return f"{beginningTime} - {endingTime}"



