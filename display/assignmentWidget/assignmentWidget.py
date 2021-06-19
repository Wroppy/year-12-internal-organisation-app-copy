from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from display.assignmentWidget.assignment import Assignment


class AssignmentWidget(QWidget):
    def __init__(self, assignment: Assignment):
        super(AssignmentWidget, self).__init__()
        layout = QHBoxLayout(self)

        # Creates a radio button for thw widget
        self.selectButton = QRadioButton()
        layout.addWidget(self.selectButton)

        # Creates a label on the left for the title
        label = QLabel(assignment.title)
        layout.addWidget(label)

        layout.addStretch()

        # Creates a radio button for the right of the screen
        self.completedButton = QCheckBox("Completed")

        # Disables the button if the assignment/event has been com
        if assignment.completed:
            self.completedButton.setChecked(True)
            self.completedButton.setDisabled(True)

        self.completedButton.setLayoutDirection(Qt.RightToLeft)
        layout.addWidget(self.completedButton)


if __name__ == '__main__':
    app = QApplication()
    display = AssignmentWidget(Assignment("Title", False))
    display.show()
    app.exec()



