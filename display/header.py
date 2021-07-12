from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from resourceManager.internalDataHandler import loadJsonFile


class Header(QWidget):
    def __init__(self, headerWidget: QWidget):
        super(Header, self).__init__()
        layout = QHBoxLayout(self)

        HEIGHT = 60
        self.setFixedHeight(HEIGHT)

        # Creates the header label for the header
        layout.addWidget(headerWidget)

        #layout.addStretch()

        # Styles the label
        COLOURS = loadJsonFile("settings\\colours")
        STYLE = f"""
            QLabel{{
                font-size: 16px;
                color: rgb{tuple(COLOURS["navBarTextColour"])}
            }}
        """

        self.setStyleSheet(STYLE)

        # Sets the background colour
        self.setAutoFillBackground(True)
        BACKGROUNDCOLOUR = COLOURS["buttonColour"]
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(BACKGROUNDCOLOUR[0], BACKGROUNDCOLOUR[1], BACKGROUNDCOLOUR[2]))
        self.setPalette(palette)


if __name__ == '__main__':
    app = QApplication()

    display = Header(QLabel("1"))
    display.show()

    app.exec()
