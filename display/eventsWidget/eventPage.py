import datetime

from PySide6.QtWidgets import *

from display.eventsWidget.eventDisplay import EventsDisplay
from display.contentButtonWidget import ContentButtonWidget
from display.eventsWidget.addEventDialog import AddEventDialog
from display.confirmDialog import ConfirmDialog
from resourceManager.resourceHandler import ResourceHandler


class EventPage(QWidget):
    def __init__(self, resourceManager: ResourceHandler):
        super(EventPage, self).__init__()

        self.resourceManager = resourceManager

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
        # Accesses the radiobutton inside the assignment holder
        # Assignment holder -> All assignments -> Each assignment -> radio button
        for i in range(len(self.eventDisplay.eventHolder.events)):
            # for i in range(len(self.timetableWidget.timetables[self.timetableWidget.daysSelection.currentIndex()].classWidgets))
            if self.eventDisplay.eventHolder.eventWidgets[i].selectButton.isChecked():
                dialog = ConfirmDialog("Are you sure you want to delete?")
                if dialog.exec():
                    self.eventDisplay.eventHolder.deleteEvent(i)
                    self.eventDisplay.eventHolder.addEventsToLayout()

                    # assignmentKeyCode = self.eventDisplay.returnAssignmentKeyCode
                    # self.resourceManager.deleteAssignment(assignmentKeyCode)
                break

    def addEvent(self, eventTitle: str, notifyTime: datetime.datetime, eventKey: str):
        """
        Adds an assignment to the display

        :param assignmentTitle: str
        :param assignmentKey: str

        """

        self.eventDisplay.addWidget(eventTitle, notifyTime, eventKey)

    def showEventDialog(self):
        """
        Is displayed when the user decides to open add a new assignment

        """

        dialog = AddEventDialog(self)
        if dialog.exec():
            # If there is no input, and the user pressed "ok" then then it will display the window again
            if len(dialog.assignmentEntry.text()) == 0:
                self.showEventDialog()
            else:
                assignmentTitle = dialog.assignmentEntry.text()

                #assignmentKey = self.resourceManager.generateKeyCode()
                assignmentKey = "2"
                # Adds the assignment to the page
                self.addEvent(assignmentTitle, datetime.datetime.now(), assignmentKey)
                #self.resourceManager.addAssignment(assignmentTitle, False, assignmentKey)

    def addButtonFunction(self):
        """
        Adds functionality to the buttons

        """
        self.buttonWidget.addButton.clicked.connect(self.showEventDialog)
        self.buttonWidget.deleteButton.clicked.connect(self.deleteEventDialog)


if __name__ == '__main__':
    app = QApplication()

    display = EventPage(None)
    display.show()
    app.exec()