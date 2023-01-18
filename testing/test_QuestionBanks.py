import pytest

import io,os,shutil,copy

from pyassignment.Assignment import Assignment
import pyassignment.Assignment.Answers as Answer
import pyassignment.Writers as Writers
from pyassignment.Filters.Predicates import has_tag
from pyassignment.QuestionBank.Utils import Checks,PullRandomQuestions,CheckQuestionBank

import pint
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

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

  for q in PullRandomQuestions(bank, predicate= (has_tag("M1") & has_tag("L1")) ):
    with test1.add_question(q): pass

  for q in PullRandomQuestions(bank, predicate= (has_tag("M1") | has_tag("L1")) ):
    with test2.add_question(q): pass

  for q in PullRandomQuestions(bank, num=2, predicate= (has_tag("M1") & has_tag("L1")) ):
    with test3.add_question(q): pass

  for q in PullRandomQuestions(bank, num=2, predicate= (has_tag("M1") | has_tag("L1")) ):
    with test4.add_question(q): pass


  assert len(test1._questions) == 3
  assert len(test2._questions) == 6
  assert len(test3._questions) == 2
  assert len(test4._questions) == 2


  with pytest.raises(RuntimeError):
    PullRandomQuestions(bank, num=2, predicate=has_tag("Missing") )



  assert CheckQuestionBank(bank, Checks.has_a_tag)
  assert CheckQuestionBank(bank, has_tag("M1"))
  assert not CheckQuestionBank(bank, has_tag("M2"))

  assert CheckQuestionBank(bank, Checks.has_answer)


  with bank.add_question() as q:
    q.text = "None"
  
  assert not CheckQuestionBank(bank, Checks.has_answer)

  del bank._questions[-1]
  assert CheckQuestionBank(bank, Checks.has_answer)

  with bank.add_question() as q:
    q.text = "None"
    with q.add_answer(Answer.MultipleChoice) as a:
      pass


  assert not CheckQuestionBank(bank, Checks.has_answer)


  del bank._questions[-1]
  assert CheckQuestionBank(bank, Checks.has_answer)

  with bank.add_question() as q:
    q.text = "None"
    with q.add_answer(Answer.MultipleChoice) as a:
      a.correct += "A"


  assert CheckQuestionBank(bank, Checks.has_answer)
