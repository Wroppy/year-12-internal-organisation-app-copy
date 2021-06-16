"""
This file houses the button for the navigation bar
In order to improve accessibility for people with poor eyesight,
or even if they speak another language, a heading and icon will be present.

"""
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
import resourceManager.resources
from resourceManager.internalDataHandler import *


class NavButton(QToolButton):
    def __init__(self, heading: str, iconName: str):
        super(NavButton, self).__init__()
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        name = "NavButton"
        self.setObjectName(name)

        height = 60
        width = 200

        self.setFixedSize(width, height)

        pixmapPath = ":/buttonIcons/" + iconName + ".png"

        self.setText(heading)

        self.setIcon(QIcon(pixmapPath))
        self.setIconSize(QSize(32, 32))

        self.setLayoutDirection(Qt.RightToLeft)

        self.styleButton()

    def styleButton(self):
        colours = loadJsonFile("settings\\colours")
        style = f"""
            QToolButton {{
                color: rgb{tuple(colours["navBarTextColour"])};
                padding: 0px 12px;
                font-size: 14px;
            }}
            
        """

        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NavButton("Name", "hamburger")
    window.show()
    app.exec()
