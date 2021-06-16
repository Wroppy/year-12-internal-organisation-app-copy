from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.navigationBar import navBar
from display.timetableWidget.timetableWidget import TimetablePageWidget
from display.quickLinksWidget.quickLinksWidget import QuickLinksPage


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createWidgets()

    def createWidgets(self):
        """
        Creates the widgets for the main window

        Because the nav bar and extend and retract, there will be no layout

        :return: None
        """

        self.navBar = navBar.NavBar(self)

        # Because the widow cannot be shorter than the nav bar, this function makes it not allowed
        MINIMUMWIDTH = 750
        self.setMinimumSize(MINIMUMWIDTH, self.navBar.height())

        # Creates the pages for the app
        self.windowPages = QStackedWidget(self)
        self.windowPages.move(self.navBar.width(), 0)
        PAGES = [
            TimetablePageWidget(),
            QLabel("Assignments"),
            QLabel("Events"),
            QuickLinksPage(),
            QLabel("Account")
        ]
        for page in PAGES:
            self.windowPages.addWidget(page)

        self.addNavButtonFunction()

    def addNavButtonFunction(self):
        for i in range(len(self.navBar.buttons)):
            print(i)
            self.navBar.buttons[i].clicked.connect(lambda checked=False, index=i: self.switchPage(index))

    def switchPage(self, index: int):
        print(index)
        self.windowPages.setCurrentIndex(index)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Because there is no layout, the widgets be resized and moved in this function

        :param event: QResizeEvent
        :return: None
        """

        # Resizes the nav bar to the height of the window
        self.navBar.resize(self.navBar.width(), self.height())

        resizeWidth = self.width() - self.navBar.width()
        self.windowPages.resize(resizeWidth, self.height())

if __name__ == '__main__':
    app = QApplication()
    display = MainWindow()
    display.show()

    app.exec()
