"""
This class handles the event class

"""

import datetime as dt
from dataclasses import dataclass

@dataclass()
class Event:
    eventName: str
    notifyTime: dt.datetime
    eventKeyCode: str

    def formatTime(self) -> str:
        """
        Formats the time to hh/mm dd/mm/yy
        Ex: 12:30 Mon/Dec/2021

        :return: str
        """

        formattedTime = self.notifyTime.strftime("%X")[:-3]

        day = self.notifyTime.strftime("%a")
        month = self.notifyTime.strftime("%b")
        year = self.notifyTime.strftime("%Y")

        text = f"{formattedTime} {day}/{month}/{year}"

        return text
