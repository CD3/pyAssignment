from .element import *
import os

class Figure(Element):
  '''Represents a figure.'''

  def __init__(self):
    super().__init__()
    self._filename = ""
    self._caption = ""


  @property
  def caption(self):
    return self._caption

  @caption.setter
  def caption(self,val):
    self._caption = self._lint(val)

  @property
  def formatted_caption(self):
    return self._formatter.fmt( self._caption, **self.NS.__dict__ )

  @property
  def filename(self):
    return self._filename

  @filename.setter
  def filename(self,val):
    # store absolute path to file
    val = os.path.abspath(val)
    # todo: if file does not exist, search
    # for a candidate
    self._filename = self._lint(val)

