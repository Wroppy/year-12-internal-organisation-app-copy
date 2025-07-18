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

from datetime import time
from display.customDecorators import singleton


@singleton
class TimetableDisplay(QWidget):
    def __init__(self, resourceManger: 'ResourceHandler'):
        super().__init__()
        self.resourceManger = resourceManger
        self.layout = QVBoxLayout(self)

        self.createComboBox()


        self.classes = self.resourceManger.returnClassesFromFile()[0]
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
        self.timetableWidget.setCurrentIndex(day)

    def createTimetableDays(self):
        """
        Adds a timetable for each day

        :return:
        """

        self.timetables = []
        self.timetableWidget = QStackedWidget()


        for i in range(len(self.days)):
            timetable = ClassHolder(self.classes[i])
            self.timetableWidget.addWidget(timetable)

            self.timetables.append(timetable)

        self.layout.addWidget(self.timetableWidget)


    def updateTimetable(self):
        self.deleteItemsInAllClassHolders()

        for i in range(len(self.timetables)):
            classHolder = self.timetables[i]
            classes = self.classes[i]

            classHolder.setClasses(classes)
            classHolder.updateClasses()

    def setTimetable(self, classes: List[List[Class]]):
        self.classes = classes


    def deleteItemsInAllClassHolders(self):
        """
        Deletes the items in the layout

        :return: None
        """

        # Deletes each widget in the layout one by one
        for classHolder in self.timetables:
            classHolder.deleteItemsInLayout()


    def deleteStackedWidget(self):
        pass

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
