"""
This file defines the assignment class
"""


class Assignment:
    def __init__(self, title: str, completed: bool, assignmentKeyCode: str):
        self.title = title
        self.completed = completed
        self.assignmentKeyCode = assignmentKeyCode

