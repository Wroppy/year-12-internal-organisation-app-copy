"""
Contains a list of class widgets

"""
import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
from datetime import time
import sys
from typing import *
from abc import abstractmethod


from display.timetableWidget.classWidget import ClassWidget
from display.assignmentWidget.assignmentWidget import AssignmentWidget
from display.eventsWidget.eventWidget import EventWidget

from display.timetableWidget.classClass import Class
from display.eventsWidget.event import Event
from display.assignmentWidget.assignment import Assignment


class WidgetHolder(QWidget):
    def __init__(self, infoClasses: List[Union[Class, Event, Assignment]]):
        super(WidgetHolder, self).__init__()
        self.info = infoClasses

        self.widgetLayout = QVBoxLayout(self)
        self.updateDisplay()

    def updateDisplay(self):
        """
        Adds classes to the layout

        :return:
        """
        self.displayedWidgets = []
        self.sortInfo()
        for info in self.info:
            widget = self.widgetType(info)
            self.widgetLayout.addWidget(widget)
            self.displayedWidgets.append(widget)

        self.widgetLayout.addStretch()

    @abstractmethod
    def addInfo(self, info: Union[Class, Event, Assignment]):
        """
        Adds a class to the timetable by appending it and re-displaying the layout

        :param info: Union[Class, Event, Assignment]

        :return: None
        """

        self.info.append(info)

        self.deleteItemsInLayout()

        self.updateDisplay()

    def deleteInfo(self, index: int):
        """
        Deletes a class given the index

        :param index: int
        :return: None
        """

        self.info.pop(index)
        self.deleteItemsInLayout()
        self.updateDisplay()

    def deleteItemsInLayout(self):
        """
        Deletes the items in the layout

        :return: None
        """
        # Deletes each widget in the layout one by one
        while self.widgetLayout.count():
            item = self.widgetLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                pass
    @abstractmethod
    def sortInfo(self):
        """
        Sorts the list :)

        """



if __name__ == '__main__':
    classes = [Class("Digitech", 830, 930), Class("English", 930, 1030), Class("Physics", 1130, 1230)]

    app = QApplication()
    display = WidgetHolder(classes, ClassWidget)
    display.show()
    app.exec()
