"""
This file defines the assignment class
"""

from dataclasses import dataclass


@dataclass()
class Assignment:
    title: str
    completed: bool
    keyCode: str


