from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from resourceManager.internalDataHandler import *

colours = loadJsonFile("settings\\colours")
fonts = loadJsonFile("settings\\fonts")


class CompletedAssignment(QWidget):
    def __init__(self, assignment):
        super(CompletedAssignment, self).__init__()
        self.setObjectName("AssignmentWidget")
        layout = QHBoxLayout(self)

        title = QLabel(assignment.title)
        # title.setWordWrap(True)
        layout.addWidget(title)

        layout.addStretch()

        completeLabel = QLabel("Completed")
        completeLabel.setObjectName("completedLabel")

        radioButton = QRadioButton()
        radioButton.setChecked(True)
        radioButton.setEnabled(False)

        layout.addWidget(completeLabel)
        layout.addWidget(radioButton)

        style = f"""
        QWidget#assignmentWidget{{
            border-bottom: solid 1px rgb{tuple(colours["buttonColour"])};
        }}

        """
        self.setStyleSheet(style)
