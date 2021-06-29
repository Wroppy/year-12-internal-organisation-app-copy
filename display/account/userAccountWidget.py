"""
Not Used in Internal


"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *


class UserSigedInWidget(QWidget):
    def __init__(self):
        super(UserSigedInWidget, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Creates the label
        descriptionWidget = self.returnCenteredWidget(QLabel("You Have Successfully Logged In"))
        layout.addWidget(descriptionWidget)

    def returnCenteredWidget(self, *widgets) -> QWidget:
        """
        Takes a number of widgets that adds it to a parent widget, spacing it horizontally

        :param widgets: args -> List[QWidget]
        :return: QWidget
        """

        hWidget = QWidget()
        hLayout = QHBoxLayout(hWidget)
        hLayout.setContentsMargins(0, 0, 0, 0)

        hLayout.addStretch()
        for widget in widgets:
            hLayout.addWidget(widget)

        hLayout.addStretch()

        return hWidget


if __name__ == '__main__':
    app = QApplication()

    display = UserSigedInWidget()
    display.show()

    app.exec()
