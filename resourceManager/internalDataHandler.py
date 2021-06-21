"""
This file handles all of the internal json files
The icons and images will be handled by a .qrc file

"""

import pathlib
from typing import *
import json


def getProjectDirPath() -> str:
    """
    Returns the absolute file path of the resources folder by looping
    through characters until the app folder is found.
    This is done because the absolute path will be different depending on where the function is called from

    :return: str
    """
    try:
        appFolderName = "year_12_organisation_app"
        absolutePath = str(pathlib.Path().absolute())
        for i in range(0, len(absolutePath)):
            # folderName = year_12_organisation_app
            # Slices the absolute path
            folderName = absolutePath[i: i + len(appFolderName)]
            if folderName == appFolderName:
                # returns C:\Users\Weyman\PycharmProjects\year_12_organisation_app\
                return absolutePath[0: i + len(appFolderName)] + "\\"
        raise Exception
    except Exception:
        print("File path does not exist")
        print("Check if it exists")

        return ""


def createFile(path: str):
    """
    Creates a json file given its path

    :param path: str
    :return: None
    """
    with open(path, "w") as file:
        json.dump({}, file)


def loadJsonFile(fileName: str) -> dict:
    """
    Returns a json file's data given the file's name

    :param fileName: str
    :return: dict[Any]
    """

    prefix = ".json"
    projectPath = "resources\\"
    path = getProjectDirPath() + projectPath + fileName + prefix

    try:
        with open(path, "r") as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        """
        When an exception occurs it means the file does not exist, but the path does
        """

        print("File does not exist")
        print("Writing a new file in that location")
        createFile(path)
    except ValueError:
        """
        When there is a problem decoding the json file
        """

        print("There was an error decoding the json file")

        createFile(path)


def writeJsonFile(fileName: str, data: Dict[Any, Any]):
    """
    Writes the a json file given the filename and the data

    :param fileName: str
    :param data: Dict[Any: Any]
    :return: None
    """
    prefix = ".json"
    projectPath = "resources\\"
    path = getProjectDirPath() + projectPath + fileName + prefix

    with open(path, "w") as file:
        json.dump(data, file)


class InternalDataBaseManager:
    def getAccountKey(self) -> Union[str, None]:
        """
        Loads the account key from the file

        :return: Union[str, None]
        """
        accountDetails = loadJsonFile("data\\account")
        userKeyCode = accountDetails["accountKey"]
        return userKeyCode

    def addAccount(self, accountKey: int):
        """
        Adds an account to the file

        :param accountKey: int
        :return: None
        """
        data = {"accountKey": accountKey}
        writeJsonFile("data\\account", data)


if __name__ == '__main__':
    print(loadJsonFile("assignments"))
