from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from display.assignmentWidget.assignment import *
from display.assignmentWidget.activeAssignmentWidget import *


class ActiveAssignmentsWidget(QWidget):
    def __init__(self):
        super(ActiveAssignmentsWidget, self).__init__()
        self.assignments = [Assignment("title 1", "description 1", False),
                            Assignment("title 2", "description 2", False)]
        self.layout = QVBoxLayout(self)


        self.displayAssignments()

    def displayAssignments(self):
        for assignment in self.assignments:
            print(assignment.title)
            assignmentWidget = ActiveAssignmentWidget(assignment)
            self.layout.addWidget(assignmentWidget)

    def addAssignments(self, assignment: Assignment):
        self.assignments.append(assignment)

    def editAssignment(self, assignment: Assignment, title: str, description: str):
        assignment.title = title
        assignment.description = description

    def setAssignmentComplete(self, assignment: Assignment):
        assignment.completed = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = ActiveAssignmentsWidget()
    display.show()
    app.exec()
