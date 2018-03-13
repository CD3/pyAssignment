import pytest
from pyAssignment.Assignment import Assignment

def test_demo():

  ass = Assignment()

  with ass.add_question() as q:
    q.text = '''
    Compute the gravitational force exerted on a {Mass1} object by:
    '''
    q.NS.Mass1 = 1.2

    with q.add_part() as p:
      p.text = '''
      Earth.
      '''

    with q.add_part() as p:
      p.text = '''
      A {Mass2} object placed {Distance} away.
      '''

      p.NS.Mass2 = 2.3



