from .answer_base import *
from random import shuffle

class MultipleChoice(AnswerBase):
  def __init__(self):
    super().__init__()
    self._choices = collection()
    self._correct = collection()


  # we want to support a natural and consistent interface.
  # all of the following should work the way the user woudl expect
  #
  # scenario 1:
  #
  # a.choices  = 'one'
  # a.choices += 'two'
  # a.choices += 'three'
  # a.set_correct('two')
  #
  #
  # scenario 2
  #
  # a.correct   = '...'
  # a.incorrect = '...'
  #
  # scenario 3
  #
  # a.correct += '...'
  # a.incorrect += '...'
  # a.incorrect += '...'
  # a.incorrect += '...'
  #
  # scenario 4
  #
  # a.correct = '...'
  # a.incorrect += '...'
  # a.incorrect += '...'
  # ...
  # a.correct = 'new value'
  #
  #
  # Notes:
  # a.property = val calls the property setter
  # a.property += val calls the property getter,
  #                   then calls the __iadd__ function on the returned object,
  #                   then calls the property setter.
  #                   however, the property will already have been modified by the +=
  #
  # we need a way to tell the difference between these two
  #
  # create a proxy class to help determine if correct/incorrect were
  # called with = or +=
  class Proxy(object):
    def __init__(self):
      self._add = None

    def __iadd__(self,val):
      if self._add is None:
        self._add = collection()
      self._add += val
      return self


  @property
  def choices(self):
    return self._choices

  @choices.setter
  def choices(self,val):
    self._choices = collection()
    self._choices += val

  @property
  def correct(self):
    return MultipleChoice.Proxy()

  @correct.setter
  def correct(self,val):
    # the only (supported) way for us to get a Proxy instance
    # is if they called the correct property.
    if isinstance(val,MultipleChoice.Proxy):
      if val._add is not None:
        self._choices += val._add
        self.add_correct(self._choices[-1])

    else:
      # we need to set the correct choice, but we want to
      # leave the incorrect choices.
      new_choices = collection()
      for i in range(len(self._choices)):
        if not i in self._correct:
          new_choices.append(self._choices[i])

      self._choices = new_choices
      self._correct = collection()
      self._choices += val
      self.add_correct(self._choices[-1])

  @property
  def incorrect(self):
    return MultipleChoice.Proxy()

  @incorrect.setter
  def incorrect(self,val):
    if isinstance(val,MultipleChoice.Proxy):
      if val._add is not None:
        self._choices += val._add
    else:
      # we need to set the incorrect choice, but we want to
      # leave the correct choices.
      new_choices = collection()
      for i in range(len(self._choices)):
        if i in self._correct:
          new_choices.append(self._choices[i])

      self._choices = new_choices
      self._correct = collection()
      self._choices += val





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


  def shuffle(self):
    idx = [ i for i in range(len(self._choices)) ]
    shuffle(idx)
    old_choices = self._choices
    self._choices = collection()
    for i in idx:
      self._choices.append( old_choices[i] )
    old_correct = self._correct
    self._correct = collection()
    for i in old_correct:
      self._correct.append( idx.index(i) )



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
