from ..Assignment import *

class FilterBase(object):
  def __init__(self):
    self.predicates = list()

  def filter(self,ass):
    quiz = Assignment()

    for q in ass._questions:
      for p in self.predicates:
        if p(q):
          with quiz.add_question(q) as qq: pass

    return quiz

