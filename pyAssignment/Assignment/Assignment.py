from .Element import *
from .Question import *
from .Answer import *
from .Figure import *

class Assignment(Element):

  # an internal class to implement the
  # information interface
  # does it make sense to extract this so that
  # questions can have information?... yes
  class Information(object):
    def __init__(self):
      self._text = ""

    @property
    def text(self):
      return self._text

    @text.setter
    def text(self,val):
      self._text = val


  def __init__(self):
    super().__init__()
    self._questions = []
    self._information = []
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

  @contextlib.contextmanager
  def add_information(self,):
    pass
    # Need to:
    #
    # 1. Mark the location that the information should be inserted into the assignment
    #    by storing the current length of the _questions list.
    # 2. Create an Information object yeild it.
