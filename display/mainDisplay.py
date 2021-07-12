from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.navigationBar import navBar
from display.spashScreen import SplashScreen
from display.timetableWidget.timetableWidget import TimetablePageWidget
from display.quickLinksWidget.quickLinksWidget import QuickLinksPage
from display.assignmentWidget.assignmentPage import AssignmentPage
from resourceManager.resourceHandler import ResourceHandler
from display.eventsWidget.eventPage import EventPage
from notifications.notificationHandler import *
import resourceManager.resources
import threading


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.threadPool = QThreadPool()

        APPICON = QIcon(":/appIcons/appIcon.png")
        APPNAME = "Organiser"

        self.setWindowIcon(APPICON)
        self.setWindowTitle(APPNAME)

        splashScreen = SplashScreen()

        splashScreen.displayMessage("Connecting To Notification Manager")

        self.resourceManager = ResourceHandler(self.threadPool)

        self.notificationManager = NotificationHandler(self.resourceManager)
        self.startNotificationThread()
        # threading.Thread(target=self.notificationManager.startLoop).start()

        splashScreen.displayMessage("Creating Widgets")
        self.createWidgets()

        splashScreen.displayMessage("Creating Cool Animations")
        self.animationTime = 300
        self.createAnimations()

        splashScreen.displayMessage("Launching Window")

        self.animating = False

    def startNotificationThread(self):
        worker = NotificationWorker(self.notificationManager)
        self.threadPool.start(worker)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Closes the window, and stops the notification handler

        event: QCloseEvent
        """
        super().closeEvent(event)
        self.notificationManager.running = False

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
            TimetablePageWidget(self.resourceManager),
            AssignmentPage(self.resourceManager),
            EventPage(self.resourceManager, self.notificationManager),
            QuickLinksPage(),
            QLabel("Accounts, Coming Soon!")
        ]
        for page in PAGES:
            self.windowPages.addWidget(page)

        self.addNavButtonFunction()

    def switchPage(self, index: int):
        """
        Switches the pages of the widget given the index

        :param index: int

        """
        self.windowPages.setCurrentIndex(index)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Because there is no layout, the widgets are resized and moved in this function
        Overrides the resizeEvent from QMainWindow

        :param event: QResizeEvent
        :return: None
        """

        # Resizes the nav bar to the height of the window
        self.navBar.resize(self.navBar.width(), self.height())
        if self.animating:
            self.stopAnimations()


        if self.navBar.isExtended():
            self.shrinkContentWidget()
        else:
            self.enlargeContentWidget()

        if self.animating:
            self.hamburgerButtonClicked()



    def addNavButtonFunction(self):
        """
        When these buttons are clicked, will do certain commands

        :return: None
        """
        for i in range(len(self.navBar.buttons)):
            self.navBar.buttons[i].clicked.connect(lambda checked=False, index=i: self.switchPage(index))

        self.navBar.header.hamburgerButton.clicked.connect(lambda: self.hamburgerButtonClicked())

    def createAnimations(self):
        """
        Creates the animation variables for later

        :return: None
        """
        self.navBarPosAnimation = QPropertyAnimation(self.navBar, b"pos")
        self.navBarPosAnimation.setEasingCurve(QEasingCurve.InOutCubic)

        self.navbarHamburgerButtonAnimation = QPropertyAnimation(self.navBar.header.hamburgerButton, b"pos")
        self.navbarHamburgerButtonAnimation.setEasingCurve(QEasingCurve.InOutCubic)

        self.contentPosAnimation = QPropertyAnimation(self.windowPages, b"pos")
        self.contentPosAnimation.setEasingCurve(QEasingCurve.InOutCubic)

        self.contentSizeAnimation = QPropertyAnimation(self.windowPages, b"size")
        self.contentSizeAnimation.setEasingCurve(QEasingCurve.InOutCubic)

    def hamburgerButtonClicked(self):
        """
        Will collapse or extend the nav bar and resize the widgets

        :return: None
        """

        if self.navBar.isExtended():
            self.animating = True

            self.collapseNavbarAnimate()
            self.enlargeContentWidgetAnimate()

            self.closeNavBarAnimate()

            # self.collapseNavBar()
            # self.enlargeContentWidget()

        else:
            self.animating = True
            self.enlargeNavBarAnimate()
            self.shrinkContentWidgetAnimate()

            self.openNavBarAnimation()
            # self.extendNavBar()
            # self.shrinkContentWidget()

    def closeNavBarAnimate(self):
        """
        Closes the nav bar

        :return: None
        """


        self.closeNavBarAnimationGroup = QParallelAnimationGroup(self)
        self.closeNavBarAnimationGroup.finished.connect(self.animationFinished)

        self.closeNavBarAnimationGroup.addAnimation(self.contentPosAnimation)
        self.closeNavBarAnimationGroup.addAnimation(self.contentSizeAnimation)
        self.closeNavBarAnimationGroup.addAnimation(self.navBarPosAnimation)
        self.closeNavBarAnimationGroup.addAnimation(self.navbarHamburgerButtonAnimation)

        self.closeNavBarAnimationGroup.start()

    def openNavBarAnimation(self):
        """
        Opens the nav bar

        :return: None
        """
        self.openNavBarAnimationGroup = QParallelAnimationGroup(self)
        self.openNavBarAnimationGroup.finished.connect(self.animationFinished)

        self.openNavBarAnimationGroup.addAnimation(self.contentPosAnimation)
        self.openNavBarAnimationGroup.addAnimation(self.contentSizeAnimation)
        self.openNavBarAnimationGroup.addAnimation(self.navBarPosAnimation)
        self.openNavBarAnimationGroup.addAnimation(self.navbarHamburgerButtonAnimation)

        self.openNavBarAnimationGroup.start()
    def animationFinished(self):
        """
        Changes the animation state
        Changes the extended state

        :return: None
        """
        self.changeAnimatingFalse()
        self.navBar.changeExtended()

    def changeAnimatingFalse(self):
        """
        Changes the state of animating

        :return:
        """
        self.animating = False

    def stopAnimations(self):
        """
        Stops all animations

        :return: None
        """
        try:
            self.closeNavBarAnimationGroup.stop()
        except AttributeError as e:
            print(e)

        try:
            self.openNavBarAnimationGroup.stop()
        except AttributeError as e:
            print(e)

    def changeAnimate(self):
        """
        Changes the animating state

        :return: None
        """
        self.animating = not self.animating

    def extendNavBar(self):
        """
        Moves the nav bar to fully extend

        :return: None

        """
        self.navBar.move(QPoint(0, 0))
        self.navBar.header.moveButtonExtended()

    def collapseNavBar(self):
        """
        Moves the nav bar through to a negative point to give the feeling of the nav bar closing

        """
        self.navBar.move(QPoint(-144, 0))
        self.navBar.header.moveButtonCollapsed()

    def collapseNavbarAnimate(self):
        self.navBarPosAnimation.setEndValue(QPoint(-144, 0))
        self.navBarPosAnimation.setDuration(self.animationTime)

        self.navbarHamburgerButtonAnimation.setEndValue(QPoint(144, 0))
        self.navbarHamburgerButtonAnimation.setDuration(self.animationTime)

    def enlargeContentWidgetAnimate(self):
        """
        Enlarges the content widget

        :return: None
        """
        RESIZEWIDTH = self.width() - 56

        self.contentSizeAnimation.setEndValue(QSize(RESIZEWIDTH, self.height()))
        self.contentSizeAnimation.setDuration(self.animationTime)

        self.contentPosAnimation.setEndValue(QPoint(56, 0))
        self.contentPosAnimation.setDuration(self.animationTime)

    def shrinkContentWidgetAnimate(self):
        """
        shrinks the content widget

        :return:
        """
        RESIZEWIDTH = self.width() - self.navBar.width()

        self.contentSizeAnimation.setEndValue(QSize(RESIZEWIDTH, self.height()))
        self.contentSizeAnimation.setDuration(self.animationTime)

        self.contentPosAnimation.setEndValue(QPoint(200, 0))
        self.contentPosAnimation.setDuration(self.animationTime)

    def enlargeNavBarAnimate(self):
        """
        Enlarges the nav bar

        :return: None
        """
        self.navBarPosAnimation.setEndValue(QPoint(0, 0))
        self.navBarPosAnimation.setDuration(self.animationTime)

        self.navbarHamburgerButtonAnimation.setEndValue(QPoint(0, 0))
        self.navbarHamburgerButtonAnimation.setDuration(self.animationTime)

    def shrinkContentWidget(self):
        """
        Shrinks the content of the display

        """
        RESIZEWIDTH = self.width() - self.navBar.width()

        self.windowPages.resize(QSize(RESIZEWIDTH, self.height()))
        self.windowPages.move(QPoint(200, 0))

    def enlargeContentWidget(self):
        """
        Resizes the content widget and repositions it

        """

        RESIZEWIDTH = self.width() - 56
        self.windowPages.resize(QSize(RESIZEWIDTH, self.height()))
        self.windowPages.move(QPoint(56, 0))


if __name__ == '__main__':
    app = QApplication()
    display = MainWindow()
    display.show()

    app.exec()
