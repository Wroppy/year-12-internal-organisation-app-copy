"""
This file houses the button for the navigation bar
In order to improve accessibility for people with poor eyesight,
or even if they speak another language, a heading and icon will be present.

"""
from PySide6 .QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
import resourceManager.resources


class NavButton(QPushButton):
    def __init__(self, heading: str, iconName: str):
        super(NavButton, self).__init__()

        horizontalLayout = QHBoxLayout(self)
        name = "NavButton"
        self.setObjectName(name)

        height = 60
        width = 200

        self.setFixedSize(width, height)

        text = QLabel(heading)

        icon = QLabel()
        pixmapPath = ":/buttonIcons/" + iconName + ".png"
        pixmap = QPixmap()
        pixmap.load(pixmapPath)
        icon.setPixmap(pixmap.scaledToHeight(height - 20))

        horizontalLayout.addWidget(text)

        horizontalLayout.addStretch()

        horizontalLayout.addWidget(icon)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NavButton("Name", "generic")
    window.show()
    app.exec()
