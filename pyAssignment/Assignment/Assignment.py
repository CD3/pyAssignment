from .Element import *
from .Question import *
from .Answer import *
from .Figure import *

class Assignment(Element):
  def __init__(self):
    super().__init__()
    self._questions = []
    self._figures   = []


  @contextlib.contextmanager
  def add_question(self,q=None):
    if q is None:
      q = Question()
    self._questions.append(q)
    self._questions[-1].NS.__dict__.update( self.NS.__dict__ )
    yield self._questions[-1]

  @contextlib.contextmanager
  def add_figure(self,f=None):
    if f is None:
      f = Figure()
    self._figures.append(f)
    self._figures[-1].NS.__dict__.update( self.NS.__dict__ )
    yield self._figures[-1]
