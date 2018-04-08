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

  if 'debug' in kwargs and kwargs['debug']:
    print("CMD:",cmd)
    print("R:",r)
    print("O:",o)
    print("E:",e)

  return r,o,e


#  ____  _          _ _ _____         _   
# / ___|| |__   ___| | |_   _|__  ___| |_ 
# \___ \| '_ \ / _ \ | | | |/ _ \/ __| __|
#  ___) | | | |  __/ | | | |  __/\__ \ |_ 
# |____/|_| |_|\___|_|_| |_|\___||___/\__|

class ShellTest(object):
  def __init__(self):
    self._name = None
    self._desc = None
    self._scmds = "" #collection() # setup commands
    self._cmds  = "" #collection()
    self._ecmds = "" #collection() # teardown command
    self._o = None
    self._e = None
    self._r = None
    self._dir = None

    self._on_fail_tests = collection()
    self._on_pass_tests = collection()

    self._formatter = SFFormatter()

    self._namespace = Namespace()
    self._meta      = Namespace()

  @property
  def NS(self):
    return self._namespace

  @property
  def meta(self):
    return self._meta

  @property
  def name(self):
    if self._name is None:
      return ""
    else:
      return self._formatter.fmt( self._name , **self.NS.__dict__ )

  @name.setter
  def name(self,val):
    self._name = val

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
  def command_string(self):
    startup = "cd %s;"%self._dir if self._dir is not None else ""
    cmds = [ c.strip(';') for c in  [startup, self._scmds, self._cmds, self._ecmds] if c != "" ]
    cmds_string = self._formatter.fmt( ";".join(cmds), **self.NS.__dict__ )
    return cmds_string

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


  @property
  def directory(self):
    if self._dir is None:
      return None
    else:
      return self._formatter.fmt( self._dir, **self.NS.__dict__ )

  @directory.setter
  def directory(self,val):
    self._dir = val

  def run(self):
    self._r,self._o,self._e = run(self.command_string,**self._meta.__dict__.get('run_kwargs',{}))
    if self._r == 0 and len(self._on_pass_tests) > 0:
      for t in self._on_pass_tests:
        t.run()
    if self._r != 0 and len(self._on_fail_tests) > 0:
      for t in self._on_fail_tests:
        t.run()


  @contextlib.contextmanager
  def add_on_fail_test(self):
    t = ShellTest()
    t.NS.__dict__.update( self.NS.__dict__ )
    t.meta.__dict__.update( self.meta.__dict__ )
    t.directory = self._dir
    yield t
    if t._name is None:
      t.name = "Failure Follow-up Test "+str(len(self._on_fail_tests))
    self._on_fail_tests.append(t)

  @contextlib.contextmanager
  def add_on_pass_test(self):
    t = ShellTest()
    t.NS.__dict__.update( self.NS.__dict__ )
    t.meta.__dict__.update( self.meta.__dict__ )
    t.directory = self._dir
    yield t
    if t._name is None:
      t.name = "Success Follow-up Test "+str(len(self._on_pass_tests))
    self._on_pass_tests.append(t)

  @property
  def weight(self):
    try: return self._weight
    except: return 1

  @weight.setter
  def weight(self,val):
    self._weight = val

  @property
  def fail_tests_weight(self):
    try: return self._fail_tests_weight
    except: return 0.5

  @fail_tests_weight.setter
  def fail_tests_weight(self,val):
    self._fail_tests_weight = val


  @property
  def score(self):
    # return None if the test hasn't been run
    if self._r is None:
      return None

    # if test succeeded, return 100%
    if self._r == 0:
      return 1
    else:
      # if test failed,
      # add up the score from the _on_fail_tests (if any)
      # and return
      score = 0
      total_weight = sum([t.weight for t in self._on_fail_tests])
      for t in self._on_fail_tests:
        score += t.weight * t.score / total_weight
      score *= self.fail_tests_weight
      return score


#   ____ _     ____               _           
#  / ___| |   / ___|_ __ __ _  __| | ___ _ __ 
# | |   | |  | |  _| '__/ _` |/ _` |/ _ \ '__|
# | |___| |__| |_| | | | (_| | (_| |  __/ |   
#  \____|_____\____|_|  \__,_|\__,_|\___|_|   

class CLGrader(GraderBase):
  def __init__(self):
    super().__init__()
    self._tests = collection()
    self._scmds = ""
    self._ecmds = ""

    self._dir = None

    self._namespace = Namespace()
    self._meta      = Namespace()

  @property
  def NS(self):
    return self._namespace

  @property
  def meta(self):
    return self._meta


  def run(self):
    for t in self._tests:
      t.run()

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
  def num_pass(self):
    n = 0
    for t in self._tests:
      if t.returncode is not None and t.returncode == 0:
        n += 1
    return n

  def _summarize_test(self,t,prefix=""):
    s = ""
    if t.returncode is None:
      s += prefix+"DID NOT RUN\n"
      return s
    if t.returncode == 0:
      s += prefix+"PASS"
    if t.returncode != 0:
      s += prefix+"FAIL"
    s += "  "
    s += t.name
    s += ": "
    s += t.description
    s += "\n"
    if t.returncode != 0:
      s += prefix+"  return code: "
      s += str(t.returncode)
      s += "\n"
      s += prefix+"  error msg: "
      s += t.error.strip()
      s += "\n"

    if len(t._on_fail_tests):
      s += prefix+"Additional Tests\n"
      for ft in t._on_fail_tests:
        s += self._summarize_test(ft,prefix="  "+prefix)

    if len(t._on_pass_tests):
      s += prefix+"Additional Tests\n"
      for pt in t._on_pass_tests:
        s += self._summarize_test(pt,prefix="  "+prefix)

    return s

  @property
  def summary(self):
    s = ""
    for t in self._tests:
      s += self._summarize_test(t)
    s += "\n\n"
    s +="Summary\n"
    s += "    fail: %d\n"%self.num_fail
    s += "    pass: %d\n"%self.num_pass
    s += " missing: %d\n"%(self.num_tests - self.num_pass - self.num_fail)
    s += "===========================\n"
    s += "score: %.2f%%\n"%(100*self.score)


    return s

  @contextlib.contextmanager
  def add_test(self):
    t = ShellTest()
    t.NS.__dict__.update( self.NS.__dict__ )
    t.meta.__dict__.update( self.meta.__dict__ )
    t.directory = self._dir
    yield t
    if t._name is None:
      t.name = "Test "+str(len(self._tests))
    t.startup_command = (self.startup_command + ";" +   t.startup_command).strip(";")
    t.clenaup_command =    (t.cleanup_command + ";" +self.cleanup_command).strip(";")
    self._tests.append(t)

  @contextlib.contextmanager
  def directory(self,dir):
    odir = self._dir
    self._dir = dir
    yield
    self._dir = odir

  @property
  def score(self):
    score = 0
    total_weight = sum([t.weight for t in self._tests])
    for t in self._tests:
      score += t.weight * t.score / total_weight
    return score


  def write_grader_script(self,fn):
    with open(fn,'w') as f:
      f.write("script = ")
      f.write(str(pickle.dumps(self)))
      f.write("\n")


      f.write("import pickle\n")
      f.write("g = pickle.loads(script)\n")
      f.write("g.run()\n")
      f.write("print(g.summary)\n")

