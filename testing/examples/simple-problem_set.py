import os,sys
from pyAssignment.Assignment import Assignment
import pyAssignment.Assignment.Answers as Answer
from pyAssignment.Actions import BuildProblemSetAndBlackboardQuiz
import pint

units = pint.UnitRegistry()
Q_ = units.Quantity

ass = Assignment()
ass.meta.title = r'Simple Assignment'

with ass.add_question() as q:
  q.text = r'''Calculate the weight of a 20 kg mass.'''

  with q.add_question() as qq:
    qq.text = r'''What is the mass?'''
    with qq.add_answer(Answer.Numerical) as a:
      a.quantity = (Q_(20,'kg')*Q_(9.8,'m/s^2')).to('N')


basename = os.path.basename(__file__).replace(".py","")
BuildProblemSetAndBlackboardQuiz(ass,basename)
