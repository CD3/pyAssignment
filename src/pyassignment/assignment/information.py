from .element import *

# an internal class to implement the
# information interface
# does it make sense to extract this so that
# questions can have information?... yes
class Information(Element):
  def __init__(self):
    super().__init__()

    self._text = ""

  @property
  def text(self):
    return self._text

  @text.setter
  def text(self,val):
    self._text = self._lint(val)

  @property
  def formatted_text(self):
    return self._formatter.fmt( self._text, **self.NS.__dict__ )


