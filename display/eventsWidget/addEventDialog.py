import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
import resourceManager.resources
from typing import *


class AddEventDialog(QDialog):
    def __init__(self, parent: QWidget, errorText):
        super(AddEventDialog, self).__init__(parent=parent)
        APPICON = QIcon(":/appIcons/appIcon.png")
        self.setWindowIcon(APPICON)

        self.resize(300, 100)
        TITLE = "Add Event"
        self.setWindowTitle(TITLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        if errorText is not None:
            errorLabel = QLabel(errorText)
            errorLabel.setStyleSheet("color: red")
            layout.addWidget(errorLabel)

        # This widget is for the label and the entry box
        eventWidget = QWidget()
        eventLayout = QHBoxLayout(eventWidget)
        eventLayout.setContentsMargins(0, 0, 0, 0)

        # Creates a label for the entry box
        eventLabel = QLabel("Event")
        eventLayout.addWidget(eventLabel)

        # Creates an entry box for user to input their event
        self.eventEntry = QLineEdit()
        eventLayout.addWidget(self.eventEntry)

        layout.addWidget(eventWidget)

        # Creates the widget that asks the user for the date
        dateWidget = self.createDateWidget()
        layout.addWidget(dateWidget)

        # Creates the widget that asks for the user's time
        timeWidget = self.createTimeWidget()
        layout.addWidget(timeWidget)

        layout.addStretch()

        # Creates the button box
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def createDateWidget(self) -> QWidget:
        """
        Creates a widget that asks the user for the year

        :return: QWidget
        """

        dateWidget = QWidget()
        dateLayout = QHBoxLayout(dateWidget)
        dateLayout.setContentsMargins(0, 0, 0, 0)

        dateLabel = QLabel("Notify Date: (DD/MM/YY)")

        time = datetime.datetime.now()

        self.dateDay = QSpinBox()
        self.dateDay.setMinimum(1)
        self.dateDay.setMaximum(31)
        self.dateDay.setValue(time.day)

        self.dateMonth = QSpinBox()
        self.dateMonth.setMinimum(1)
        self.dateMonth.setMaximum(12)
        self.dateMonth.setValue(time.month)

        self.dateYear = QSpinBox()
        self.dateYear.setMinimum(time.year)
        dateLayout.addWidget(dateLabel)
        dateLayout.addStretch()
        dateLayout.addWidget(self.dateDay)
        dateLayout.addWidget(self.dateMonth)
        dateLayout.addWidget(self.dateYear)

        return dateWidget

    def createTimeWidget(self) -> QWidget:
        """
        Creates a widget that asks the user for the year

        :return: QWidget
        """

        notifyTimeWidget = QWidget()
        notifyTimeLayout = QHBoxLayout(notifyTimeWidget)
        notifyTimeLayout.setContentsMargins(0, 0, 0, 0)

        time = datetime.datetime.now()

        notifyTimeLabel = QLabel("Notify Time (24Hr Time):")
        self.notifyTimeHour = QSpinBox()
        self.notifyTimeHour.setValue(time.hour)
        self.notifyTimeHour.setMaximum(23)

        self.notifyTimeMinute = QSpinBox()
        self.notifyTimeMinute.setValue(time.minute)
        self.notifyTimeMinute.setMaximum(59)

        notifyTimeLayout.addWidget(notifyTimeLabel)
        notifyTimeLayout.addStretch()
        notifyTimeLayout.addWidget(self.notifyTimeHour)
        notifyTimeLayout.addWidget(self.notifyTimeMinute)

        return notifyTimeWidget


if __name__ == '__main__':
    app = QApplication()
    display = AddEventDialog(None)
    display.show()
    app.exec()
