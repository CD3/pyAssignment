from .answer_base import *

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
