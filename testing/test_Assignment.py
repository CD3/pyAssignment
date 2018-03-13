import pytest
from pyAssignment.Assignment import Assignment


def test_demo():

  ass = Assignment()

  with ass.add_question() as q:
    q.text = '''
    Compute the gravitational force exerted on a {Mass1} object by:
    '''
    q.NS.Mass1 = 1.2

    with q.add_part() as p:
      p.text = '''
      Earth.
      '''

    with q.add_part() as p:
      p.text = '''
      A {Mass2} object placed {Distance} away.
      '''

      p.NS.Mass2 = 2.3


def test_question_text():
  ass = Assignment()

  with ass.add_question() as q:
    q.text = "question 1 text"

    with q.add_part() as p:
      p.text = "question 1, part 1 text"
    with q.add_part() as p:
      p.text = "question 1, part 2 text"

  with ass.add_question() as q:
    q.text = "question 2 text"

    with q.add_part() as p:
      p.text = "question 2, part 1 text"
    with q.add_part() as p:
      p.text = "question 2, part 2 text"


  assert ass._questions[0]._text == "question 1 text"
  assert ass._questions[0]._parts[0]._text == "question 1, part 1 text"
  assert ass._questions[0]._parts[1]._text == "question 1, part 2 text"
  assert ass._questions[1]._text == "question 2 text"
  assert ass._questions[1]._parts[0]._text == "question 2, part 1 text"
  assert ass._questions[1]._parts[1]._text == "question 2, part 2 text"
