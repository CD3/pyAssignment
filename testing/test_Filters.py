import pytest

import io

from pyAssignment.Assignment import Assignment
import pyAssignment.Filters as Filters
import pyAssignment.Writers as Writers


def test_extract_quiz():

  ass = Assignment()

  with ass.add_question() as q:
    q.text = "q1"

    with q.add_question() as qq:
      qq.text = "q1:qq"

  with ass.add_question() as q:
    q.text = "q2"

    with q.add_part() as p:
      p.text = "q2p1"

      with q.add_question() as qq:
        qq.text = "q2p1:qq"

  with ass.add_question() as q:
    q.text = "q3"

    with q.add_part() as p:
      p.text = "q3p1"

      with q.add_question() as qq:
        qq.text = "q3p1:qq"

    with q.add_part() as p:
      p.text = "q3p2"

  filt = Filters.QuizExtractor()

  quiz = filt.filter(ass)

  fh = io.StringIO()
  writer = Writers.Simple(fh)
  writer.dump(quiz)

  print(fh.getvalue())


