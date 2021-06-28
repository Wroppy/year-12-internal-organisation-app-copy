from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys

from display.assignmentWidget.assignmentDisplay import AssignmentDisplay
from display.contentButtonWidget import ContentButtonWidget
from display.assignmentWidget.addAssignmentDialog import AddAssignmentDialog
from display.confirmDialog import ConfirmDialog
from resourceManager.resourceHandler import ResourceHandler


class AssignmentPage(QWidget):
    def __init__(self, resourceManager: ResourceHandler):
        super(AssignmentPage, self).__init__()

        self.resourceManager = resourceManager

        layout = QVBoxLayout(self)

        # Adds widgets to the page
        self.assignmentDisplay = AssignmentDisplay(self.resourceManager)
        layout.addWidget(self.assignmentDisplay)

        self.buttonWidget = ContentButtonWidget("Add Assignment", "Delete Assignment")
        layout.addWidget(self.buttonWidget)

        self.addButtonFunction()

    def deleteAssignmentDialog(self):
        """
        Asks the user if they want to delete an assignment or not

        """
        # Accesses the radiobutton inside the assignment holder
        # Assignment holder -> All assignments -> Each assignment -> radio button
        for i in range(len(self.assignmentDisplay.widgetHolder.assignments)):
            # for i in range(len(self.timetableWidget.timetables[self.timetableWidget.daysSelection.currentIndex()].classWidgets))
            if self.assignmentDisplay.widgetHolder.assignmentWidgets[i].selectButton.isChecked():
                dialog = ConfirmDialog("Are you sure you want to delete?")
                if dialog.exec():
                    assignmentKeyCode = self.assignmentDisplay.returnAssignmentKeyCode(i)

                    self.assignmentDisplay.widgetHolder.deleteAssignment(i)
                    self.assignmentDisplay.widgetHolder.addAssignmentsToLayout()

                    self.resourceManager.deleteAssignment(assignmentKeyCode)
                break

    def addAssignment(self, assignmentTitle: str, assignmentKey: str):
        """
        Adds an assignment to the display

        :param assignmentTitle: str
        :param assignmentKey: str

        """

        self.assignmentDisplay.addWidget(assignmentTitle, False, assignmentKey)

    def showAssignmentDialog(self, errorMessage: str):
        """
        Is displayed when the user decides to open add a new assignment

        """

        dialog = AddAssignmentDialog(self, errorMessage)
        if dialog.exec():
            assignmentTitle = dialog.assignmentEntry.text()

            # If there is no input, and the user pressed "ok" then then it will display the window again
            if len(assignmentTitle) == 0:
                self.showAssignmentDialog("Please Input An Assignment")
                return

            # Checks if the assignment name is made up of digits
            if assignmentTitle.isdigit():
                self.showAssignmentDialog("Please Input An Assignment")
                return

            assignmentKey = self.resourceManager.generateKeyCode()
            # Adds the assignment to the page
            self.addAssignment(assignmentTitle, assignmentKey)
            self.resourceManager.addAssignment(assignmentTitle, False, assignmentKey)

    def addButtonFunction(self):
        """
        Adds functionality to the buttons

        """
        self.buttonWidget.addButton.clicked.connect(lambda: self.showAssignmentDialog(None))
        self.buttonWidget.deleteButton.clicked.connect(self.deleteAssignmentDialog)


if __name__ == '__main__':
    app = QApplication()
    display = AssignmentPage()
    display.show()
    app.exec()
