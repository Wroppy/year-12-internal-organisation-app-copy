"""
This class displays the Event classes attributes to the user

"""
import datetime
from display.eventsWidget.event import Event
from PySide6.QtWidgets import *


class EventWidget(QWidget):
    def __init__(self, event: Event):
        super(EventWidget, self).__init__()
        layout = QHBoxLayout(self)

        # Creates the widgets
        self.selectButton = QRadioButton()

        titleLabel = QLabel(event.eventName)

        notifyTime = event.formatTime()
        notifyLabel = QLabel(f"Reminder: {notifyTime}")

        # Adds them to the layout
        layout.addWidget(self.selectButton)
        layout.addWidget(titleLabel)
        layout.addStretch()
        layout.addWidget(notifyLabel)


if __name__ == '__main__':
    event = Event("Test 1", datetime.datetime.now())

    app = QApplication()
    display = EventWidget(event)
    display.show()
    app.exec()
