import pytest

import io,os

from pyAssignment.Assignment import Assignment
import pyAssignment.Writers as Writers
import pyAssignment.Assignment.Answer as Answer

import pint
u = pint.UnitRegistry()

from pyErrorProp import *
uconv = UncertaintyConvention()
units = uconv._UNITREGISTRY
UQ_ = uconv.UncertainQuantity
Q_  = UQ_.Quantity


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
    w = Writers.Simple()
    w.dump(ass)


  fh = io.StringIO()
  writer = Writers.Simple(fh)
  writer.dump(ass)

  # assert fh.getvalue() == "1. q1\n  1. q1p1\n  2. q1p2\n2. q2\n  1. q2p1\n  2. q2p2\n"

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
    w = Writers.Latex()
    w.dump(ass)

def test_blackboard_quiz_writer_raises_on_no_answers():
  fh = io.StringIO()
  writer = Writers.BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"

  with pytest.raises(RuntimeError):
    writer.dump(ass)

def test_blackboard_quiz_writer_raises_on_unrecognized_answer_type():
  fh = io.StringIO()
  writer = Writers.BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.AnswerBase) as a:
      pass

  with pytest.raises(RuntimeError):
    writer.dump(ass)

def test_blackboard_quiz_writer_raises_on_multiple_choice_with_no_correct_answer():
  fh = io.StringIO()
  writer = Writers.BlackboardQuiz(fh)
  writer.config.add_none_of_the_above_choice = False

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.incorrect += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"

  with pytest.raises(RuntimeError):
    writer.dump(ass)

  writer.config.add_none_of_the_above_choice = True
  writer.dump(ass)


  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.meta.add_none_of_the_above_choice = False
      a.incorrect += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"

  with pytest.raises(RuntimeError):
    writer.dump(ass)

def test_blackboard_quiz_writer_output():
  fh = io.StringIO()
  writer = Writers.BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1.1"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.incorrect += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"
      a.correct += "a4"
  with ass.add_question() as q:
    q.text = "q1.2"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.incorrect += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"
      a.incorrect += "a4"

  with ass.add_question() as q:
    q.text = "q2.1"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = 1.23
  with ass.add_question() as q:
    q.text = "q2.2"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = u.Quantity(987654321,'m/s')
  with ass.add_question() as q:
    q.text = "q2.3"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = u.Quantity(5432,'')
  with ass.add_question() as q:
    q.text = "q2.4"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = UQ_(Q_(10.234,'m'),Q_(321,'cm'))

  with ass.add_question() as q:
    q.text = "q3.1"
    with q.add_answer(Answer.Text) as a:
      a.text = "correct answer"
  with ass.add_question() as q:
    q.text = "q3.2"
    with q.add_answer(Answer.Text) as a:
      a.text = "first correct answer;second correct answer"
  writer.dump(ass)

  quiz_text="""\
MC\tq1.1\ta1\tincorrect\ta2\tincorrect\ta3\tincorrect\ta4\tcorrect\tNone of the above.\tincorrect
MC\tq1.2\ta1\tincorrect\ta2\tincorrect\ta3\tincorrect\ta4\tincorrect\tNone of the above.\tcorrect
NUM\tq2.1\t1.23e+00\t1.23e-02
NUM\tq2.2 Give your answer in meter / second.\t9.88e+08\t9.88e+06
NUM\tq2.3\t5.43e+03\t5.43e+01
NUM\tq2.4 Give your answer in meter.\t1.02e+01\t3.21e+00
FIB\tq3.1\tcorrect answer
FIB\tq3.2\tfirst correct answer\tsecond correct answer
"""




  assert fh.getvalue() == quiz_text

def test_blackboard_quiz_writer_output_with_macros():
  fh = io.StringIO()
  writer = Writers.BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = r"q1.1 \shell[strip]{pwd}"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.incorrect += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"
      a.correct += "a4"
  writer.dump(ass)

  quiz_text="""\
MC\tq1.1 {CWD}\ta1\tincorrect\ta2\tincorrect\ta3\tincorrect\ta4\tcorrect\tNone of the above.\tincorrect
""".format(CWD=os.path.abspath(os.getcwd()))




  assert fh.getvalue() == quiz_text
  
  

def test_latex_writer():

  fh = io.StringIO()
  writer = Writers.Latex(fh)

  ass = Assignment()
  ass.meta.title = "Homework Assignment"
  ass.meta.header = {'R':"powered by \LaTeX"}
  ass.meta.config = {
                    'answers' : {
                      'numerical/spacing' :  '2in',
                      'multiple_choice/symbol' :  r'\alph*)',
                      'text/spacing' :  r'3in'
                      }
                    }


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
    with q.add_part() as p:
      p.text = "q3p1"
    with q.add_part() as p:
      p.text = "q3p2"

  writer.dump(ass)
  print(fh.getvalue())

  with open('test.tex', 'w') as f:
    f.write(fh.getvalue())

