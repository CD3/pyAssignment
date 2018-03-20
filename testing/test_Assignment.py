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
    q.NS.x = 10

    # with q.add_answer( Numerical ) as a:
      # def calc(x):
        # return 2*x
      # a.NS.calc = calc

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
      # with q.add_answer( MultipleChoice ) as a:
        # a.choices  = '''
                     # incorrect
                     # ^correct"
                     # also not correct
                     # incorrect 4
                     # '''



  assert ass._questions[0]._text == "question 1 text"
  assert ass._questions[0]._parts[0]._text == "question 1, part 1 text"
  assert ass._questions[0]._parts[1]._text == "question 1, part 2 text"
  assert ass._questions[1]._text == "question 2 text"
  assert ass._questions[1]._parts[0]._text == "question 2, part 1 text"
  assert ass._questions[1]._parts[1]._text == "question 2, part 2 text"

def test_figures():
  ass = Assignment()

  with ass.add_figure() as f:
    f.caption = "A"
    f.caption += " figure"
    f.filename = "image.png"


  assert len(ass._figures) == 1
  assert ass._figures[0].filename == "image.png"
  assert ass._figures[0].caption == "A figure"
  assert ass._figures[0].formatted_caption == "A figure"

  ass.NS.id = "1234"

  with ass.add_figure() as f:
    f.caption = "figure for question {id}"
    f.filename = "image.png"

  assert len(ass._figures) == 2
  assert ass._figures[0].filename == "image.png"
  assert ass._figures[0].caption == "A figure"
  assert ass._figures[0].formatted_caption == "A figure"
  assert ass._figures[1].filename == "image.png"
  assert ass._figures[1].caption == "figure for question {id}"
  assert ass._figures[1].formatted_caption == "figure for question 1234"
