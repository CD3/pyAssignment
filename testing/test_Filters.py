import pytest

import io

from pyAssignment.Assignment import Assignment
import pyAssignment.Filters as Filters
import pyAssignment.Writers as Writers
import pyAssignment.Assignment.Answers as Answer


def test_extract_quiz():

  ass = Assignment()

  with ass.add_question() as q:
    q.text = "q1"

    with q.add_question() as qq:
      qq.text = "q1:qq"

      with qq.add_answer(Answer.Text) as a:
        a.text = 'the answer'

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


def test_question_tagging():

  ass = Assignment()
  with ass.add_question() as q:
    q.meta.tag = "topic 1,topic 2"
    q.text = "q1"
    with q.add_answer(Answer.Text) as a:
      a.text = 'the answer'

  with ass.add_question() as q:
    q.meta.tag = "topic 3"
    q.text = "q2"
    with q.add_part() as p:
      p.text = "q2p1"
      with p.add_answer(Answer.Text) as a:
        a.quantity = 2.34

  with ass.add_question() as q:
    q.text = "q3"
    q.meta.tag = "topic 2"
    with q.add_part() as p:
      p.text = "q3p1"
      with p.add_answer(Answer.Text) as a:
        a.quantity = 3.10
    with q.add_part() as p:
      p.text = "q3p2"
      with p.add_answer(Answer.Text) as a:
        a.quantity = 3.2

  tf = Filters.TagFilter()
  fass = tf.filter( ass, 'topic 2' )

  assert len(fass._questions) == 2
  assert fass._questions[0]._text == "q1"
  assert fass._questions[1]._text == "q3"
