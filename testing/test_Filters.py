import pytest

import io

from pyassignment.Assignment import Assignment
import pyassignment.Writers as Writers
import pyassignment.Assignment.Answers as Answer

import pyassignment.Filters as Filters

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

  # print(fh.getvalue())


def test_question_tagging():

  ass = Assignment()
  with ass.add_question() as q:
    q.tags = "topic 1"
    q.tags += "topic 2"
    q.text = "q1"
    with q.add_answer(Answer.Text) as a:
      a.text = 'the answer'

  with ass.add_question() as q:
    q.tags = "topic 3"
    q.text = "q2"
    with q.add_part() as p:
      p.text = "q2p1"
      with p.add_answer(Answer.Text) as a:
        a.quantity = 2.34

  with ass.add_question() as q:
    q.text = "q3"
    q.tags = "topic 2"
    with q.add_part() as p:
      p.text = "q3p1"
      with p.add_answer(Answer.Text) as a:
        a.quantity = 3.10
    with q.add_part() as p:
      p.text = "q3p2"
      with p.add_answer(Answer.Text) as a:
        a.quantity = 3.2

  fass = Filters.filter( Filters.has_tag('topic 2'), ass )
  assert len(fass._questions) == 2
  assert fass._questions[0]._text == "q1"
  assert fass._questions[1]._text == "q3"

  fass = Filters.filter( Filters.has_tag('topic 3'), ass )
  assert len(fass._questions) == 1
  assert fass._questions[0]._text == "q2"


  fass = Filters.filter( Filters.has_tag("topic 2"), ass )
  assert len(fass._questions) == 2
  assert fass._questions[0]._text == "q1"
  assert fass._questions[1]._text == "q3"

  fass = Filters.filter( Filters.has_tag("topic 3"), ass )
  assert len(fass._questions) == 1
  assert fass._questions[0]._text == "q2"

  fass = Filters.filter( Filters.has_matching_tag("topic ."), ass )
  assert len(fass._questions) == 3
  assert fass._questions[0]._text == "q1"
  assert fass._questions[1]._text == "q2"
  assert fass._questions[2]._text == "q3"


def test_predicates():


  a = [v for v in range(10)]
  b = [v for v in filter(Filters.Predicate(lambda x: True) & (lambda x : x%2 == 0),a )]

  assert len(a) == 10
  assert len(b) == 5
  assert a[0] == 0
  assert a[1] == 1
  assert b[0] == 0
  assert b[1] == 2



