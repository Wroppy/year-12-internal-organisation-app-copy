from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys


class AddClassDialog(QDialog):
    def __init__(self, parent=None):
        super(AddClassDialog, self).__init__(parent=parent)
        title = "Add Class"
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Asks for the user's class
        classWidget = QWidget()
        classLayout = QHBoxLayout(classWidget)
        classLayout.setContentsMargins(0, 0, 0, 0)

        classNameLabel = QLabel("Class:")
        self.classNameEntry = QLineEdit()

        classLayout.addWidget(classNameLabel)
        classLayout.addWidget(self.classNameEntry)

        layout.addWidget(classWidget)

        # Asks for the start and end time
        startTimeWidget = QWidget()
        startTimeLayout = QHBoxLayout(startTimeWidget)
        startTimeLayout.setContentsMargins(0, 0, 0, 0)

        startTimeLabel = QLabel("Beginning Time (24Hr Time)")
        self.startTimeHour = QSpinBox()
        self.startTimeHour.setMaximum(23)

        self.startTimeMinute = QSpinBox()
        self.startTimeMinute.setMaximum(59)

        startTimeLayout.addWidget(startTimeLabel)
        startTimeLayout.addStretch()
        startTimeLayout.addWidget(self.startTimeHour)
        startTimeLayout.addWidget(self.startTimeMinute)

        layout.addWidget(startTimeWidget)

        endTimeWidget = QWidget()
        endTimeLayout = QHBoxLayout(endTimeWidget)
        endTimeLayout.setContentsMargins(0, 0, 0, 0)

        endTimeLabel = QLabel("Ending Time (24Hr Time)")
        self.endTimeHour = QSpinBox()
        self.endTimeMinute = QSpinBox()

        self.endTimeHour.setMaximum(24)
        self.endTimeMinute.setMaximum(59)
        endTimeLayout.addWidget(endTimeLabel)
        endTimeLayout.addStretch()
        endTimeLayout.addWidget(self.endTimeHour)
        endTimeLayout.addWidget(self.endTimeMinute)

        layout.addWidget(endTimeWidget)


        layout.addStretch()

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)


if __name__ == '__main__':
    app = QApplication()
    display = AddClassDialog()
    display.show()
    app.exec()
