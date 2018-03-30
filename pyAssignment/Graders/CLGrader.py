from .GraderBase import *

import contextlib

def run(cmd,**kwargs):
  pass

class Test(object):
  def __init__(self):
    self._cmds = collection()
    self._o = None
    self._r = None

  def run(self):
    pass

  @contextlib.contextmanager
  def add_fail_callback(self):
    pass


class CLGrader(GraderBase):
  def __init__(self):
    super().__init__()
    self._tests = collection()

  def run(self):
    pass

  @contextlib.contextmanager
  def add_test(self):
    pass

