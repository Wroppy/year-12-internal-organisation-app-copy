from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys

from display.assignmentWidget.assignmentDisplay import AssignmentDisplay
from display.assignmentWidget.contentButtonWidget import ContentButtonWidget
from display.assignmentWidget.addAssignmentDialog import AddAssignmentDialog
from display.confirmDialog import ConfirmDialog


class AssignmentPage(QWidget):
    def __init__(self):
        super(AssignmentPage, self).__init__()

        layout = QVBoxLayout(self)

        # Adds widgets to the page
        self.assignmentDisplay = AssignmentDisplay()
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
                    self.assignmentDisplay.widgetHolder.deleteAssignment(i)
                    self.assignmentDisplay.widgetHolder.addAssignmentsToLayout()
                break

    def addAssignment(self, assignmentTitle: str):
        """
        Adds an assignment to the display

        """
        self.assignmentDisplay.addWidget(assignmentTitle, False)

    def showAssignmentDialog(self):
        """
        Is displayed when the user decides to open add a new assignment

        """

        dialog = AddAssignmentDialog(self)
        if dialog.exec():
            # If there is no input, and the user pressed "ok" then then it will display the window again
            if len(dialog.assignmentEntry.text()) == 0:
                self.showAssignmentDialog()
            else:
                assignmentTitle = dialog.assignmentEntry.text()

                # Adds the assignment to the page
                self.addAssignment(assignmentTitle)

    def addButtonFunction(self):
        """
        Adds functionality to the buttons

        """
        self.buttonWidget.addButton.clicked.connect(self.showAssignmentDialog)
        self.buttonWidget.deleteButton.clicked.connect(self.deleteAssignmentDialog)


if __name__ == '__main__':
    app = QApplication()
    display = AssignmentPage()
    display.show()
    app.exec()
