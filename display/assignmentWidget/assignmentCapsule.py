from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from display.assignmentWidget.assignments import AssignmentsWidgets
from display.contentButtonWidget import ContentButtonWidget


class AssignmentCapsule(QWidget):
    def __init__(self):
        super(AssignmentCapsule, self).__init__()
        self.layout = QVBoxLayout(self)

        self.placeWidgets()

    def placeWidgets(self):
        self.assignmentWidget = AssignmentsWidgets()
        self.layout.addWidget(self.assignmentWidget)

        self.layout.addStretch()

        self.buttonWidget = ContentButtonWidget("Add Assignment", "Edit Assignment", "Delete Assignment")
        self.layout.addWidget(self.buttonWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = AssignmentCapsule()
    display.show()
    app.exec()
