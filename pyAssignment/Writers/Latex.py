
from .WriterBase import *
from ..Assignment import *


class LatexWriter(WriterBase):

  def __init__(self,fh=None):
    super().__init__()

  def dump(self,fh):
    fh = super().get_fh(fh)

    

