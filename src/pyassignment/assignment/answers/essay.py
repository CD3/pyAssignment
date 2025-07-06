from .answer_base import *
from .text import *


class Essay(Text):
    def __init__(self):
        super().__init__()

    @property
    def example(self):
        return super().text

    @example.setter
    def example(self, val):
        super().text = val
