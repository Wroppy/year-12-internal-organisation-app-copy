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

        # Creates the






if __name__ == '__main__':
    app = QApplication()

    display = UserSigedInWidget()
    display.show()

    app.exec()
