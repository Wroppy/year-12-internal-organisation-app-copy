"""
This class creates a simple yes/no dialog window with a label

"""


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys


class ConfirmDialog(QDialog):
    def __init__(self, text: str):
        super(ConfirmDialog, self).__init__()
        TITLE = "Confirm"
        self.setWindowTitle(TITLE)
        layout = QVBoxLayout(self)

        # Creates the label for the dialog window
        labelWidget = QWidget()
        labelLayout = QHBoxLayout(labelWidget)

        label = QLabel(text)
        labelLayout.addStretch()
        labelLayout.addWidget(label)
        labelLayout.addStretch()

        layout.addWidget(labelWidget)

        # Creates the button box
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

if __name__ == '__main__':
    app = QApplication()
    display = ConfirmDialog("Are you sure?")
    display.show()
    app.exec()