"""
Created the button widget for the timetable page

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from resourceManager.internalDataHandler import loadJsonFile


class ButtonWidget(QWidget):
    def __init__(self):
        super(ButtonWidget, self).__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Adds 2 buttons to the page
        self.newButton = QPushButton("New Class")
        self.deleteButton = QPushButton("Delete Class")

        self.newButton.setCursor(Qt.PointingHandCursor)
        self.deleteButton.setCursor(Qt.PointingHandCursor)

        layout.addStretch()
        layout.addWidget(self.newButton)
        layout.addWidget(self.deleteButton)

        COLOURS = loadJsonFile("settings\\colours")
        # Styles the buttons to its colours
        STYLE = f""" 
            QPushButton{{
                border: none;
                font-size: 15px;
                color: white;
                background-color: rgb{tuple(COLOURS["buttonColour"])};
                padding: 10px 15px;

            }}

            QPushButton::hover{{
                background-color: rgb{tuple(COLOURS["buttonHoverColour"])}
            }}
                """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication()

    display = ButtonWidget()
    display.show()
    app.exec()
