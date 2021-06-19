from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from display.assignmentWidget.assignment import Assignment
from display.assignmentWidget.widgetHolder import WidgetHolder
from display.assignmentWidget.assignmentHeaders import Header


class AssignmentDisplay(QWidget):
    def __init__(self):
        super(AssignmentDisplay, self).__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(0)

        # Creates the header
        header = Header("Assignments")
        layout.addWidget(header)

        # Creates the widget holder
        self.widgetHolder = WidgetHolder([Assignment("Assignment", False) for _ in range(10)])

        # Creates the scroll bar for the widget display
        scrollbar = QScrollArea()
        scrollbar.setWidget(self.widgetHolder)
        scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollbar.setWidgetResizable(True)
        scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(scrollbar)

        self.styleWidgets()

    def addWidget(self, title: str, completed: bool):
        """
        Adds an assignment given the title and its state

        :param title: str
        :param completed: boolean
        """
        assignment = Assignment(title, completed)
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
