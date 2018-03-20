from .ReaderBase import *
from .HTML import *
import mistletoe

class Markdown(ReaderBase):
  def __init__(self,fh=None):
    super().__init__(fh)

  def load(self, fh=None, ass=None):
    if ass is None:
      ass = Assignment()

    fh = super().get_fh(fh)

    reader = HTML(fh)
    ass = reader.load()

    return ass

    

