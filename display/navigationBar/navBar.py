from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.navigationBar import navButton, navHeader
from resourceManager.internalDataHandler import *


class NavBar(QWidget):
    def __init__(self):
        super(NavBar, self).__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.buttons = {}

        self.header = navHeader.NavHeader()

        self.layout.addWidget(self.header)
        self.createNavButtons()

        self.setPresets()

        self.styleWidgets()

    def setPresets(self):
        """
        Sets the presets for the widget

        :return: None
        """

        self.setFixedWidth(self.header.width())

    def createNavButtons(self):
        """
        Creates buttons given the name and the icon

        :return: None

        """
        # Creates the frame for the buttons
        # This is done so there is a different colour for the spacing between buttons
        self.buttonFrame = QWidget()
        buttonFrameLayout = QVBoxLayout(self.buttonFrame)
        buttonFrameLayout.setSpacing(1)
        buttonFrameLayout.setContentsMargins(0, 0, 0, 1)

        self.layout.addWidget(self.buttonFrame)

        # Creates the buttons
        buttonNames = ["Timetable", "Assignments", "Events", "Quick Links", "Settings"]
        buttonIcons = ["timetable", "task", "list", "link", "settings"]
        buttonName = "navButtons"

        for i in range(len(buttonNames)):
            button = navButton.NavButton(buttonNames[i], buttonIcons[i])
            buttonFrameLayout.addWidget(button)
            button.setObjectName(buttonName)

            self.buttons[buttonNames[i]] = button

        self.layout.addStretch()

    def styleWidgets(self):
        """
        Styles all of the widgets in the nav bar

        :return: None
        """
        colours = loadJsonFile("settings\\colours")

        style = f"""
            QPushButton#navButtons{{
                border: none;
                background-color: rgb{tuple(colours["buttonColour"])};
                color: rgb{tuple(colours["navBarTextColour"])}
            }}
            
            QPushButton#navButtons::hover{{
                background-color: rgb{tuple(colours["buttonHoverColour"])};
            }}
        """

        self.setStyleSheet(style)

        self.setAutoFillBackground(True)
        backgroundColour = colours["buttonColour"]
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(backgroundColour[0], backgroundColour[1], backgroundColour[2]))
        self.setPalette(palette)

        self.buttonFrame.setAutoFillBackground(True)
        backgroundColour = colours["navBarFrameColour"]
        palette = self.buttonFrame.palette()
        palette.setColor(QPalette.Window, QColor(backgroundColour[0], backgroundColour[1], backgroundColour[2]))
        self.buttonFrame.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NavBar()
    window.show()
    app.exec()
