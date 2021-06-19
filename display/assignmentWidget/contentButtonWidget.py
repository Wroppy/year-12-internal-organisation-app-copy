from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from resourceManager.internalDataHandler import *


class ContentButtonWidget(QWidget):
    def __init__(self, addButtonText: str, deleteButtonText: str):
        super(ContentButtonWidget, self).__init__(None)

        # Sets a fixed height for the widget
        HEIGHT = 69
        self.setFixedHeight(HEIGHT)

        # Creates the layout and adds a spacer to it
        layout = QHBoxLayout(self)
        layout.addStretch()

        # Creates an add button
        self.addButton = QPushButton(addButtonText)
        layout.addWidget(self.addButton)

        # Creates a delete button
        self.deleteButton = QPushButton(deleteButtonText)
        layout.addWidget(self.deleteButton)
        colours = loadJsonFile("settings\\colours")

        # Styles the widgets
        STYLE = f""" 
            QPushButton{{
                border: none;
                font-size: 15px;
                color: white;
                background-color: rgb{tuple(colours["buttonColour"])};
                padding: 10px 15px;

            }}
            
            QPushButton::hover{{
                background-color: rgb{tuple(colours["buttonHoverColour"])}
            }}
                """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = ContentButtonWidget("add text", "delete text")
    display.show()
    app.exec()
