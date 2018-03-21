from .Element import *
from .Answer import *

class Question(Element):
  """A class representing a question.

  A can question contain:
  
  - text : the actual question itself
  - answer : an answer to the question
  - parts : one or more parts to the questions (sub-questions). these are also questions.
  - questions : one or more questions about the question (i.e. a quiz that references a problem set question.)
  """

  def __init__(self, text=None):
    super().__init__()

    self._text = ""
    self._pre_text = ""
    self._post_text = ""
    self._parts     = []
    self._questions = []
    self._answer    = None


  @property
  def text(self):
    return self._text

  @text.setter
  def text(self,val):
    self._text = self._lint(val)

  @property
  def formatted_text(self):
    return self._formatter.fmt( self._text, **self.NS.__dict__ )




  @contextlib.contextmanager
  def add_question(self,q=None):
    if q is None:
      q = Question()
    self._questions.append(q)
    self._questions[-1].NS.__dict__.update( self.NS.__dict__ )
    yield self._questions[-1]

  @contextlib.contextmanager
  def add_part(self,p=None):
    if p is None:
      p = Question()
    self._parts.append(p)
    self._parts[-1].NS.__dict__.update( self.NS.__dict__ )
    yield self._parts[-1]

  @contextlib.contextmanager
  def add_answer(self,a=None):
    if a is None:
      a = Answer
    if inspect.isclass(a):
      a = a()
    self._answer = a
    self._answer.NS.__dict__.update( self.NS.__dict__ )
    yield self._answer

