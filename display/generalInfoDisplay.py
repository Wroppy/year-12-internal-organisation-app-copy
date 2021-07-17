"""
This file contains widgets that the events, assignments, and the classes

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
from datetime import time
import sys
from typing import *
from abc import abstractmethod



class InfoDisplay(QWidget):
    def __init__(self ):
        super().__init__(None)
        self.layout = QHBoxLayout(self)

        self.selectButton = QRadioButton()
        self.layout.addWidget(self.selectButton)

        self.createLeftSideWidgets()
        self.layout.addStretch()
        self.createRightSideWidgets()

    @ abstractmethod
    def createLeftSideWidgets(self):
        """
        Creates widgets for the left side of the display

        """

    @ abstractmethod
    def createRightSideWidgets(self):
        """
        Creates widgets for the right side of the display

        """