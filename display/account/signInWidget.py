from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6 import QtWidgets
from PySide6.QtGui import *
from PySide6 import QtCore
import sys
from resourceManager.internalDataHandler import loadJsonFile
from typing import *


class SignIn(QWidget):
    def __init__(self):
        super(SignIn, self).__init__()

        self.createWidgets()

        self.styleWidget()

    def createWidgets(self):
        """
        Creates widgets that will be nested inside of the sign in widget

        :return: None
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 11, 60, 11)
        layout.addSpacing(10)

        self.headerLabel = QLabel("Sign In")
        headerWidget = self.createHorizontalCenterWidget(self.headerLabel)
        layout.addWidget(headerWidget)

        # Creates the headings for the text fields
        usernameHeading = QLabel("Username:")
        passwordHeading = QLabel("Password:")

        # Creates the text fields for signing in
        self.usernameEntry = QLineEdit()
        self.passwordEntry = QLineEdit()

        usernameWidget = self.createHorizontalWidget(usernameHeading, self.usernameEntry)
        passwordWidget = self.createHorizontalWidget(passwordHeading, self.passwordEntry)

        layout.addWidget(usernameWidget)
        layout.addWidget(passwordWidget)

        # Creates the button for signing in
        self.processButton = QPushButton("Log In")
        self.processButton.setObjectName("signInButton")

        # This places the button to the right of the display
        buttonWidget = QWidget()
        buttonWidgetLayout = QHBoxLayout(buttonWidget)
        buttonWidgetLayout.addStretch()

        buttonWidgetLayout.addWidget(self.processButton)

        layout.addWidget(buttonWidget)

        # Creates an error message label if these is an error with the sign in
        self.errorLabel = QLabel()
        errorWidget = self.createHorizontalCenterWidget(self.errorLabel)

        layout.addWidget(errorWidget)

        self.createSignUpButton(layout)

        layout.addStretch()

    def createSignUpButton(self, layout: Union[QVBoxLayout, QHBoxLayout, QGridLayout]):
        """
        Creates the sign up button and adds it to the layout

        :param layout: Union[QVBoxLayout, QHBoxLayout, QGridLayout]
        """

        self.signUpButton = QPushButton("Dont have an account? Sign Up")
        layout.addWidget(self.signUpButton)

    def changeErrorText(self, text: str):
        self.errorLabel.setText(text)

    def createHorizontalWidget(self, *widgets) -> QWidget:
        """
        Given the widgets, creates a widget with those widgets aligned horizontally

        :param widgets: args -> list
        :return: QWidget
        """
        hWidget = QWidget()
        hLayout = QHBoxLayout(hWidget)
        for widget in widgets:
            hLayout.addWidget(widget)

        return hWidget

    def createHorizontalCenterWidget(self, *widgets) -> QWidget:
        """
        Givens the widgets

        :param widgets: args -> list
        :return: QWidget
        """
        horizontalWidget = QWidget()
        hLayout = QHBoxLayout(horizontalWidget)

        hLayout.addStretch()
        for widget in widgets:
            hLayout.addWidget(widget)

        hLayout.addStretch()

        return horizontalWidget

    def styleWidget(self):
        COLOURS = loadJsonFile("settings\\colours")
        STYLE = f"""
            QPushButton{{
                border: none;
                background-color: rgb{tuple(COLOURS["buttonColour"])};
                color: rgb{tuple(COLOURS["navBarTextColour"])};
                border-bottom: 1px solid rgb{tuple(COLOURS["navBarFrameColour"])};
                padding: 14px 30px;
            }}  
            
            QPushButton::hover{{
                background-color: rgb{tuple(COLOURS["buttonHoverColour"])};
            }}
            
            QPushButton#signInButton{{
                padding: 16px 60px;
            }}
        """

        self.setStyleSheet(STYLE)


if __name__ == '__main__':
    app = QApplication()
    display = SignIn()

    display.show()
    app.exec()
