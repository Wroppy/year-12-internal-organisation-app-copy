from resourceManager.internalDataHandler import *
from resourceManager.databaseHandler import *
from display.timetableWidget.classClass import Class


class ResourceHandler:
    def __init__(self):
        dataBaseHandler = CloudDataBase()

    def returnClasses(self):
        """
        Returns the classes from the internal database

        :return:
        """

        data = loadJsonFile("data\\timetable")
        timetable = data["classes"]

        newTimetable = []
        for day in timetable:
            timetableDay = []
            for _class in day:
                _classObj = Class(_class["className"], _class["startingTime"], _class["endingTime"])
                timetableDay.append(_classObj)
            newTimetable.append(timetableDay)
        return newTimetable

    def deleteClassFromfile(self, day: int, index: int):
        timetable = loadJsonFile("data\\timetable")

        timetable["classes"][day].pop(index)

        writeJsonFile("data\\timetable", timetable)

    def addClassToFile(self, day: int, className: int, startingTime: int, endingTime: int):
        timetable = loadJsonFile("data\\timetable")

        print(timetable)

        _class = {
            "className": className,
            "startingTime": startingTime,
            "endingTime": endingTime
            }

        timetable["classes"][day].append(_class)

        writeJsonFile("data\\timetable", timetable)
if __name__ == '__main__':
    r = ResourceHandler()
    r.returnClasses()
