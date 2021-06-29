from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from resourceManager.internalDataHandler import loadJsonFile
from display.eventsWidget.eventHeader import Header



class QuickLinksPage(QWidget):
    def __init__(self):
        super(QuickLinksPage, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)

        # Creates a header for the daily notices
        header = Header("Quick Links")
        HEADERNAME = "header"
        header.setObjectName(HEADERNAME)
        layout.addWidget(header)

        # Creates links for the widget page
        LINKS = [
            "https://www.scotscollege.school.nz/daily-notices/",
            "https://www.scotscollege.school.nz/about-us/college-communications/handbooks/",
            "https://scotscollegenz.sharepoint.com/SitePages/Home.aspx",
            "https://spider.scotscollege.school.nz/Spider2011/Pages/Login"
        ]

        LINKSDISPLAY = [
            "Scots College Daily Notices",
            "Scots College Handbooks",
            "Scot E Portal",
            "PC School Spider"
        ]

        LINKNAME = "link"

        COLOURS = loadJsonFile("settings\\colours")
        KEY = "linkColour"

        # Loops through each link and creates a label of it
        for i in range(len(LINKS)):
            linkLabel = QLabel(
                f"<a href=\"{LINKS[i]}\" style=\"text-decoration:none; color: rgb{tuple(COLOURS[KEY])};; \">{LINKSDISPLAY[i]}</a>")
            linkLabel.setObjectName(LINKNAME)
            linkLabel.setOpenExternalLinks(True)
            layout.addWidget(linkLabel)

        layout.addStretch()

        self.styleWidgets()

    def styleWidgets(self):
        """
        Styles widgets

        :return: None
        """

        STYLE = f"""
            QLabel#header{{
                font-size: 18px;
                margin: 0px;
                margin-bottom: 20px;
            }}
            
            QLabel#link{{
                font-size: 14px;

                
            }}
        """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication()
    display = QuickLinksPage()
    display.show()

    app.exec()
