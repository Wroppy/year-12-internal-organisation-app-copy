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
    def __init__(self, parent=None):
        super(NavBar, self).__init__(parent=parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.buttons = []

        self.header = navHeader.NavHeader()

        self.layout.addWidget(self.header)
        self.createNavButtons()

        self.setPresets()

        self.styleWidgets()

        self.extended = True

    def isExtended(self):
        return self.extended

    def changeExtended(self):
        self.extended = not self.extended

    def setPresets(self):
        """
        Sets the presets for the widget

        :return: None
        """

        self.setFixedWidth(self.header.WIDTH)

    def createNavButtons(self):
        """
        Creates buttons given the name and the icon

        :return: None

        """

        # Creates the buttons
        BUTTONNAMES = ["Timetable", "Assignments", "Events", "Quick Links", "Account"]
        BUTTONICONS = ["timetable", "task", "list", "link", "user"]
        BUTTONNAME = "navButtons"

        # Loops through and creates a button for each name in the list
        for i in range(len(BUTTONNAMES)):
            button = navButton.NavButton(BUTTONNAMES[i], BUTTONICONS[i])
            self.layout.addWidget(button)
            button.setObjectName(BUTTONNAME)

            self.buttons.append(button)
        self.layout.addStretch()

        # Makes the minimum height of the nav bar the header height + all of the button's heights
        MINIMUMHEIGHT = self.header.HEIGHT + navButton.NavButton.HEIGHT * len(self.buttons)
        self.setMinimumHeight(MINIMUMHEIGHT)

    def styleWidgets(self):
        """
        Styles all of the widgets in the nav bar

        :return: None
        """
        COLOURS = loadJsonFile("settings\\colours")

        STYLE = f"""
            QToolButton#navButtons{{
                border: none;
                background-color: rgb{tuple(COLOURS["buttonColour"])};
                color: rgb{tuple(COLOURS["navBarTextColour"])};
                border-bottom: 1px solid rgb{tuple(COLOURS["navBarFrameColour"])};
                padding: 0px 10px;
                font-size: 14px;
            }}  
            
            QToolButton#navButtons::hover{{
                background-color: rgb{tuple(COLOURS["buttonHoverColour"])};
            }}
            
        """

        self.setStyleSheet(STYLE)

        # Sets the background colour to a grey
        self.setAutoFillBackground(True)
        BACKGROUNDCOLOUR = COLOURS["buttonColour"]
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(BACKGROUNDCOLOUR[0], BACKGROUNDCOLOUR[1], BACKGROUNDCOLOUR[2]))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NavBar()
    window.show()
    app.exec()
