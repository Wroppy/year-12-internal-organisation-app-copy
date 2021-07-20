import datetime

from PySide6.QtWidgets import *

from display.eventsWidget.eventDisplay import EventsDisplay
from display.contentButtonWidget import ContentButtonWidget
from display.eventsWidget.addEventDialog import AddEventDialog
from display.confirmDialog import ConfirmDialog
from resourceManager.resourceHandler import ResourceHandler
from notifications.notificationHandler import NotificationHandler
from typing import *
from display.eventsWidget.event import Event


class EventPage(QWidget):
    def __init__(self, resourceManager: ResourceHandler, notificationHandler: NotificationHandler):
        super(EventPage, self).__init__()

        self.resourceManager = resourceManager
        self.notificationManger = notificationHandler

        layout = QVBoxLayout(self)

        # Adds widgets to the page
        self.eventDisplay = EventsDisplay(self.resourceManager)
        layout.addWidget(self.eventDisplay)

        self.buttonWidget = ContentButtonWidget("Add Event", "Delete Event")
        layout.addWidget(self.buttonWidget)

        self.addButtonFunction()

    def deleteEventDialog(self):
        """
        Asks the user if they want to delete an event or not

        :return: None
        """
        # Accesses the radiobutton inside the event holder
        # Event holder -> All events -> Each event -> radio button
        for i in range(len(self.eventDisplay.eventHolder.events)):
            if self.eventDisplay.eventHolder.eventWidgets[i].selectButton.isChecked():
                dialog = ConfirmDialog("Are you sure you want to delete?")
                if dialog.exec():
                    eventKeyCode = self.eventDisplay.returnEventKeyCode(i)
                    self.notificationManger.removeNotification(self.eventDisplay.eventHolder.events[i])
                    self.eventDisplay.eventHolder.deleteEvent(i)
                    self.eventDisplay.eventHolder.addEventsToLayout()

                    self.resourceManager.deleteEvent(eventKeyCode)

                break

    def addEvent(self, eventTitle: str, notifyTime: datetime.datetime, eventKey: str):
        """
        Adds an event to the display

        :param eventTitle: str
        :param notifyTime: datetime
        :param eventKey: str
        :return: None
        """

        self.eventDisplay.addWidget(eventTitle, notifyTime, eventKey)

    def showEventDialog(self, errorCode: Union[str, None], eventName: Union[str, None]):
        """
        Is displayed when the user decides to add a new event

        :param errorCode: str or None
        :param eventName: str or None
        :return: None
        """

        dialog = AddEventDialog(self, errorCode, eventName)
        if dialog.exec():
            eventName = dialog.eventEntry.text()

            # If there is no input, and the user pressed "ok" then then it will display the window again
            if len(eventName) == 0:
                self.showEventDialog("Please Input An Event", None)
                return

            # Checks if the event is made up of only digits
            if eventName.isdigit():
                self.showNewClassDialog("Please Input Some Characters", eventName)
                return

            # If there is an error with the time, then the dialog will reappear
            try:
                year = dialog.dateYear.value()
                month = dialog.dateMonth.value()
                day = dialog.dateDay.value()

                hour = dialog.notifyTimeHour.value()
                minute = dialog.notifyTimeMinute.value()

                notifyTime = datetime.datetime(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute
                )

                # Checks if the time has already passed
                if notifyTime <= datetime.datetime.now():
                    raise Exception
            except Exception:
                self.showEventDialog("Please Input A Valid Time", eventName)
                return

            eventKey = self.resourceManager.generateKeyCode()

            # Adds the event to the json file
            self.resourceManager.addEvent(eventName, notifyTime, eventKey)

            # Adds the event to the page
            self.addEvent(eventName, notifyTime, eventKey)

            # Adds the event to the notification manager
            self.notificationManger.addNotification(Event(eventName, notifyTime, eventKey))

    def addButtonFunction(self):
        """
        Adds functionality to the buttons

        :return: None
        """
        self.buttonWidget.addButton.clicked.connect(lambda: self.showEventDialog(None, None))
        self.buttonWidget.deleteButton.clicked.connect(self.deleteEventDialog)


if __name__ == '__main__':
    app = QApplication()

    display = EventPage(None)
    display.show()
    app.exec()
