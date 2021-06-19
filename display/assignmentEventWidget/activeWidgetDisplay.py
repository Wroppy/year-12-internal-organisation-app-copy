from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from display.assignmentEventWidget.assignment import Assignment
from display.assignmentEventWidget.widgetHolder import WidgetHolder
from display.assignmentEventWidget.assignmentHeaders import Header


class ActiveWidgetDisplay(QWidget):
    def __init__(self):
        super(ActiveWidgetDisplay, self).__init__()
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
        pass

    def styleWidgets(self):
        STYLE = f"""
            QScrollArea{{
                border: none;
            }}
        """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication()
    display = ActiveWidgetDisplay()
    display.show()
    app.exec()
