import pytest

import io,os,re

from pyAssignment.Assignment import Assignment
import pyAssignment.Writers as Writers
import pyAssignment.Assignment.Answers as Answer

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

def test_latex_writer_raises_with_no_fh():
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
NUM\tq2.1\t1.23E+00\t1.23E-02
NUM\tq2.2 Give your answer in meter / second.\t9.88E+08\t9.88E+06
NUM\tq2.3\t5.43E+03\t5.43E+01
NUM\tq2.4 Give your answer in meter.\t1.02E+01\t3.21E+00
FIB\tq3.1\tcorrect answer
FIB\tq3.2\tfirst correct answer\tsecond correct answer
"""




  assert fh.getvalue() == quiz_text

@pytest.mark.skip(reason="Have not added expand-macros support to rewrite")
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
  writer.make_key = True

  ass = Assignment()
  ass.meta.title = "Homework Assignment"
  ass.meta.header = {'R':r"powered by \LaTeX"}
  ass.meta.config = {
                    'answers' : {
                      'numerical/spacing' :  '2in',
                      'multiple_choice/symbol' :  r'\alph*)',
                      'text/spacing' :  r'3in'
                      }
                    }

  with ass.add_information() as info:
    info.text = "This is some information for the assignment."

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
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.correct += "a1"
      a.incorrect += "a2"
      a.incorrect += "a3"
      a.correct += "a4"

  writer.dump(ass)

  with open('test.tex', 'w') as f:
    f.write(fh.getvalue())

def test_latex_writer_header_and_footers():
  ass = Assignment()
  ass.meta.title = "The Title"
  ass.meta.header = {'R':"right header",
                     'L':"left header",
                     'C':"center header"}
  ass.meta.footer = {'R':"right footer",
                     'L':"left footer",
                     'C':"center footer"}
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
      a.correct += "a2"


  fh = io.StringIO()
  writer = Writers.Latex(fh)
  writer.make_key = True

  writer.dump(ass)

  print(fh.getvalue())
  assert re.search( "header", fh.getvalue() )
  assert re.search( "footer", fh.getvalue() )
  assert re.search( "left header", fh.getvalue() )
  assert re.search( "center header", fh.getvalue() )
  assert re.search( "right header", fh.getvalue() )
  assert re.search( "left footer", fh.getvalue() )
  assert re.search( "center footer", fh.getvalue() )
  assert re.search( "right footer", fh.getvalue() )
  assert re.search( r"\\title\{The Title\}", fh.getvalue() )


def test_blackboard_writer_figures():

  image_text = r"""<?xml version="1.0" encoding="UTF-8" ?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1">
<circle cx="125" cy="125" r="75" fill="orange" />
</svg>
"""
  with open("file.svg", "w") as f:
    f.write(image_text)



  fh = io.StringIO()
  writer = Writers.BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "See image above."
    with q.add_figure() as f:
      f.filename = "file.svg"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.incorrect += "a"
      a.correct += "b"
  with ass.add_question() as q:
    q.text = "no image here."
    with q.add_answer(Answer.MultipleChoice) as a:
      a.correct += "a"
      a.incorrect += "b"

  writer.dump(ass)

  quiz_text = """\
MC\t{IMAGE_TEXT}</br>Consider the figure above. See image above.\ta\tincorrect\tb\tcorrect\tNone of the above.\tincorrect
MC\tno image here.\ta\tcorrect\tb\tincorrect\tNone of the above.\tincorrect
""".format(IMAGE_TEXT=image_text.replace("\n","\n"))

  assert fh.getvalue() == quiz_text

  with open("Bb-quiz-with-figure.txt","w") as f:
    writer.dump(ass,f)
    
def test_blackboard_quiz_writer_with_numerical_answer_tolerance():
  fh = io.StringIO()
  writer = Writers.BlackboardQuiz(fh)

  ass = Assignment()
  with ass.add_question() as q:
    q.text = "q1"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = UQ_(Q_(10,'m'),Q_(1,'m'))
  with ass.add_question() as q:
    q.text = "q2"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = UQ_(Q_('10','m'),Q_('1','cm'))
  with ass.add_question() as q:
    q.text = "q3"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = Q_(10,'m')
  with ass.add_question() as q:
    q.text = "q4"
    with q.add_answer(Answer.Numerical) as a:
      a.quantity = Q_('10','m')

  writer.dump(ass)

