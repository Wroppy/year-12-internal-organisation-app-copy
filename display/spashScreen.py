from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
import resourceManager.resources
from PySide6.QtGui import *
import time

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.setCursor(QCursor(Qt.ArrowCursor))
        pixmap = QPixmap(":/appIcons/splashScreen.png")
        self.setPixmap(pixmap.scaled(500,260))
        self.setMask(self.mask())
        self.font = QFont()
        self.font.setPointSize(15)
        self.setFont(self.font)

        self.show()

    def displayMessage(self, message: str):
        self.showMessage(f"{message}...", alignment=Qt.AlignBottom | Qt.AlignRight)
        self.font.setPointSize(15)
        self.setFont(self.font)
        time.sleep(1)


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        s = SplashScreen()
        s.displayMessage("Loading Database")
        s.displayMessage("Loading Application")
        s.finish(self)


if __name__ == '__main__':
    app = QApplication()
    display = TestWindow()
    display.show()

    app.exec()
