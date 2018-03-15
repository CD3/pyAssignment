import pytest
import pyAssignment.Answer as Answer

def test_Numerical():

  a = Answer.Numerical()

  a.quantity = 1.2
  assert a.quantity == 1.2

  a = Answer.Numerical()
  assert a.quantity is None

  a.NS.x = 2
  a.NS.y = 3

  def calc(x,y):
    return x + y

  a.quantity = calc

  assert a.quantity == 5

  del a.NS.x
  with pytest.raises(RuntimeError):
    assert a.quantity == 5
  
def test_MultipleChoice():

  a = Answer.MultipleChoice()

  a.choices  = "one"
  a.choices += "two"
  a.choices += "three"
  a.choices += "four"
  a.set_correct("three")

  assert len(a._choices) == 4
  assert len(a._correct) == 1
  assert 2 in a._correct



  a = Answer.MultipleChoice()


  a.incorrect += "1"
  a.incorrect += "2"
  a.correct   += "3"
  a.incorrect += "4"

  assert len(a._choices) == 4
  assert len(a._correct) == 1
  assert 2 in a._correct

