from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
from typing import *
from display.assignmentWidget.assignmentWidget import AssignmentWidget
from resourceManager.resourceHandler import ResourceHandler
from display.assignmentWidget.assignment import Assignment
from display.widgetHolders import WidgetHolder


class AssignmentHolder(QWidget):
    def __init__(self, assignments: List[Assignment], resourceManager: ResourceHandler):
        super().__init__()

        self.resourceManager = resourceManager

        self.assignmentWidgets = []
        self.assignments = assignments

        self.widgetLayout = QVBoxLayout(self)

        self.addAssignmentsToLayout()

    def deleteItemsInLayout(self):
        """
        Deletes the items in the layout

        :return: None
        """
        # Deletes each widget in the layout one by one
        while self.widgetLayout.count():
            item = self.widgetLayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                pass

    def changeAssignmentCompleted(self, assignmentCheckBox: QCheckBox, index: int, assignmentKeyCode: str):
        """
        Changes the state of an assignment in the self.assignment variable

        :param assignmentCheckBox: QCheckBox
        :param index: int
        :param assignmentKeyCode: str
        """
        self.assignments[index].completed = assignmentCheckBox.isChecked()

        self.resourceManager.updateAssignmentCompletedFile(assignmentKeyCode, assignmentCheckBox.isChecked())

    def setCheckBoxesFunctions(self):
        """
        Adds functions to the check boxes in all of the assignment widgets

        :return: None
        """
        for i in range(len(self.assignmentWidgets)):
            self.assignmentWidgets[i].completedButton.stateChanged.connect(
                lambda e, checkBox=self.assignmentWidgets[i].completedButton, index=i: self.changeAssignmentCompleted(checkBox,
                                                                                                                      index,
                                                                                                                      self.assignments[
                                                                                                                 index].keyCode))

    def addAssignmentsToLayout(self):
        """
        Adds the assignments to the layout

        :return: None
        """

        # Deletes all old widgets and clears previous widgets as well
        self.deleteItemsInLayout()
        self.sortAssignments()
        self.assignmentWidgets: List[AssignmentWidget] = []

        layout = self.layout()

        # Displays all of the assignments on the window
        for assignment in self.assignments:
            widget = AssignmentWidget(assignment)
            layout.addWidget(widget)
            self.assignmentWidgets.append(widget)

        layout.addStretch()

        self.setCheckBoxesFunctions()

    def appendAssignments(self, assignment: Assignment):
        """
        Given the assignment, it adds it at the end of a list

        :param assignment: Assignment
        :return: None
        """
        self.assignments.append(assignment)

    def deleteAssignment(self, index: int):
        """
        Given the index, deleted the assignment off the list

        :param index: int
        :return: None
        """
        self.assignments.pop(index)

    def sortAssignments(self):
        """
        First sorts the assignments by name, then by its completion status

        :return: None
        """
        self.assignments.sort(key=lambda a: a.title)
        self.assignments.sort(key=lambda a: a.completed)


if __name__ == '__main__':
    app = QApplication()

    display = WidgetHolder([Assignment("No", False) for _ in range(10)])
    display.show()

    app.exec()
