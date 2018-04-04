import pytest
import os

from pyAssignment.Graders.CLGrader import CLGrader

def test_CLGrader_simple():
  g = CLGrader()

  with g.add_test() as t:
    t.NS.FILE = "file1.txt"
    t.command = "touch {FILE}"

  if os.path.isfile( "file1.txt" ):
    os.remove("file1.txt")
  g.run()

  assert os.path.isfile("file1.txt")

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
  assert g.num_success == 3

  assert g.summary.split("\n")[0].startswith("PASS")
  assert g.summary.split("\n")[1].startswith("PASS")
  assert g.summary.split("\n")[2].startswith("FAIL")
  assert g.summary.split("\n")[-1] == ""
  assert len(g.summary.split("\n")) == 6

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
    t.on_success = None


@pytest.mark.skip()
def test_CLGrader_on_fail_callback():
  g = CLGrader()


  with a.add_test() as t:
    t.NS.SCRIPTNAME = "cos.gnuplot"
    t.NS.IMAGENAME = "cos.png"

    t.directory = "gnuplot"
    t.commands += "gnuplot {SCRIPTNAME}"
    t.commands += "test -f {IMAGENAME}"

    with t.add_fail_callback() as f:
      f.commands += 'gnuplot $(find_file "{SCRIPTNAME}")'
      with f.add_fail_callback() as ff:
        ff.commands += '''gnuplot -e 'set term png; set ouptut "{IMAGENAME}"' $(find_file "{SCRIPTNAME}")'''


@pytest.mark.skip()
def test_CLGrader_basic():
  g = CLGrader()


  with a.add_test() as t:
    t.commands += "test -f {IMAGENAME}"
    t.run_if = cmd("test -e {IMAGENAME}")



