import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
from typing import *
from display.eventsWidget.eventWidget import EventWidget
from resourceManager.resourceHandler import ResourceHandler
from display.eventsWidget.event import Event
import sys

class EventHolder(QWidget):
    def  __init__(self, events: List[Event], resourceManager: ResourceHandler):
        super(EventHolder, self).__init__()

        self.resourceManager = resourceManager

        self.eventWidgets = []
        self.events = events

        self.widgetLayout = QVBoxLayout(self)

        self.addEventsToLayout()

    def deleteItemsInLayout(self):
        """
        Deletes the items in the layout

        :return: None
        """

        if self.widgetLayout.count() > 1:
            # Deletes each widget in the layout one by one
            while self.widgetLayout.count():
                item = self.widgetLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    pass
        else:
            pass

    def addEventsToLayout(self):
        """
        Adds the assignments to the layout

        """

        # Deletes all old widgets and clears previous widgets as well
        self.deleteItemsInLayout()
        self.eventWidgets: List[Event] = []

        layout = self.layout()

        # Displays all of the assignments on the window
        for event in self.events:
            widget = EventWidget(event)
            layout.addWidget(widget)
            self.eventWidgets.append(widget)

        layout.addStretch()


    def appendEvent(self, event: Event):
        """
        Given the assignment, it adds it at the end of a list

        :param assignment: Assignment
        """
        self.events.append(event)

    def deleteEvent(self, index: int):
        """
        Given the index, deleted the assignment off the list

        :param index: int
        """
        self.events.pop(index)


if __name__ == '__main__':
    app = QApplication()

    display = EventHolder([Event("No", datetime.datetime.now()) for _ in range(10)], None)
    display.show()

    app.exec()
