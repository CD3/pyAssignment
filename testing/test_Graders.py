import pytest
import os,pickle

from pyAssignment.Graders.CLGrader import CLGrader, ShellTest

def test_CLGrader_simple():
  g = CLGrader()

  with g.add_test() as t:
    t.NS.FILE = "file1.txt"
    t.command = "touch {FILE}"

  if os.path.isfile( "file1.txt" ):
    os.remove("file1.txt")
  g.run()

  assert os.path.isfile("file1.txt")

  os.remove("file1.txt")

def test_CLGrader_tests_summary():
  g = CLGrader()

  with g.add_test() as t:
    t.command = "ls"
  with g.add_test() as t:
    t.command = "pwd"
  with g.add_test() as t:
    t.command = "lkdfs"
  with g.add_test() as t:
    t.command = "test 1 -eq 0"
  with g.add_test() as t:
    t.command = "ls"

  g.run()

  assert g.num_tests == 5
  assert g.num_fail == 2
  assert g.num_pass == 3

  assert g.summary.split("\n")[0].startswith("PASS")
  assert g.summary.split("\n")[1].startswith("PASS")
  assert g.summary.split("\n")[2].startswith("FAIL")
  assert g.summary.split("\n")[-1] == ""

def test_CLGrader_namespace_inheritance():
  g = CLGrader()
  g.NS.VAR1 = "x"

  with g.add_test() as t:
    t.NS.VAR2= "y"
    t.command = "echo {VAR1}{VAR2}"

  assert g._tests[0].command == "echo xy"

def test_CLGrader_workdir():
  g = CLGrader()

  with g.add_test() as t:
    t.command = "pwd"

  with g.add_test() as t:
    t.directory = "test"
    t.command = "pwd"

  with g.directory("test"):
    with g.add_test() as t:
      t.command = "pwd"
    with g.add_test() as t:
      t.command = "pwd"

  with g.add_test() as t:
    t.command = "pwd"

  if not os.path.isdir("test"): os.mkdir("test")
  g.run()
  os.rmdir("test")

  for i in [ 0, 4 ]:
    assert g._tests[i].command.startswith("pwd")
    assert g._tests[i].directory is None
    assert g._tests[i].output.strip() == os.getcwd()

  for i in range(1,4):
    assert g._tests[i].command.startswith("cd")
    assert g._tests[i].directory == "test"
    assert g._tests[i].output.strip() == os.path.join(os.getcwd(),"test")

def test_CLGrader_shelltest_pickle():
  t = ShellTest()
  t.command = "pwd"
  t2 = pickle.loads( pickle.dumps(t) )

  assert len(t2._cmds) == 1
  assert t2._cmds[0] == "pwd"
  assert t2.command == "pwd"

  t = ShellTest()
  t.command = "ls {DIR}"
  t.NS.DIR = "dir1"
  t2 = pickle.loads( pickle.dumps(t) )

  assert len(t2._cmds) == 1
  assert t2._cmds[0] == "ls {DIR}"
  assert t2.command == "ls dir1"
  assert t2.NS.DIR  == "dir1"

def test_CLGrader_clgrader_pickle():
  g = CLGrader()

  with g.add_test() as t:
    t.NS.FILE = "file1.txt"
    t.command = "touch {FILE}"


  g2 = pickle.loads( pickle.dumps(g) )

def test_CLGrader_grader_script():
  g = CLGrader()

  with g.add_test() as t:
    t.NS.FILE = "file1.txt"
    t.command = "touch {FILE}"

  with g.add_test() as t:
    t.command = "test 1 -eq 0"
    t.description = "test that will fail"

  with g.add_test() as t:
    t.command = "tst 1 -eq 0"
    t.description = "another test that will fail"

  with g.add_test() as t:
    t.command = "pwd"

  g.write_grader_script("grader.py")


def test_CLGrader_on_fail_callback():
  if os.path.exists("ON_FAIL_CMD.txt"):
    os.remove("ON_FAIL_CMD.txt")
  if os.path.exists("ON_PASS_CMD.txt"):
    os.remove("ON_PASS_CMD.txt")

  assert not os.path.exists("ON_FAIL_CMD.txt")
  assert not os.path.exists("ON_PASS_CMD.txt")

  g = CLGrader()
  with g.add_test() as t:
    t.command = "doe-not-exist-cmd arg1 arg2"
    with t.add_on_fail_test() as ft:
      ft.command = 'touch ON_FAIL_CMD.txt'
    with t.add_on_pass_test() as pt:
      pt.command = 'touch ON_PASS_CMD.txt'

  g.run()

  assert os.path.exists("ON_FAIL_CMD.txt")
  assert not os.path.exists("ON_PASS_CMD.txt")

def test_CLGrader_on_pass_callback():
  if os.path.exists("ON_FAIL_CMD.txt"):
    os.remove("ON_FAIL_CMD.txt")
  if os.path.exists("ON_PASS_CMD.txt"):
    os.remove("ON_PASS_CMD.txt")

  assert not os.path.exists("ON_FAIL_CMD.txt")
  assert not os.path.exists("ON_PASS_CMD.txt")

  g = CLGrader()
  with g.add_test() as t:
    t.command = "ls"
    with t.add_on_fail_test() as ft:
      ft.command = 'touch ON_FAIL_CMD.txt'
    with t.add_on_pass_test() as pt:
      pt.command = 'touch ON_PASS_CMD.txt'

  g.run()

  assert not os.path.exists("ON_FAIL_CMD.txt")
  assert os.path.exists("ON_PASS_CMD.txt")

@pytest.mark.skip()
def test_CLGrader_multiple_commands():
  g = CLGrader()

  with a.add_test() as t:
    t.NS.DIR = "dir1"
    t.NS.FILE = "file.txt"

    t.commands += "test -d {DIR}"
    t.commands += "test -f {DIR}/{FILE}"

@pytest.mark.skip()
def test_CLGrader_on_fail_extra_commands():
  g = CLGrader()

  with a.add_test() as t:
    t.NS.SCRIPTNAME = "sin.gnuplot"
    t.NS.IMAGENAME = "sin.png"

    t.directory = "gnuplot"
    t.commands += "gnuplot {SCRIPTNAME}"
    t.commands += "test -f {IMAGENAME}"

    t.on_fail = "touch {IMAGENAME}"
    t.on_pass = None




@pytest.mark.skip()
def test_CLGrader_basic():
  g = CLGrader()


  with a.add_test() as t:
    t.commands += "test -f {IMAGENAME}"
    t.run_if = cmd("test -e {IMAGENAME}")



