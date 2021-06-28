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
        """

        self.eventDisplay.addWidget(eventTitle, notifyTime, eventKey)

    def showEventDialog(self, errorCode: Union[str, None]):
        """
        Is displayed when the user decides to add a new event

        """

        dialog = AddEventDialog(self, errorCode)
        if dialog.exec():
            # If there is no input, and the user pressed "ok" then then it will display the window again
            if len(dialog.eventEntry.text()) == 0:
                self.showEventDialog("Please Input An Event")
                return

            # Checks if the event is made up of only digits
            if dialog.eventEntry.text().isdigit():
                self.showNewClassDialog("Please Input An Event")
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
                self.showEventDialog("Please Input A Valid Time")
                return

            eventTitle = dialog.eventEntry.text()

            eventKey = self.resourceManager.generateKeyCode()

            # Adds the event to the page
            self.addEvent(eventTitle, notifyTime, eventKey)

            self.resourceManager.addEventToFile(eventTitle, notifyTime, eventKey)

            # Adds the event to the notification manager
            self.notificationManger.addNotification(Event(eventTitle, notifyTime, eventKey))

    def addButtonFunction(self):
        """
        Adds functionality to the buttons

        """
        self.buttonWidget.addButton.clicked.connect(lambda: self.showEventDialog(None))
        self.buttonWidget.deleteButton.clicked.connect(self.deleteEventDialog)


if __name__ == '__main__':
    app = QApplication()

    display = EventPage(None)
    display.show()
    app.exec()
