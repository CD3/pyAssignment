from .grader_base import *
from ..utils import Namespace, SFFormatter, working_directory
from .utils import *
from .shell_test import ShellTest
from .python_test import PythonTest

import os
import contextlib
import inspect
import pathlib
import textwrap
import sys

#   ____ _     ____               _
#  / ___| |   / ___|_ __ __ _  __| | ___ _ __
# | |   | |  | |  _| '__/ _` |/ _` |/ _ \ '__|
# | |___| |__| |_| | | | (_| | (_| |  __/ |
#  \____|_____\____|_|  \__,_|\__,_|\___|_|

class CLGrader(GraderBase):
  '''
  A command-line grader.

  A grader is just a collection of tests. It can also store some data that is common to all tests. For example,
  the graders namespace member (NS) will be passed to all tests when added.
  '''
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

  @property
  def test_output(self):
    s = ""
    for t in self._tests:
      s += t.test_output()
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
    # with open(fn,'w') as f:
    #   f.write("script = ")
    #   f.write(str(pickle.dumps(self)))
    #   f.write("\n")


    #   f.write("import pickle\n")
    #   f.write("g = pickle.loads(script)\n")
    #   f.write("g.run()\n")
    #   f.write("print(g.summary)\n")

    def write_test(test,depth=1):
        lines = []
        for k,v in test.NS.__dict__.items():
            lines.append(f'''{'  '*depth}t.NS.{k} = """{v}"""''')
        lines.append(f'''{'  '*depth}{'t'*depth}._name = """{test._name}"""''')
        lines.append(f'''{'  '*depth}{'t'*depth}._desc = """{test._desc}"""''')

        if isinstance(test,ShellTest):
            lines.append(f'''{'  '*depth}{'t'*depth}._scmds = """{test._scmds}"""''')
            lines.append(f'''{'  '*depth}{'t'*depth}._cmds = """{test._cmds}"""''')
            lines.append(f'''{'  '*depth}{'t'*depth}._ecmds = """{test._ecmds}"""''')
        if isinstance(test,PythonTest):
            lines.append(textwrap.indent(textwrap.dedent(inspect.getsource(test._func)),prefix="  "*depth))
            lines.append(f'''{'  '*depth}{'t'*depth}._func = {test._func.__name__}''')

        for ttest in test._on_fail_tests:
            lines.append(f'''{'  '*depth}with {'t'*depth}.add_on_fail_test() as {'t'*(depth+1)}:''')
            lines += write_test(ttest,depth+1)

        for ttest in test._on_pass_tests:
            lines.append(f'''{'  '*depth}with {'t'*depth}.add_on_pass_test() as {'t'*(depth+1)}:''')
            lines += write_test(ttest,depth+1)

        return lines


    lines = []
    lines.append('''from pyassignment.graders.cl_grader import CLGrader, ShellTest, PythonTest''')

    lines.append('''g = CLGrader()''')

    for t in self._tests:
        lines.append(f'''with g.add_test( {t.__class__.__name__} ) as t:''')
        lines += write_test(t)

    lines.append('''g.run()''')
    lines.append('''print(g.summary)''')


    with open(fn,'w') as f:
        f.write("\n".join(lines) + "\n")


