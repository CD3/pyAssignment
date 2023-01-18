import pytest
import pyassignment.Assignment.Answers as Answers

def test_Numerical():

  a = Answers.Numerical()

  a.quantity = 1.2
  assert a.quantity == 1.2

  a = Answers.Numerical()
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
  
def test_MultipleChoice_choices_property():

  a = Answers.MultipleChoice()

  a.choices  = "one"
  a.choices += "two"
  a.choices += "three"
  a.choices += "four"
  a.set_correct("three")

  assert len(a._choices) == 4
  assert len(a._correct) == 1
  assert 2 in a._correct

  assert len(a.choices) == 4
  assert len(list(a.all_formatted_choices)) == 4
  assert len(list(a.correct_formatted_choices)) == 1
  assert len(list(a.incorrect_formatted_choices)) == 3


  a = Answers.MultipleChoice()

  a.choices  = "one"
  a.choices += "two"
  a.choices = "three"
  a.choices += "four"
  a.set_correct("three")

  assert len(a._choices) == 2
  assert len(a._correct) == 1
  assert 0 in a._correct

  assert len(a.choices) == 2
  assert len(list(a.all_formatted_choices)) == 2
  assert len(list(a.correct_formatted_choices)) == 1
  assert len(list(a.incorrect_formatted_choices)) == 1



def test_MultipleChoice_correct_incorrect_properties():
  a = Answers.MultipleChoice()

  a.incorrect = "incorrect"
  a.correct   = "correct"

  assert len(a.choices) == 2
  assert len(list(a.all_formatted_choices)) == 2
  assert len(list(a.correct_formatted_choices)) == 1
  assert len(list(a.incorrect_formatted_choices)) == 1


  a.incorrect += "also incorrect"
  a.correct   += "also correct"

  assert len(a.choices) == 4
  assert len(list(a.all_formatted_choices)) == 4
  assert len(list(a.correct_formatted_choices)) == 2
  assert len(list(a.incorrect_formatted_choices)) == 2


  a = Answers.MultipleChoice()

  a.incorrect += "1"
  a.incorrect += "2"
  a.correct   += "3"
  a.incorrect += "4"

  assert len(a.choices) == 4
  assert len(list(a.all_formatted_choices)) == 4
  assert len(list(a.correct_formatted_choices)) == 1
  assert len(list(a.incorrect_formatted_choices)) == 3






def test_Text():
  
  a = Answers.Text()

  a.text = "the"
  a.text += " answer"

  assert a.text == "the answer"

  def func():
    return "returned answer"

  a.text = func

  assert a.text == "returned answer"
  assert a.formatted_text == "returned answer"

  a.text = "{x} is the answer"
  a.NS.x = 42

  assert a.text == "{x} is the answer"
  assert a.formatted_text == "42 is the answer"
