from .Element import *
from ..Utils import collection


class AnswerBase(Element):
  def __init__(self):
    super().__init__()

class Numerical(AnswerBase):
  def __init__(self):
    super().__init__()
    self._quantity = None

  @property
  def quantity(self):
    # if quantity is callable, call it and return
    if hasattr(self._quantity,'__call__'):
      return self._namespace.call( self._quantity)

    return self._quantity

  @quantity.setter
  def quantity(self,quant):
    self._quantity = quant

class MultipleChoice(AnswerBase):

  def __init__(self):
    super().__init__()
    self._choices = collection()
    self._correct = collection()

  @property
  def choices(self):
    return self._choices

  @choices.setter
  def choices(self,val):
    self._choices = collection()
    self._choices += val

  @choices.setter
  def incorrect(self,val):
    self.choices = val

  @choices.setter
  def correct(self,val):
    self.choices = val
    self.add_correct(self._choices[-1])

  @property
  def all_formatted_choices(self):
    for i in range(len(self._choices)):
      c = self._choices[i]
      yield self._formatter.fmt( c, **self.NS.__dict__ )

  @property
  def correct_formatted_choices(self):
    for i in self._correct:
      c = self._choices[i]
      yield self._formatter.fmt( c, **self.NS.__dict__ )

  @property
  def incorrect_formatted_choices(self):
    for i in range(len(self._choices)):
      if i not in self._correct:
        c = self._choices[i]
        yield self._formatter.fmt( c, **self.NS.__dict__ )



  def set_correct( self, i = None ):
    self._correct = collection()
    self.add_correct(i)

  def add_correct( self, i = None ):
    if i is None:
      i = len(self._choices)
    if isinstance( i, str ):
      i = self._choices.find(i)
    if i >= 0 and i < len(self._choices):
      self._correct.append( i )

class Text(AnswerBase):
  def __init__(self):
    super().__init__()
    self._text = None

    self._lint_flag = True
    self.disable_linter = set_state_context(self, {'_lint_flag':False})

  def _lint(self,text):
    if not self._lint_flag:
      return text

    return textwrap.dedent(text)

  @property
  def text(self):
    if hasattr(self._text,'__call__'):
      return self._namespace.call( self._text )
    return self._text

  @text.setter
  def text(self,val):
    if hasattr(val,'__call__'):
      self._text = val
    else:
      self._text = self._lint(val)
  
  @property
  def formatted_text(self):
      return self._formatter.fmt( self.text, **self.NS.__dict__ )


class Essay(Text):
  def __init__(self):
    super().__init__()
