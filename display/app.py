from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys


class Display(QMainWindow):
    def __init__(self):
        super(Display, self).__init__(None)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    display = Display()
    display.show()
    app.exec()
