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
from display.account.accountWidget import AccountWidget


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
            AccountWidget()
        ]
        for page in PAGES:
            self.windowPages.addWidget(page)

        self.addNavButtonFunction()

    def switchPage(self, index: int):
        self.windowPages.setCurrentIndex(index)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Because there is no layout, the widgets be resized and moved in this function

        :param event: QResizeEvent
        :return: None
        """

        # Resizes the nav bar to the height of the window
        self.navBar.resize(self.navBar.width(), self.height())

        if self.navBar.isExtended():
            self.shrinkContentWidget()
        else:
            self.enlargeContentWidget()



    def addNavButtonFunction(self):
        for i in range(len(self.navBar.buttons)):
            self.navBar.buttons[i].clicked.connect(lambda checked=False, index=i: self.switchPage(index))

        self.navBar.header.hamburgerButton.clicked.connect(lambda: self.hamburgerButtonClicked())

    def hamburgerButtonClicked(self):
        """
        Will collapse or extend the nav bar and resize the widgets

        :return: None
        """
        if self.navBar.isExtended():
            self.collapseNavBar()
            self.enlargeContentWidget()

        else:
            self.extendNavBar()
            self.shrinkContentWidget()


        self.navBar.changeExtended()
        print(self.navBar.isExtended())

    def extendNavBar(self):
        self.navBar.move(QPoint(0, 0))
        self.navBar.header.moveButtonExtended()

    def collapseNavBar(self):
        self.navBar.move(QPoint(-144, 0))
        self.navBar.header.moveButtonCollapsed()

    def shrinkContentWidget(self):
        resizeWidth = self.width() - self.navBar.width()

        self.windowPages.resize(QSize(resizeWidth, self.height()))
        self.windowPages.move(QPoint(200, 0))

    def enlargeContentWidget(self):
        # Resizes the content widget and repositions it


        resizeWidth = self.width() - 56
        self.windowPages.resize(QSize(resizeWidth, self.height()))
        self.windowPages.move(QPoint(56, 0))

if __name__ == '__main__':
    app = QApplication()
    display = MainWindow()
    display.show()

    app.exec()
