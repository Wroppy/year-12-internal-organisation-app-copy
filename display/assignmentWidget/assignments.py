from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from display.assignmentWidget.assignment import *


class AssignmentsWidgets(QMainWindow):
    def __init__(self):
        super(AssignmentsWidgets, self).__init__(None)
        self.assignments = []

    def addAssignments(self, assignment: Assignment):
        self.assignments.append(assignment)

    def editAssignment(self, assignment: Assignment, title: str, description: str):
        assignment.title = title
        assignment.description = description

    def setAssignmentComplete(self, assignment: Assignment):
        assignment.completed = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = AssignmentsWidgets()
    display.show()
    app.exec()
