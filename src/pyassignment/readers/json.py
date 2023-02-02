from .reader_base import *
import json

class JSON(ReaderBase):
  def __init__(self,fh=None):
    self.fh = fh


  def load(self, fh=None, ass=None):
    fh = super().get_fh(fh)

    data = json.load(fh)

    # process the data tree. for example, we may have an entry named "Questions", which needs
    # to be renamed to 'questions'
    for k in data.keys():
      if k.lower() != k:
        data[k.lower()] = data[k]
        del data[k]

    return self._load_from_dict(data)

