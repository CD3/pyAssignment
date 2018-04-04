from .GraderBase import *
from ..Utils import Namespace, SFFormatter

import contextlib, subprocess, io

def run(cmd,**kwargs):


  c = subprocess.run( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
  r = c.returncode
  o = c.stdout
  e = c.stderr

  try:
    o = o.decode('utf-8')
    e = e.decode('utf-8')
  except: pass

  return r,o,e

class ShellTest(object):
  def __init__(self):
    self._name = ""
    self._cmds = collection()
    self._o = None
    self._e = None
    self._r = None

    self._namespace = Namespace()
    self._formatter = SFFormatter()

  @property
  def NS(self):
    return self._namespace

  @property
  def command(self):
    return ";".join(self._cmds)

  @command.setter
  def command(self,val):
    self._cmds = collection()
    self._cmds.append(val)

  def run(self):
    cmd = self._formatter.fmt( ";".join(self._cmds), **self.NS.__dict__ )
    self._r,self._o,self._e = run(cmd)


  @property
  def returncode(self):
    return self._r

  @property
  def output(self):
    return self._o

  @property
  def error(self):
    return self._e

  @contextlib.contextmanager
  def add_fail_callback(self):
    pass



class CLGrader(GraderBase):
  def __init__(self):
    super().__init__()
    self._tests = collection()

  def run(self):
    for t in self._tests:
      t.run()

  @property
  def num_tests(self):
    return len( self._tests )

  @property
  def num_fail(self):
    n = 0
    for t in self._tests:
      if t.returncode is not None and t.returncode != 0:
        n += 1
    return n

  @property
  def num_success(self):
    n = 0
    for t in self._tests:
      if t.returncode is not None and t.returncode == 0:
        n += 1
    return n


  @contextlib.contextmanager
  def add_test(self):
    t = ShellTest()
    yield t
    self._tests.append(t)

