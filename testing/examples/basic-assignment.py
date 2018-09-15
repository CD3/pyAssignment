import os,sys
from pyAssignment.Assignment import Assignment
import pyAssignment.Assignment.Answers as Answer
from pyAssignment.Actions import BuildBlackboardAssignment, BuildPDFAssignment
import pint

units = pint.UnitRegistry()
Q_ = units.Quantity

ass = Assignment()
ass.meta.title = r'Basic Assignment'

with ass.add_question() as q:
  q.text = r'''Calculate the weight of a 20 kg mass.'''
  with q.add_answer(Answer.Numerical) as a:
    a.quantity = (Q_(20,'kg')*Q_(9.8,'m/s^2')).to('N')

with ass.add_question() as q:
  with q.add_figure() as f:
    f.filename = "image.png"
  q.text = r'''What color is the image?'''
  with q.add_answer(Answer.MultipleChoice) as a:
    a.correct += "orange"
    a.incorrect += "purple"

  with q.add_part() as p:
    p.text = r'''What shape is the image?'''
    with p.add_answer(Answer.MultipleChoice) as a:
      a.correct += "circle"
      a.incorrect += "rectangle"



basename = os.path.basename(__file__).replace(".py","")
BuildBlackboardAssignment(ass,basename)
BuildPDFAssignment(ass,basename)
