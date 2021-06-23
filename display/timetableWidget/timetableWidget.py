"""
This class contains the entire timetable page, which includes the timetable display and the buttons

"""
import datetime

from PySide6.QtWidgets import *
from display.timetableWidget.timetableDisplay import TimetableDisplay
from display.timetableWidget.buttonWidget import ButtonWidget
from display.timetableWidget.addClassDialog import AddClassDialog
from display.confirmDialog import ConfirmDialog
from resourceManager.resourceHandler import ResourceHandler
from datetime import time


class TimetablePageWidget(QWidget):
    def __init__(self, resourceManger: ResourceHandler):
        super(TimetablePageWidget, self).__init__()

        self.resourceManager = resourceManger

        # Sets a layout and adds widgets to the page
        layout = QVBoxLayout(self)

        self.timetableWidget = TimetableDisplay(self.resourceManager)

        self.buttonWidget = ButtonWidget()

        layout.addWidget(self.timetableWidget)
        layout.addWidget(self.buttonWidget)

        self.connectButtons()

    def showNewClassDialog(self):
        """
        Displays a dialog window that asks the user for a class

        :return: None
        """
        dialog = AddClassDialog(self)
        if dialog.exec():
            # If there is no input, and the user pressed "ok" then then it will display the window again
            if len(dialog.classNameEntry.text()) == 0:
                self.showNewClassDialog()
            else:
                classTitle = dialog.classNameEntry.text()

                startingTime = time(dialog.startTimeHour.value(), dialog.startTimeMinute.value())
                endingTime = time(dialog.endTimeHour.value(), dialog.endTimeMinute.value())

                # Checks if the starting time is greater than the ending time
                if startingTime >= endingTime:
                    self.showNewClassDialog()
                    return

                currentTime = datetime.datetime.now()

                # Adds the class to the page
                self.addClass(classTitle, startingTime, endingTime, currentTime)

                currentDay = self.timetableWidget.daysSelection.currentIndex()
                self.resourceManager.addClassToFile(currentDay, classTitle, startingTime, endingTime, currentTime)



    def addClass(self, classTitle: str, startingTime: time, endingTime: time, currentTime: datetime.datetime):
        """
        Adds a class to a specific day

        :param classTitle: str
        :param startingTime: int
        :param endingTime: int
        :param currentTIme: datetime class
        :return: None
        """
        currentDay = self.timetableWidget.daysSelection.currentIndex()
        timetables = self.timetableWidget.timetables
        # Timetable -> Specific Day of Timetable -> Each individual class. addClass(:params)
        timetables[currentDay].addClass(classTitle, startingTime, endingTime, currentTime)


    def showDeleteDialog(self):
        """
        Checks if the user wants to delete the class in their timetable

        :return: None
        """
        currentDay = self.timetableWidget.daysSelection.currentIndex()
        timetables = self.timetableWidget.timetables

        # Accesses the radiobutton inside the class holder, inside of the timetable
        # Timetable -> Specific Day of Timetable -> Each individual class -> radio button
        for i in range(len(timetables[currentDay].classWidgets)):
            # for i in range(len(self.timetableWidget.timetables[self.timetableWidget.daysSelection.currentIndex()].classWidgets))
            if timetables[currentDay].classWidgets[i].selectButton.isChecked():

                dialog = ConfirmDialog("Are you sure you want to delete?")
                if dialog.exec():
                    timetables[currentDay].deleteClass(i)
                    currentTime = datetime.datetime.now()
                    self.resourceManager.deleteClassFromfile(currentDay, i, currentTime)
                break

    def connectButtons(self):
        """
        Gives the buttons functionality

        :return: None
        """
        self.buttonWidget.newButton.clicked.connect(self.showNewClassDialog)
        self.buttonWidget.deleteButton.clicked.connect(self.showDeleteDialog)


if __name__ == '__main__':
    app = QApplication()
    display = TimetablePageWidget()
    display.show()
    app.exec()
