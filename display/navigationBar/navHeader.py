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
    WIDTH = 200
    HEIGHT = 60

    def __init__(self):
        super(NavHeader, self).__init__()
        self.layout = QHBoxLayout(self)

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.createButton()
        self.createLabel()

        self.styleWidgets()

    def createButton(self):
        """
        Creates the button for the nav header

        :return: None
        """
        ICONPATH = ":/buttonIcons/hamburger.png"
        self.hamburgerButton = QPushButton(self)
        self.hamburgerButton.setIcon(QIcon(ICONPATH))
        self.hamburgerButton.setFixedSize(self.HEIGHT, self.HEIGHT)
        self.hamburgerButton.setIconSize(QSize(self.HEIGHT - 20, self.HEIGHT - 20))
        self.hamburgerButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.hamburgerButton.move(0, 0)
        BUTTONNAME = "headerButton"
        self.hamburgerButton.setObjectName(BUTTONNAME)

        # self.layout.addWidget(self.hamburgerButton)

    def createLabel(self):
        self.label = QLabel(self)
        self.label.setText("Organiser")

        LABELNAME = "headerLabel"
        self.label.setObjectName(LABELNAME)

        self.label.move(65, 15)

    def styleWidgets(self):
        """
        Styles the widgets nested inside of the widget

        :return: None
        """
        COLOURS = loadJsonFile("settings\\colours")
        FONT = loadJsonFile("settings\\fonts")

        STYLE = f"""
            QPushButton#headerButton{{
                border: none;
            }}
            
            QLabel#headerLabel{{
                font-size: {FONT["headerSize"]}px;
                color: rgb{tuple(COLOURS["navBarTextColour"])};
            }}
        """

        self.setStyleSheet(STYLE)

        # Sets the background colour to a dark grey
        self.setAutoFillBackground(True)
        BACKGROUNDCOLOUR = COLOURS["headerColour"]
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(BACKGROUNDCOLOUR[0], BACKGROUNDCOLOUR[1], BACKGROUNDCOLOUR[2]))
        self.setPalette(palette)

    def moveButtonCollapsed(self):
        self.hamburgerButton.move(144, 0)

    def moveButtonExtended(self):
        self.hamburgerButton.move(0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = NavHeader()
    window.show()
    app.exec()
