from .ReaderBase import *
from .HTML import *
import mistletoe

class Markdown(ReaderBase):
  '''A (very) limited Markdown parser. Currently
     just supports parsing multiple choice questions.'''

  def __init__(self,fh=None):
    super().__init__(fh)

  def load(self, fh=None, ass=None):
    if ass is None:
      ass = Assignment()

    fh = super().get_fh(fh)

    # print(mistletoe.markdown(fh))
    return HTML().load(io.StringIO(mistletoe.markdown(fh)))


    

