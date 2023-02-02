from .element import *
from .answers import *
from .figure import *

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
    self._figures = []


  @property
  def text(self):
    return self._text

  @text.setter
  def text(self,val):
    self._text = self._lint(val)

  @property
  def formatted_text(self):
    return self._formatter.fmt( self._text, **self.NS.__dict__ )

  @property
  def answer(self):
    return self._answer

  @answer.setter
  def answer(self,val):
    self._answer = val



  @contextlib.contextmanager
  def add_question(self,q=None):
    if q is None:
      q = Question()

    q.meta.parent_uuid = self._uuid
    if self.meta.has('ancestor_uuids'):
      q.meta.ancestor_uuids = [ u for u in self.meta.ancestor_uuids ] # need a copy
    else:
      q.meta.ancestor_uuids = list()
    q.meta.ancestor_uuids.append(self._uuid)

    self._questions.append(q)
    self._questions[-1].NS.__dict__.update( self.NS.__dict__ )
    yield self._questions[-1]

  @contextlib.contextmanager
  def add_part(self,p=None):
    if p is None:
      p = Question()

    p.meta.parent_uuid = self._uuid
    if self.meta.has('ancestor_uuids'):
      p.meta.ancestor_uuids = [ u for u in self.meta.ancestor_uuids ]
    else:
      p.meta.ancestor_uuids = list()
    p.meta.ancestor_uuids.append(self._uuid)

    self._parts.append(p)
    self._parts[-1].NS.__dict__.update( self.NS.__dict__ )
    yield self._parts[-1]

  @contextlib.contextmanager
  def add_answer(self,a):
    if inspect.isclass(a):
      a = a()

    a.meta.parent_uuid = self._uuid
    if self.meta.has('ancestor_uuids'):
      a.meta.ancestor_uuids = [ u for u in self.meta.ancestor_uuids ]
    else:
      a.meta.ancestor_uuids = list()
    a.meta.ancestor_uuids.append(self._uuid)

    self._answer = a
    self._answer.NS.__dict__.update( self.NS.__dict__ )
    yield self._answer

  @contextlib.contextmanager
  def add_figure(self,f=None):
    if f is None:
      f = Figure()

    self._figures.append(f)

    yield self._figures[-1]

