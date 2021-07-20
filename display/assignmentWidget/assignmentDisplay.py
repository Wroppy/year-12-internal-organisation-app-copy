from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from display.assignmentWidget.assignment import Assignment
from display.assignmentWidget.assignmentHolder import AssignmentHolder
from display.header import Header
from resourceManager.resourceHandler import ResourceHandler


class AssignmentDisplay(QWidget):
    def __init__(self, resourceManager: ResourceHandler):
        super(AssignmentDisplay, self).__init__()

        self.resourceManager = resourceManager
        layout = QVBoxLayout(self)
        layout.setSpacing(0)

        # Creates the header
        header = Header(QLabel("Assignments"))
        layout.addWidget(header)

        # Gets the assignments from the resource manager
        assignments = self.resourceManager.returnAssignmentsFromFile()

        # Creates the widget holder
        self.widgetHolder = AssignmentHolder(assignments, self.resourceManager)

        # Creates the scroll bar for the widget display
        scrollbar = QScrollArea()
        scrollbar.setWidget(self.widgetHolder)
        scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollbar.setWidgetResizable(True)
        scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(scrollbar)

        self.styleWidgets()

    def returnAssignmentKeyCode(self, index: int) -> Assignment:
        """
        Returns an assignment class given the index of its location in the list

        :param index: int
        :return: Assignment
        """
        return self.widgetHolder.assignments[index]

    def addWidget(self, title: str, completed: bool, assignmentKey: str):
        """
        Adds an assignment given the title and its state

        :param title: str
        :param completed: boolean
        :param assignmentKey: str
        """
        assignment = Assignment(title, completed, assignmentKey)
        self.widgetHolder.appendAssignments(assignment)

        self.widgetHolder.addAssignmentsToLayout()

    def styleWidgets(self):
        """
        Styles the widgets nested

        """
        STYLE = f"""
            QScrollArea{{
                border: none;
            }}
        """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication()
    display = AssignmentDisplay()
    display.show()
    app.exec()