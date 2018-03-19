import pytest

import io

from pyAssignment.Assignment import Assignment
from pyAssignment.Writers.Simple import SimpleWriter
from pyAssignment.Writers.Latex import LatexWriter
from pyAssignment.Writers.BlackboardQuiz import BlackboardQuiz
import pyAssignment.Assignment.Answer as Answer
import pint
u = pint.UnitRegistry()



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

def test_latex_writer():
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
    w = LatexWriter()
    w.dump(ass)

def test_blackboard_quiz_writer_raises_on_no_answers():
  fh = io.StringIO()
  writer = BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"

  with pytest.raises(RuntimeError):
    writer.dump(ass)

def test_blackboard_quiz_writer_raises_on_unrecognized_answer_type():
  fh = io.StringIO()
  writer = BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.AnswerBase) as a:
      pass

  with pytest.raises(RuntimeError):
    writer.dump(ass)

def test_blackboard_quiz_writer_raises_on_multiple_choice_with_no_correct_answer():
  fh = io.StringIO()
  writer = BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.incorrect += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"

  with pytest.raises(RuntimeError):
    writer.dump(ass)

def test_blackboard_quiz_writer_output():
  fh = io.StringIO()
  writer = BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.incorrect += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"
      a.correct += "a4"
  with ass.add_question() as q:
    q.text = "q2"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = 1.23
  with ass.add_question() as q:
    q.text = "q3"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = u.Quantity(987654321,'m/s')
  with ass.add_question() as q:
    q.text = "q4"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = u.Quantity(5432,'')

  writer.dump(ass)

  quiz_text="""\
MC\tq1\ta1\tincorrect\ta2\tincorrect\ta3\tincorrect\ta4\tcorrect
NUM\tq2\t1.23e+00\t1.23e-02
NUM\tq3 Give your answer in meter / second.\t9.88e+08\t9.88e+06
NUM\tq4\t5.43e+03\t5.43e+01
"""




  assert fh.getvalue() == quiz_text
  
