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
    self._name = None
    self._desc = None
    self._cmds = collection()
    self._o = None
    self._e = None
    self._r = None
    self._dir = None

    self._namespace = Namespace()
    self._formatter = SFFormatter()

  @property
  def NS(self):
    return self._namespace

  @property
  def command(self):
    startup = "cd %s;"%self._dir if self._dir is not None else ""
    return self._formatter.fmt( startup+";".join( self._cmds), **self.NS.__dict__ )

  @command.setter
  def command(self,val):
    self._cmds = collection()
    self._cmds.append(val)

  def run(self):
    self._r,self._o,self._e = run(self.command)


  @property
  def returncode(self):
    return self._r

  @property
  def output(self):
    return self._o

  @property
  def error(self):
    return self._e

  @property
  def directory(self):
    if self._dir is None:
      return None
    else:
      return self._formatter.fmt( self._dir, **self.NS.__dict__ )

  @directory.setter
  def directory(self,val):
    self._dir = val

  @property
  def description(self):
    if self._desc is None:
      return ""
    else:
      return self._formatter.fmt( self._desc , **self.NS.__dict__ )

  @description.setter
  def description(self,val):
    self._desc = val

  @property
  def name(self):
    if self._name is None:
      return ""
    else:
      return self._formatter.fmt( self._name , **self.NS.__dict__ )

  @name.setter
  def name(self,val):
    self._name = val

  @contextlib.contextmanager
  def add_fail_callback(self):
    pass



class CLGrader(GraderBase):
  def __init__(self):
    super().__init__()
    self._tests = collection()

    self._dir = None

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

  @property
  def summary(self):
    s = ""
    for t in self._tests:
      if t.returncode is None:
        s += "DID NOT RUN\n"
        continue
      if t.returncode == 0:
        s += "PASS"
      if t.returncode != 0:
        s += "FAIL"
      s += "  "
      s += t.name
      s += ": "
      s += t.description
      s += "\n"

    return s

  @contextlib.contextmanager
  def add_test(self):
    t = ShellTest()
    t.NS.__dict__.update( self.NS.__dict__ )
    t.directory = self._dir
    yield t
    if t._name is None:
      t.name = "Test "+str(len(self._tests))
    self._tests.append(t)

  @contextlib.contextmanager
  def directory(self,dir):
    odir = self._dir
    self._dir = dir
    yield
    self._dir = odir

