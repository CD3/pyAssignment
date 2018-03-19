from .ReaderBase import *

class Markdown(ReaderBase)
  def __init__(self,fh=None):
    super().__init__(fh)


  def load(self, ass, fh=None):
    fh = super().get_fh(fh)

    

