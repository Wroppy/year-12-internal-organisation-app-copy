"""
This class is made to be subclassed for different widgets in order to stop repetitive code in the project

"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *


class widgetTemplate(QWidget):
    def __init__(self, layout: QBoxLayout):
        super(QWidget, self).__init__()

        self.layout = layout(self)

        self.createWidgets()

    def setPresets(self):
        """
        Sets the presets for the window

        :return: None
        """

    def createWidgets(self):
        """
        Creates the widgets for the widget

        :return: None
        """

    def