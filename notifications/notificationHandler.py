from notifications.notification import *
from datetime import datetime
from plyer import notification as n
from PySide6.QtCore import QRunnable, Slot, QThreadPool
from resourceManager.internalDataHandler import *


class NotificationHandler:
    def __init__(self):
        self.notifications = []
        self.running = True

    def addNotification(self, title: str, message: str, year: int, month: int, day: int, hour: int, minute: int):
        """
        Creates a notification class and appends it to the end of the list

        :param title: str
        :param message: str
        :param year: int
        :param month: int
        :param day: int
        :param hour: int
        :param minute: int
        :return: None
        """

        notification = Notification(title, message, year, month, day, hour, minute)
        self.notifications.append(notification)

    def startLoop(self):
        """
        Loops through all of the notifications, and sends them when needed

        :return: None
        """
        while self.running:
            for notification in self.notifications:
                if notification.notificationTime > datetime.now():
                    self.sendNotification(notification)
                    self.removeNotification(notification)

    def removeNotification(self, notification: Notification):
        """
        Removes a notification from the notification variables

        :param notification: Notification
        :return: None
        """

        index = self.notifications.index(notification)
        self.notifications.pop(index)

    def sendNotification(self, userNotification: Notification):
        """
        Sends out and notifies the user's window

        :param userNotification: Notification
        :return: None
        """
        appName = "Organisation App"
        toast = False

        title = userNotification.title
        message = userNotification.message

        try:
            appIcon = getProjectDirPath() + "resources\\icons\\appIcon.png"

            n.notify(title=title, message=message, app_name=appName, app_icon=appIcon, toast=toast)
        except Exception:
            n.notify(title=title, message=message, app_name=appName, toast=toast)


class NotificationWorker(QRunnable):
    """
    Worker Thread

    Copied and modified from:
    https://www.mfitzp.com/multithreading-pyside-applications-qthreadpool/
    """

    def __init__(self, notificationHandler: NotificationHandler):
        super(NotificationWorker, self).__init__()
        self.notificationHandler = notificationHandler

    @Slot()
    def run(self):
        self.notificationHandler.startLoop()


if __name__ == '__main__':
    appIcon = getProjectDirPath() + "resources\\icons\\appIcon.ico"

    n.notify(title="This is the title", app_name="Organiser", message="This is a message",
             app_icon=appIcon)
