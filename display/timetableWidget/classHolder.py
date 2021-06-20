"""
Contains a list of class widgets

"""


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.timetableWidget.classClass import Class
from display.timetableWidget.classWidget import ClassWidget


class ClassHolder(QWidget):
    def __init__(self, classes: List[Class]):
        super(ClassHolder, self).__init__()
        self.classes = classes
        self.widgetLayout = QVBoxLayout(self)

        self.updateClasses()

    def updateClasses(self):
        """
        Adds classes to the layout

        :return:
        """
        self.classWidgets = []
        self.sortTimetable()
        for _class in self.classes:
            widget = ClassWidget(_class)
            self.widgetLayout.addWidget(widget)
            self.classWidgets.append(widget)

        self.widgetLayout.addStretch()

    def addClass(self, classTitle: str, startingTime: int, endingTime: int):
        """
        Adds a class to the timetable by appending it and re-displaying the layout

        :param classTitle: str
        :param startingTime: int
        :param endingTime: int
        :return: None
        """


        c = Class(classTitle, startingTime, endingTime)
        self.classes.append(c)

        self.deleteItemsInLayout()

        self.updateClasses()



    def deleteClass(self, index: int):
        """
        Deletes a class in the list given its index

        :param index: int
        :return: None
        """

        self.classes.pop(index)
        self.deleteItemsInLayout()
        self.updateClasses()

    def deleteItemsInLayout(self):
        """
        Deletes the items in the layout

        :return: None
        """
        print(self.widgetLayout.count())
        if self.widgetLayout.count() > 1:
            # Deletes each widget in the layout one by one
            while self.widgetLayout.count():
                item = self.widgetLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    pass
        else:
            pass

    def sortTimetable(self):
        """
        Sorts the timetable by the classes beginning time.

        :return: None
        """
        self.classes.sort(key=lambda t: t.beginningTime)
        print(self.classes)


if __name__ == '__main__':
    classes = [Class("Digitech", 830, 930), Class("English", 930, 1030), Class("Physics", 1130, 1230)]

    app = QApplication()
    display = ClassHolder(classes)
    display.show()
    app.exec()
