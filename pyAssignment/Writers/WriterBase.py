
class WriterBase(object):
  def __init__(self,fh=None):
    self.fh = fh

  def get_fh(self,fh=None):
    if fh is None:
      fh = self.fh
    if fh is None:
      raise(RuntimeError("No filehandle available."))
    return fh
