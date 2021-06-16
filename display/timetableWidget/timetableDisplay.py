"""
This class only displays the timetables and its days

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from display.timetableWidget.classClass import Class
from typing import *
from resourceManager.internalDataHandler import loadJsonFile
from display.timetableWidget.classHolder import ClassHolder


class TimetableDisplay(QWidget):
    def __init__(self):
        super(TimetableDisplay, self).__init__()
        self.layout = QVBoxLayout(self)

        self.createComboBox()

        self.createTimetableDays()

        self.styleWidget()

    def createComboBox(self):
        """
        Creates the combobox displaying the days

        :return: None
        """
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.daysSelection = QComboBox()

        self.daysSelection.addItems(self.days)

        self.layout.addWidget(self.daysSelection)

        self.daysSelection.currentIndexChanged.connect(self.changeTimetableDay)

    def changeTimetableDay(self):
        """
        Changes the timetable based on the day

        :return: None
        """
        day = self.daysSelection.currentIndex()
        self.timetablesWidget.setCurrentIndex(day)

    def createTimetableDays(self):
        """
        Adds a timetable for each day

        :return:
        """

        self.timetables = []
        self.timetablesWidget = QStackedWidget()

        for _ in range(len(self.days)):
            timetable = ClassHolder([Class("Eng", 1200, 1300), Class("Phy", 1500, 1600), Class("Digi", 1100, 1200)])
            self.timetablesWidget.addWidget(timetable)

            self.timetables.append(timetable)

        self.layout.addWidget(self.timetablesWidget)

    def addClass(self, day: str, title: str, startingTime: int, endingTime: int):
        """
        Adds a class to the timetable given the day

        :param day: str
        :param title: str
        :param startingTime: int
        :param endingTime: int
        :return:
        """
        self.classes[day].append(Class(title, startingTime, endingTime))

    def styleWidget(self):
        """
        Styles the widgets

        :return: None
        """
        style = f"""
            QComboBox{{
                font-size: 18px;
                border: none;
            }}
        """

        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication()
    display = TimetableDisplay()
    display.show()
    app.exec()
