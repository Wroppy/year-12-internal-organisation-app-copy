from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
import resourceManager.resources
from typing import *

class AddAssignmentDialog(QDialog):
    def __init__(self, parent: QWidget, errorText: Union[str, None], assignmentName: Union[str, None]):
        super(AddAssignmentDialog, self).__init__(parent=parent)
        # Sets the window icon, title, and size
        APPICON = QIcon(":/appIcons/appIcon.png")
        self.setWindowIcon(APPICON)

        self.resize(300, 100)

        TITLE = "Add Assignment"
        self.setWindowTitle(TITLE)

        layout = QVBoxLayout(self)

        # This widget is for the label and the entry box
        assignmentWidget = QWidget()
        assignmentLayout = QHBoxLayout(assignmentWidget)
        assignmentLayout.setContentsMargins(0, 0, 0, 0)

        # Will display an error message if one is parsed through
        if errorText is not None:
            errorLabel = QLabel(errorText)
            errorLabel.setStyleSheet("color: red")
            layout.addWidget(errorLabel)

        # Creates a label for the entry box
        assignmentLabel = QLabel("Assignment")
        assignmentLayout.addWidget(assignmentLabel)

        # Creates an entry box for user to input their assignment
        self.assignmentEntry = QLineEdit()
        self.assignmentEntry.setText(assignmentName)
        assignmentLayout.addWidget(self.assignmentEntry)

        layout.addWidget(assignmentWidget)

        # Creates the button box
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)


if __name__ == '__main__':
    app = QApplication()
    display = AddAssignmentDialog(None)
    display.show()
    app.exec()
