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

        # Sets the completed button to the assignments state
        self.completedButton.setChecked(assignment.completed)

        self.completedButton.setLayoutDirection(Qt.RightToLeft)
        layout.addWidget(self.completedButton)


if __name__ == '__main__':
    app = QApplication()
    display = AssignmentWidget(Assignment("Title", False))
    display.show()
    app.exec()



