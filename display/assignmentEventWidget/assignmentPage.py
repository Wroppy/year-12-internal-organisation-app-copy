from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys

from display.assignmentEventWidget.activeWidgetDisplay import ActiveWidgetDisplay
from display.assignmentEventWidget.completedWidgetDisplay import CompletedWidgetDisplay
from display.assignmentEventWidget.contentButtonWidget import ContentButtonWidget


class AssignmentPage(QWidget):
    def __init__(self):
        super(AssignmentPage, self).__init__()

        layout = QVBoxLayout(self)

        # Adds widgets to the page
        self.activeWidgets = ActiveWidgetDisplay()
        layout.addWidget(self.activeWidgets)

        self.completedWidgets = CompletedWidgetDisplay()
        layout.addWidget(self.completedWidgets)

        self.buttonWidget = ContentButtonWidget("Add Assignment", "Edit Assignment", "Delete Assignment")
        layout.addWidget(self.buttonWidget)

if __name__ == '__main__':
    app = QApplication()
    display = AssignmentPage()
    display.show()
    app.exec()