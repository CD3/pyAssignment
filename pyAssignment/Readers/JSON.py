from .ReaderBase import *
import json

class JSON(ReaderBase):
  def __init__(self,fh=None):
    self.fh = fh


  def load(self, ass, fh=None):
    fh = super().get_fh(fh)

    data = json.load(fh)

    print(data)

