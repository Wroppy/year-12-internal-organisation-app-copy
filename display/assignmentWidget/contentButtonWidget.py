from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from resourceManager.internalDataHandler import *


class ContentButtonWidget(QWidget):
    def __init__(self, addButtonText: str, editButtonText: str, deleteButtonText: str):
        super(ContentButtonWidget, self).__init__(None)

        height = 69
        self.setFixedHeight(height)

        layout = QHBoxLayout(self)

        layout.addStretch()

        self.addButton = QPushButton(addButtonText)
        layout.addWidget(self.addButton)

        self.editButton = QPushButton(editButtonText)
        layout.addWidget(self.editButton)

        self.deleteButton = QPushButton(deleteButtonText)
        layout.addWidget(self.deleteButton)
        colours = loadJsonFile("settings\\colours")

        style = f""" 
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

        self.setStyleSheet(style)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = ContentButtonWidget("add text", "edit text", "delete text")
    display.show()
    app.exec()
