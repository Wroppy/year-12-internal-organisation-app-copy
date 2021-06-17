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


class NavButton(QToolButton):
    HEIGHT = 60
    WIDTH = 200

    def __init__(self, heading: str, iconName: str):
        super(NavButton, self).__init__()
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        NAME = "NavButton"
        self.setObjectName(NAME)

        # Sets dimensions of widget
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self.setText(heading)

        # Sets the icon for the button
        PIXMAPPATH = ":/buttonIcons/" + iconName + ".png"
        self.setIcon(QIcon(PIXMAPPATH))
        self.setIconSize(QSize(32, 32))

        self.setLayoutDirection(Qt.RightToLeft)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NavButton("Name", "hamburger")
    window.show()
    app.exec()
