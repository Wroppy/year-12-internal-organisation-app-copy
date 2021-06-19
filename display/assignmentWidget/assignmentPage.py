from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys

from display.assignmentWidget.activeWidgetDisplay import ActiveWidgetDisplay
from display.assignmentWidget.contentButtonWidget import ContentButtonWidget


class AssignmentPage(QWidget):
    def __init__(self):
        super(AssignmentPage, self).__init__()

        layout = QVBoxLayout(self)

        # Adds widgets to the page
        self.activeWidgets = ActiveWidgetDisplay()
        layout.addWidget(self.activeWidgets)


        self.buttonWidget = ContentButtonWidget("Add Assignment", "Edit Assignment", "Delete Assignment")
        layout.addWidget(self.buttonWidget)

    def addButtonFunction(self):
        pass

if __name__ == '__main__':
    app = QApplication()
    display = AssignmentPage()
    display.show()
    app.exec()