import contextlib
from .Question import Question
from ..Utils import Namespace

class Assignment(object):
  def __init__(self):
    self._questions = []
    self._namespace = Namespace()

  @property
  def NS(self):
    return self._namespace

  @contextlib.contextmanager
  def add_question(self,q=None):
    if q is None:
      q = Question()
    self._questions.append(q)
    self._questions[-1].NS.__dict__.update( self.NS.__dict__ )
    yield self._questions[-1]

