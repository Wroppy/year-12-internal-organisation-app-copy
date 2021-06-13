"""
This class handles the widgets nested inside of the Active Assignment Widget

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from display.assignmentWidget.assignment import Assignment
from resourceManager.internalDataHandler import *

colour = loadJsonFile("settings\\colours")


class ActiveAssignmentWidget(QWidget):
    def __init__(self, assignment: Assignment):
        super(ActiveAssignmentWidget, self).__init__()
        self.setObjectName("AssignmentWidget")
        layout = QHBoxLayout(self)

        self.radioButton = QRadioButton()
        self.radioButton.setObjectName("selectAssignmentButton")
        layout.addWidget(self.radioButton)

        title = QLabel(assignment.title)
        #title.setWordWrap(True)
        layout.addWidget(title)

        description = QLabel(assignment.description)
        #description.setWordWrap(True)
        layout.addWidget(description)

        layout.addStretch()

        completedLabel = QLabel("Complete")
        layout.addWidget(completedLabel)

        self.completedButton = QRadioButton()
        layout.addWidget(self.completedButton)

        style = f"""
        QRadioButton#selectAssignmentButton{{
            border-right: 1px solid rgb{tuple(colour["buttonColour"])};
        }}
        
        
        QWidget#assignmentWidget{{
            border-bottom: solid 1px rgb{tuple(colour["buttonColour"])};
        }}

        """
        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication()
    display = ActiveAssignmentWidget(Assignment("Title", "Description", False))
    display.show()

    app.exec()
