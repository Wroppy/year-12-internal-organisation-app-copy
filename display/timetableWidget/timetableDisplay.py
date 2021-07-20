"""
This class only displays the timetables and its days

"""
import datetime

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
from resourceManager.resourceHandler import ResourceHandler
from datetime import time
from display.customDecorators import singleton


@singleton
class TimetableDisplay(QWidget):
    def __init__(self, resourceManger: ResourceHandler):
        super().__init__()
        self.resourceManger = resourceManger
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

        classes = self.resourceManger.returnClasses()

        for i in range(len(self.days)):
            timetable = ClassHolder(classes[i])
            self.timetablesWidget.addWidget(timetable)

            self.timetables.append(timetable)

        self.layout.addWidget(self.timetablesWidget)


    def styleWidget(self):
        """
        Styles the widgets

        :return: None
        """
        STYLE = f"""
            QComboBox{{
                font-size: 18px;
                border: none;
            }}
        """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication()
    display = TimetableDisplay()
    display.show()
    app.exec()
