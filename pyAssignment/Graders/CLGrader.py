from .GraderBase import *
from ..Utils import Namespace, SFFormatter, working_directory

import contextlib, subprocess, io, inspect, os, re

def run(cmd,**kwargs):
  '''
  Run a shell command and return the exit code, standard output, and standar error.
  '''
  c = subprocess.run( cmd, shell=True, executable="/bin/bash", stdout=subprocess.PIPE, stderr=subprocess.PIPE )
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


class Test(object):
  '''
  A test class represents a single test that will be ran during grading.

  A test has a name, description, working directory, result, and a set of other
  tests to run if the current tests fails or passes.

  This class should be derived to implement specific test types. The deriving
  class only needs to implements the '__run__()' method, which will be called
  by this class.

  Properties:

    NS : A namespace that will be used when formatting strings.
    meta : A dict for string meta-data in the tests. Different tests can use this data to change behavior.
    name : A name for the test.
    description : A description of what the test does.
    directory : A directory that the test should be ran in.
    result : The result of the test. True means PASS. False means FAIL.
    score : The score for the test, i.e. the nubmer of points to add for this test.
    weight : The weight that should be given to the test score when total the score for multiple tests.
  '''
  def __init__(self):
    self._name = None
    self._desc = None
    self._dir = None
    self._result = None

    self._on_fail_tests = collection()
    self._on_pass_tests = collection()

    self._formatter = SFFormatter()

    self._namespace = Namespace()
    self._meta      = Namespace()

  def _update(self,other):
    self.NS.__dict__.update( other.NS.__dict__ )
    self.meta.__dict__.update( other.meta.__dict__ )
    self.working_directory = other._dir

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
  def working_directory(self):
    if self._dir is None:
      return None
    else:
      return self._formatter.fmt( self._dir, **self.NS.__dict__ )

  @working_directory.setter
  def working_directory(self,val):
    self._dir = val

  def run(self):
    # run this test
    with working_directory(self.working_directory):
      self._result = self.__run__()

    # if test passed, run the "on pass" tests
    if self._result and len(self._on_pass_tests) > 0:
      for t in self._on_pass_tests:
        t.run()

    # if test fails, run the "on fail" tests
    if not self._result and len(self._on_fail_tests) > 0:
      for t in self._on_fail_tests:
        t.run()

    # return the result of this test
    return self._result

  @contextlib.contextmanager
  def add_on_fail_test(self,test=None):
    if test is None:
      test = self.__class__
    if inspect.isclass(test):
      t = test()
    else:
      t = test

    t._update(self)

    yield t
    if t._name is None:
      t.name = "Failure Follow-up Test "+str(len(self._on_fail_tests))

    self._on_fail_tests.append(t)

  @contextlib.contextmanager
  def add_on_pass_test(self,test=None):
    if test is None:
      test = self.__class__
    if inspect.isclass(test):
      t = test()
    else:
      t = test

    t._update(self)

    yield t
    if t._name is None:
      t.name = "Success Follow-up Test "+str(len(self._on_pass_tests))
    self._on_pass_tests.append(t)

  @property
  def result(self):
    return self._result

  @property
  def score(self):
    # return None if the test hasn't been run
    if self._result is None:
      return None

    # if test succeeded, return 100%
    if self._result:
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

  def summarize(self,prefix=""):
    s = ""
    if self.result is None:
      s += prefix+"DID NOT RUN\n"
      return s

    if self.result:
      s += prefix+"PASS"

    if not self.result:
      s += prefix+"FAIL"

    s += "  "
    s += self.name
    s += ": "
    s += self.description
    s += "\n"

    if hasattr(self,'__summarize__'):
      s += self.__summarize__(prefix)

    if len(self._on_fail_tests):
      s += prefix+"  Additional Tests\n"
      for ft in self._on_fail_tests:
        s += ft.summarize(prefix="  "+prefix)

    if len(self._on_pass_tests):
      s += prefix+"  Additional Tests\n"
      for pt in self._on_pass_tests:
        s += pt.summarize(prefix="  "+prefix)


    return s


class ShellTest(Test):
  def __init__(self):
    super().__init__()
    self._scmds = "" # setup commands
    self._cmds  = ""
    self._ecmds = "" # teardown command
    self._o = None
    self._e = None
    self._r = None

  def _update(self,other):
    super()._update(other)
    self._scmds = other._scmds
    self._scmds = other._ecmds

  def build_command_string( self,cmds ):
    cmds_string = ";".join(cmds)
    cmds_string = self._formatter.fmt( cmds_string, **self.NS.__dict__ )
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
      s += prefix+"  error msg: "
      s += self.error.strip()
      s += "\n"

    return s

class PythonTest(Test):
  def __init__(self):
    super().__init__()
    self._func = None

  @property
  def function(self):
    return self._func

  @function.setter
  def function(self,func):
    self._func = func

  def __run__(self):
    if self._func is None:
      raise Exception("No function set for PythonTest.")
    self._result = self._func()
    return self._result



#   ____ _     ____               _           
#  / ___| |   / ___|_ __ __ _  __| | ___ _ __ 
# | |   | |  | |  _| '__/ _` |/ _` |/ _ \ '__|
# | |___| |__| |_| | | | (_| | (_| |  __/ |   
#  \____|_____\____|_|  \__,_|\__,_|\___|_|   

class CLGrader(GraderBase):
  def __init__(self, root_dir = None):
    super().__init__()
    self._tests = collection()
    self._scmds = ""
    self._ecmds = ""

    self._dir = root_dir
    if self._dir is not None:
      self._dir = os.path.abspath(self._dir)

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
      if t.result is not None and not t.result:
        n += 1
    return n

  @property
  def num_pass(self):
    n = 0
    for t in self._tests:
      if t.result is not None and t.result:
        n += 1
    return n

  @property
  def summary(self):
    s = ""
    for t in self._tests:
      s += t.summarize()
    s += "\n\n"
    s +="Summary\n"
    s += "    fail: %d\n"%self.num_fail
    s += "    pass: %d\n"%self.num_pass
    s += " missing: %d\n"%(self.num_tests - self.num_pass - self.num_fail)
    s += "===========================\n"
    s += "score: %.2f%%\n"%(100*self.score)


    return s

  @contextlib.contextmanager
  def add_test(self,test=None,NS=Namespace()):
    if test is None:
      test = ShellTest # if test type was not given, create a ShellTest
    if inspect.isclass(test):
      t = test()
    else:
      t = test

    t.NS.__dict__.update( self.NS.__dict__ )
    t.NS.__dict__.update( NS.__dict__ )
    t.meta.__dict__.update( self.meta.__dict__ )
    t.working_directory = self._dir
    # this needs to be fixed. caller can easily overwrite parent setup command by accident.
    t.startup_command = self.startup_command
    t.clenaup_command = self.cleanup_command
    yield t
    if t._name is None:
      t.name = "Test "+str(len(self._tests))
    self._tests.append(t)

  @contextlib.contextmanager
  def directory(self,dir):
    odir = self._dir
    if os.path.isabs(dir):
      self._dir = dir
    else:
      if self._dir is None:
        self._dir = os.path.join( os.getcwd(), dir )
      else:
        self._dir = os.path.join( self._dir, dir )
    yield
    self._dir = odir

  @property
  def score(self):
    score = 0
    total_weight = sum([t.weight for t in self._tests if t.score is not None])
    for t in self._tests:
      if t.score is not None:
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

