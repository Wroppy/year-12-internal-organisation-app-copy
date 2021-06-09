from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.widgetTemplate import WidgetTemplate

class NavBar(WidgetTemplate):
    def __init__(self):
        super(NavBar, self).__init__(QVBoxLayout)

    