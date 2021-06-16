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

colours = loadJsonFile("settings\\colours")


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

        # Styles the buttons to its colours
        style = f"""
            QPushButton{{
                border: none;
                background-color: rgb{tuple(colours["buttonColour"])};
                color: rgb{tuple(colours["navBarTextColour"])};
                border-bottom: 1px solid rgb{tuple(colours["navBarFrameColour"])};
                padding: 12px 14px;
            }}  
            
            QPushButton::hover{{
                background-color: rgb{tuple(colours["buttonHoverColour"])};
            }}
        """

        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication()

    display = ButtonWidget()
    display.show()
    app.exec()
