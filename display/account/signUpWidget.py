from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.account.signInWidget import SignIn


class SignUpWidget(SignIn):
    """
    Inherits from the Sign in widget, and just sets the text of the buttons differently


    """

    def __init__(self):
        super(SignUpWidget, self).__init__()
        TEXT = "Sign Up"
        self.processButton.setText(TEXT)
        self.headerLabel.setText(TEXT)
        self.signUpButton.setText("Already Have an Account? Sign In")
