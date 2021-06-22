"""
This class contains the class Class.

"""

import datetime



class Class:
    def __init__(self, timetableClass: str, beginningTime: datetime.time, endingTime: datetime.time, timeUpdated: datetime.datetime):
        self.timetableClass = timetableClass
        self.beginningTime = beginningTime
        self.endingTime = endingTime

        self.timeUpdated = timeUpdated


