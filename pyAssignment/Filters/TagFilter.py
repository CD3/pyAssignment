from ..Assignment import *
from .FilterBase import *

class TagFilter(FilterBase):
  def __init__(self):
    super().__init__()

    self.filter_untagged = True


  def filter(self,ass):
    quiz = Assignment()

    for q in ass._questions:
      if q.meta.has('tag'):
        tags = q.meta.tag.split(',')
        if tag in tags:
          with quiz.add_question(q) as qq: pass
      else:
        if not self.filter_untagged:
          with quiz.add_question(q) as qq: pass

    return quiz
