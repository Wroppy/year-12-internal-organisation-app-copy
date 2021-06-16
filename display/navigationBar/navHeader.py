from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.widgetTemplate import WidgetTemplate
import resourceManager.resources
from resourceManager.internalDataHandler import *


class NavHeader(QWidget):
    def __init__(self):
        super(NavHeader, self).__init__()
        self.layout = QHBoxLayout(self)
        width = 200
        height = 60

        self.setFixedSize(width, height)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.createButton()
        self.createLabel()

        self.styleWidgets()

    def createButton(self):
        """
        Creates the button for the nav header

        :return: None
        """
        iconPath = ":/buttonIcons/hamburger.png"
        self.hamburgerButton = QPushButton(self)
        self.hamburgerButton.setIcon(QIcon(iconPath))
        self.hamburgerButton.setFixedSize(self.height(), self.height())
        self.hamburgerButton.setIconSize(QSize(self.height() - 20, self.height() - 20))
        self.hamburgerButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.hamburgerButton.move(0, 0)
        buttonName = "headerButton"
        self.hamburgerButton.setObjectName(buttonName)

        # self.layout.addWidget(self.hamburgerButton)

    def createLabel(self):
        self.label = QLabel(self)
        self.label.setText("Organiser")

        labelName = "headerLabel"
        self.label.setObjectName(labelName)

        self.label.move(70, 15)

    def styleWidgets(self):
        """
        Styles the widgets nested inside of the widget

        :return: None
        """
        colours = loadJsonFile("settings\\colours")
        font = loadJsonFile("settings\\fonts")

        style = f"""
            QPushButton#headerButton{{
                border: none;
            }}
            
            QLabel#headerLabel{{
                font-size: {font["headerSize"]}px;
                color: rgb{tuple(colours["navBarTextColour"])};
            }}
        """

        self.setStyleSheet(style)

        self.setAutoFillBackground(True)
        backgroundColour = colours["headerColour"]
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(backgroundColour[0], backgroundColour[1], backgroundColour[2]))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NavHeader()
    window.show()
    app.exec()
