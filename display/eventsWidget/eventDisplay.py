"""
This file contains the events holder and the header

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from display.eventsWidget.event import Event
from display.eventsWidget.eventHolder import EventHolder
from display.assignmentWidget.assignmentHeaders import Header
from resourceManager.resourceHandler import ResourceHandler
import datetime


class EventsDisplay(QWidget):

    def __init__(self, resourceManager: ResourceHandler):
        super(EventsDisplay, self).__init__()

        self.resourceManager = resourceManager
        layout = QVBoxLayout(self)
        layout.setSpacing(0)

        # Creates the header
        header = Header("Events")
        layout.addWidget(header)

        #events = [Event(f"Test {i}", datetime.datetime.now(), "1") for i in range(5)]

        events = self.resourceManager.returnEvents()
        # Creates the widget holder
        self.eventHolder = EventHolder(events, self.resourceManager)

        # Creates the scroll bar for the event display
        scrollbar = QScrollArea()
        scrollbar.setWidget(self.eventHolder)
        scrollbar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollbar.setWidgetResizable(True)
        scrollbar.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        layout.addWidget(scrollbar)

        self.styleWidgets()

    def returnEventKeyCode(self, index: int):
        return self.eventHolder.events[index].eventKeyCode

    def addWidget(self, title: str, notifyTime: datetime.datetime, keyCode: str):
        """
        Adds an event given the title and its notify time

        :param title: str
        :param notifyTime: datetime
        :param keyCode: str
        """
        event = Event(title, notifyTime, keyCode)
        self.eventHolder.appendEvent(event)

        self.eventHolder.addEventsToLayout()

    def styleWidgets(self):
        """
        Styles the widgets nested

        """
        STYLE = f"""
            QScrollArea{{
                border: none;
            }}
        """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication()
    display = EventsDisplay(None)
    display.show()
    app.exec()
