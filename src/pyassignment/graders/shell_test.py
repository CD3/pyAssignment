from .test import *
from .utils import *
import re


class ShellTest(Test):
  def __init__(self):
    super().__init__()
    self._scmds = "" # setup commands
    self._cmds  = ""
    self._ecmds = "" # teardown command
    self._o = ""
    self._e = ""
    self._r = None

  def _update(self,other):
    super()._update(other)
    self._scmds = other._scmds
    self._ecmds = other._ecmds

  def build_command_string( self,cmds ):
    cmds_string = ";".join(cmds)
    cmds_string = self._formatter.fmt( cmds_string, **self.NS.__dict__, **os.environ )
    # need to check cmds_string for lines that start with a ';'. these will cause a syntax error
    # in bash.
    cmds_string = re.sub(r"^\s*;","", cmds_string, flags=re.M)
    return cmds_string

  @property
  def test_command_string(self):
    startup = "cd %s;"%self._dir if self._dir is not None else ""
    cmds = [ c.strip(';') for c in  [startup, self._cmds] if c != "" ]
    return self.build_command_string(cmds)

  @property
  def command_string(self):
    cmds = [ c.strip(';') for c in  [self._scmds, self.test_command_string, self._ecmds] if c != "" ]
    return self.build_command_string(cmds)

  @property
  def command(self):
    return self._cmds

  @command.setter
  def command(self,val):
    self._cmds = val

  @property
  def startup_command(self):
    return self._scmds

  @startup_command.setter
  def startup_command(self,val):
    self._scmds = val

  @property
  def cleanup_command(self):
    return self._ecmds

  @cleanup_command.setter
  def cleanup_command(self,val):
    self._ecmds = val

  @property
  def returncode(self):
    return self._r

  @property
  def output(self):
    return self._o

  @property
  def error(self):
    return self._e

  def __run__(self):
    if self.command_string == "":
      raise Exception("No command set for ShellTest.")
    self._r,self._o,self._e = run(self.command_string,**self._meta.__dict__.get('run_kwargs',{}))
    return self._r == 0

  def __summarize__(self,prefix=""):
    s = ""
    if self.returncode != 0:
      s += prefix+"  ran command: "+self.test_command_string+"\n"
      s += prefix+"  return code: "
      s += str(self.returncode)
      s += "\n"
      s += prefix+"     output: "
      s += self.output.strip()
      s += "\n"
      s += prefix+"  error msg: "
      s += self.error.strip()
      s += "\n"

    return s

