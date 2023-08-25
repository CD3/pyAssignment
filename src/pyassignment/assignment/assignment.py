import inspect

from .answers import *
from .element import *
from .figure import *
from .information import *
from .question import *


class Assignment(Element):
    def __init__(self):
        super().__init__()
        self._questions = []
        self._information = {}
        self._figures = []


    @contextlib.contextmanager
    def add_question(self, q=None):
        if q is None:
            q = Question()

        # store the file and line number where the question was created.
        # this will be useful for diagnostics
        caller_frame = inspect.stack()[2]
        q.meta.filename = caller_frame.filename
        q.meta.lineno = caller_frame.lineno

        self._questions.append(q)
        self._questions[-1].NS.__dict__.update(self.NS.__dict__)
        yield self._questions[-1]

    @contextlib.contextmanager
    def add_figure(self, f=None):
        if f is None:
            f = Figure()
        self._figures.append(f)
        self._figures[-1].NS.__dict__.update(self.NS.__dict__)
        yield self._figures[-1]

    @contextlib.contextmanager
    def add_information(self):
        # Need to:
        #
        # 1. Mark the location that the information should be inserted into the assignment
        #    by storing the current length of the _questions list.
        # 2. Create an Information object yeild it.

        pos = len(self._questions)
        if pos not in self._information:
            self._information[pos] = Information()
        self._information[pos].NS.__dict__.update(self.NS.__dict__)
        yield self._information[pos]

    def update(self, ass):
        """Add questions, figures, and instructions from another assignment to this assignment."""

        old_n = len(self._questions)
        self._questions += ass._questions
        self._figures += ass._figures
        for i in ass._information:
            self._information[old_n + i] = ass._information[i]
