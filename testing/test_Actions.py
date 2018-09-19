import pytest

import io,os,shutil,copy

from pyAssignment.Assignment import Assignment
import pyAssignment.Actions as Actions
import pyAssignment.Assignment.Answers as Answer
import pyAssignment.Writers as Writers
from pyAssignment.Filters.Predicates import has_tag

import pint
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

@pytest.mark.skipif( "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", reason="Not running latex on Travis CI" )
def test_problem_set_builder():
  ass = Assignment()
  with ass.add_question() as q:
    q.text += "Question 1"
    with q.add_question() as qq:
      qq.text += "What is the answer to Q1?"
      with qq.add_answer(Answer.Numerical) as a:
        a.quantity = 1.23

  with ass.add_question() as q:
    q.text += "Question 2"
    with q.add_part() as p:
      p.text += "Question 2, Part 1"
      with p.add_question() as qq:
        qq.text += "What is the answer to Q2P1?"
        with qq.add_answer(Answer.Numerical) as a:
          a.quantity = 2.34

  if os.path.exists("_test"): shutil.rmtree("_test")
  os.mkdir("_test")

  Actions.BuildProblemSetAndBlackboardQuiz(ass,"test")
  shutil.rmtree("_test")

  Actions.BuildProblemSetAndBlackboardQuiz(ass,"test",True)


  assert os.path.isdir("_test")
  assert os.path.isfile("_test/test.tex")
  assert os.path.isfile("_test/test.pdf")
  assert os.path.isfile("_test/test.aux")
  assert os.path.isfile("_test/test-quiz.txt")

def test_test_question_bank():
  bank = Assignment()

  def CalcAnswer(Mass):
    return (Mass*Q_(9.8,'m/s^2')).to("N")

  with bank.add_question() as q:
    q.text = r'''How much does a {Mass:} weigh?'''
    q.tags += "M1"
    q.tags += "L1"
    q.NS.Mass = Q_(10,'kg')
    with q.add_answer( Answer.Numerical ) as a:
      a.quantity = CalcAnswer
    
  with bank.add_question(copy.deepcopy(q)) as q:
    q.NS.Mass = Q_(20,'kg')
    q.answer.NS.__dict__.update( q.NS.__dict__ )

  with bank.add_question(copy.deepcopy(q)) as q:
    q.NS.Mass = Q_(30,'kg')
    q.answer.NS.__dict__.update( q.NS.__dict__ )


  def CalcAnswer(Mass1, Mass2, Distance):
    # a_r = v^2 / r = G m1 / r^2
    # v^2 = G m1 / r
    # v = sqrt( G m1 / r )
    G = Q_(6.674e-11, 'N kg^-2 m^2')
    return ((G*Mass1/Distance)**0.5).to('m/s')


  with bank.add_question() as q:
    q.text = r'''How fast will a {Mass1} mass in a {Distance} orbit around a {Mass2} mass be traveling?'''
    q.tags += "M1"
    q.tags += "L2"
    q.NS.Mass1 = Q_(10,'kg')
    q.NS.Mass2 = Q_(300,'kg')
    q.NS.Distance = Q_(10,'m')
    with q.add_answer( Answer.Numerical ) as a:
      a.quantity = CalcAnswer
    
  with bank.add_question(copy.deepcopy(q)) as q:
    q.NS.Mass1 = Q_(35,'kg')
    q.answer.NS.__dict__.update( q.NS.__dict__ )

  with bank.add_question(copy.deepcopy(q)) as q:
    q.NS.Mass1 = Q_(500,'kg')
    q.answer.NS.__dict__.update( q.NS.__dict__ )


  test1 = Assignment()
  test2 = Assignment()
  test3 = Assignment()
  test4 = Assignment()

  for q in Actions.PullRandomQuestions(bank, predicate= (has_tag("M1") & has_tag("L1")) ):
    with test1.add_question(q): pass

  for q in Actions.PullRandomQuestions(bank, predicate= (has_tag("M1") | has_tag("L1")) ):
    with test2.add_question(q): pass

  for q in Actions.PullRandomQuestions(bank, num=2, predicate= (has_tag("M1") & has_tag("L1")) ):
    with test3.add_question(q): pass

  for q in Actions.PullRandomQuestions(bank, num=2, predicate= (has_tag("M1") | has_tag("L1")) ):
    with test4.add_question(q): pass


  assert len(test1._questions) == 3
  assert len(test2._questions) == 6
  assert len(test3._questions) == 2
  assert len(test4._questions) == 2


  with pytest.raises(RuntimeError):
    Actions.PullRandomQuestions(bank, num=2, predicate=has_tag("Missing") )




  


  fh = io.StringIO()
  writer = Writers.Simple(fh)
  writer.dump(bank)
  print(fh.getvalue())

  fh = io.StringIO()
  writer = Writers.Simple(fh)
  writer.dump(test1)
  print(fh.getvalue())

  fh = io.StringIO()
  writer = Writers.Simple(fh)
  writer.dump(test2)
  print(fh.getvalue())

  fh = io.StringIO()
  writer = Writers.Simple(fh)
  writer.dump(test3)
  print(fh.getvalue())

  fh = io.StringIO()
  writer = Writers.Simple(fh)
  writer.dump(test4)
  print(fh.getvalue())
