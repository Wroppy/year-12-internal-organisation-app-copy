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
from resourceManager.internalDataHandler import *


class ClassWidget(QWidget):
    def __init__(self, timetableClass: Class):
        super(ClassWidget, self).__init__()
        layout = QHBoxLayout(self)

        self.selectButton = QRadioButton()

        classTitle = QLabel(timetableClass.timetableClass)

        durationText = f"{timetableClass.beginningTime} - {timetableClass.endingTime}"
        durationLabel = QLabel(durationText)

        layout.addWidget(self.selectButton)
        layout.addWidget(classTitle)

        layout.addStretch()

        layout.addWidget(durationLabel)



if __name__ == '__main__':
    app = QApplication()
    display = ClassWidget(Class("Digitech", 1230, 1330))
    display.show()
    app.exec()