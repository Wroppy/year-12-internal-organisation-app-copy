"""
This class is for a specific class in the timetable.
It contains the title, start and end time, along with a radio button

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from display.timetableWidget.classClass import *
from display.generalInfoDisplay import InfoDisplay
from resourceManager.internalDataHandler import *


class ClassWidget(InfoDisplay):
    def __init__(self, timetableClass: Class):
        self.timetableClass = timetableClass
        super(ClassWidget, self).__init__()

    def createLeftSideWidgets(self):
        classTitle = QLabel(self.timetableClass.timetableClass)
        self.layout.addWidget(classTitle)

    def createRightSideWidgets(self):
        durationText = self.timetableClass.formatClassTime()
        durationLabel = QLabel(durationText)

        self.layout.addWidget(durationLabel)


if __name__ == '__main__':
    app = QApplication()
    display = ClassWidget(Class("Digitech", 1230, 1330))
    display.show()
    app.exec()
