import pytest

import io

from pyAssignment.Assignment import Assignment
from pyAssignment.Writers.Simple import SimpleWriter


def test_simple_writer():
  ass = Assignment()

  with ass.add_question() as q:
    q.text = "q1"
    with q.add_part() as p:
      p.text = "q1p1"
    with q.add_part() as p:
      p.text = "q1p2"

  with ass.add_question() as q:
    q.text = "q2"
    with q.add_part() as p:
      p.text = "q2p1"
    with q.add_part() as p:
      p.text = "q2p2"

  with pytest.raises(RuntimeError):
    w = SimpleWriter()
    w.dump(ass)


  fh = io.StringIO()
  writer = SimpleWriter(fh)
  writer.dump(ass)

  assert fh.getvalue() == "1. q1\n  1. q1p1\n  2. q1p2\n2. q2\n  1. q2p1\n  2. q2p2\n"
