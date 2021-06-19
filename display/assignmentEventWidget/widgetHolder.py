from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
from typing import *
from display.assignmentEventWidget.assignmentWidget import AssignmentWidget
from display.assignmentEventWidget.assignment import Assignment
import sys


class WidgetHolder(QWidget):
    def __init__(self, assignments: List[Assignment]):
        super(WidgetHolder, self).__init__()

        self.assignments = assignments

        layout = QVBoxLayout(self)

        self.addAssignmentsToLayout()

    def addAssignmentsToLayout(self):
        layout = self.layout()

        for assignment in self.assignments:
            widget = AssignmentWidget(assignment)
            layout.addWidget(widget)

        layout.addStretch()

    def appendAssignments(self, assignment: Assignment):
        self.assignments.append(assignment)

    def deleteAssignment(self, index: int):
        self.assignments.pop(index)


if __name__ == '__main__':
    app = QApplication()

    display = WidgetHolder([Assignment("No", False) for _ in range(10)])
    display.show()

    app.exec()