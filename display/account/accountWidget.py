"""
Not Used in Internal


"""


from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from typing import *
from display.account import signInWidget, signUpWidget, userAccountWidget


class AccountWidget(QStackedWidget):
    def __init__(self):
        super(AccountWidget, self).__init__()

        # Initializes the widgets and adds it to the display
        self.signIn = signInWidget.SignIn()
        self.signUp = signUpWidget.SignUpWidget()

        self.addWidget(self.signIn)
        self.addWidget(self.signUp)
        self.addWidget(userAccountWidget.UserSigedInWidget())

        # Sets commands for the buttons
        self.signIn.signUpButton.clicked.connect(self.changeToSignUp)
        self.signUp.signUpButton.clicked.connect(self.changeToSignIn)

    def changeToSignUp(self):
        """
        Changes the page to the sign up page

        """
        self.setCurrentIndex(1)

    def changeToSignIn(self):
        """
        Changes the page to the sign in page

        """
        self.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication()
    display = AccountWidget()
    display.show()
    app.exec()
