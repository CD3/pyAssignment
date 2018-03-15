import contextlib,textwrap,re

from ..Utils import Namespace, SFFormatter


class AnswerBase(object):
  def __init__(self):
    self._namespace = Namespace()

  @property
  def NS(self):
    return self._namespace

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
  # A custom list
  class list(list):
    def __init__(self):
      super().__init__()

    def find(self, pattern, exact=True):
      if exact:
        return self.index(pattern)
      else:
        for i in range(len(self)):
          if pattern in self[i]:
            return i
          return -1

    def __iadd__(self,val):
      if not isinstance(val,list):
        val = [val]
      for item in val:
        self.append(item)

      return self

  def __init__(self):
    self._choices = MultipleChoice.list()
    self._correct = MultipleChoice.list()

  @property
  def choices(self):
    return self._choices

  @choices.setter
  def choices(self,val):
    self._choices = MultipleChoice.list()
    self._choices += val

  @choices.setter
  def incorrect(self,val):
    self.choices = val

  @choices.setter
  def correct(self,val):
    self.choices = val
    self.add_correct(self._choices[-1])



  def set_correct( self, i = None ):
    self._correct =MultipleChoice.list()
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

