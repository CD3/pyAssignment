import pytest
import copy
from pyAssignment.Assignment.Question import Question
from pyAssignment.Assignment.Answers  import Numerical
import pyErrorProp as err

uconv = err.UncertaintyConvention()
units = uconv._UNITREGISTRY
Q_ = units.Quantity
UQ_ = uconv.UncertainQuantity


def test_question_noerror():
  q = Question()

  q.text = "What is the area of a {Length} by {Width} rectangle?"
  q.NS.Length = Q_(10,'cm')
  q.NS.Width  = Q_(20,'cm')

  with q.add_answer(Numerical) as a:
    def CalcAnswer(Length,Width):
      L = Length
      W = Width
      return L*W

    a.quantity = CalcAnswer

    assert a.quantity.magnitude == 200


def test_question_autoerror():
  q = Question()

  q.text = "What is the area of a {Length} by {Width} rectangle?"
  q.NS.Length = Q_(10,'cm')
  q.NS.Width  = Q_(20,'cm')

  with q.add_answer(Numerical) as a:
    @uconv.WithAutoError()
    def CalcAnswer(Length,Width):
      L = Length
      W = Width
      return L*W

    a.quantity = CalcAnswer

    assert a.quantity.nominal.magnitude == 200
    assert a.quantity.error.magnitude > 200*0.01
    assert abs(a.quantity.error.magnitude - 2.236) < 0.001
