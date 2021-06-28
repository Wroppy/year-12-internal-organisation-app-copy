"""
Will not be used for the digi internal

"""

from notifications.notification import *
from datetime import datetime
from pynotifier import Notification
from PySide6.QtCore import QRunnable, Slot, QThreadPool
from resourceManager.internalDataHandler import *
from display.eventsWidget.event import Event
from resourceManager.resourceHandler import ResourceHandler
import resourceManager.resources


class NotificationHandler:
    def __init__(self, resourceHandler: ResourceHandler):
        self.resourceHandler = resourceHandler

        self.notifications = self.resourceHandler.returnNotifyEvents()
        self.running = True

    def addNotification(self, event: Event):
        """
        Creates a notification and appends it to the end of the list

        :param event: Event
        :return: None
        """

        self.notifications.append(event)

    def startLoop(self):
        """
        Loops through all of the notifications, and sends them when needed

        :return: None
        """

        print("stareting loop")
        while self.running:
            for event in self.notifications:
                print(event.notifyTime)
                if event.notifyTime <= datetime.now():
                    print(2)
                    self.sendNotification(event)
                    self.removeNotification(event)
                    break
    def removeNotification(self, notification: Event):
        """
        Removes a notification from the notification variables

        :param notification: Notification
        :return: None
        """

        index = self.notifications.index(notification)
        self.notifications.pop(index)

    def removeNotificationFromFile(self, event: Event):
        self.resourceHandler.changeEventNotified(event.eventKeyCode)

    def sendNotification(self, userNotification: Event):
        """
        Sends out and notifies the user's window

        :param userNotification: Event
        :return: None
        """
        print("Notifying")
        appName = "Organisation App"
        toast = False

        title = userNotification.eventName
        try:
            appIcon = getProjectDirPath() + "resources\\icons\\diary.ico"

            # Sends the notification through
            Notification(
                title=title,
                description="From Weyman's Organiser App",
                icon_path=appIcon,
                duration=5,
                urgency="normal"
            ).send()
            print("Sent")
        except Exception as e:
            print(e)
            print("error")


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
    notify = NotificationHandler(ResourceHandler())
    notify.startLoop()

