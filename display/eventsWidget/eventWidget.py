"""
This class displays the Event classes attributes to the user

"""
import datetime
from display.eventsWidget.event import Event
from PySide6.QtWidgets import *
from display.generalInfoDisplay import InfoDisplay


class EventWidget(InfoDisplay):
    def __init__(self, event: Event):
        self._event = event
        super(EventWidget, self).__init__()

    def createLeftSideWidgets(self):
        titleLabel = QLabel(self._event.eventName)
        self.layout.addWidget(titleLabel)

    def createRightSideWidgets(self):
        notifyTime = self._event.formatTime()
        notifyLabel = QLabel(f"Reminder: {notifyTime}")
        self.layout.addWidget(notifyLabel)


if __name__ == '__main__':
    event = Event("Test 1", datetime.datetime.now(), "aw")

    app = QApplication()
    display = EventWidget(event)
    display.show()
    app.exec()
