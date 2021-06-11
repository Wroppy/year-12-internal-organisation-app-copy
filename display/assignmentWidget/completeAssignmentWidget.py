from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from display.assignmentWidget.assignment import Assignment


class CompletedAssignement(QWidget):
    def __init__(self, assignment: Assignment):
        super(CompletedAssignement, self).__init__()
        layout = QHBoxLayout(self)

        label = QLabel(assignment.title)
        label.setWordWrap(True)
        layout.addWidget(label)

        layout.addStretch()

        spacerLeft = QLabel("|")
        spacerRight = QLabel("|")
        completeLabel = QLabel("Completed")

        radioButton = QRadioButton()
        radioButton.setChecked(True)
        radioButton.setEnabled(False)

        layout.addWidget(spacerLeft)
        layout.addWidget(completeLabel)
        layout.addWidget(radioButton)
        layout.addWidget(spacerRight)



if __name__ == '__main__':
    app = QApplication()
    display = CompletedAssignement(Assignment("Nice", "nice", True))
    display.show()
    app.exec()





