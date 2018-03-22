from ..Assignment import *
from .FilterBase import *

class QuizExtractor(FilterBase):
  def __init__(self):
    super().__init__()

  def filter(self,ass):

    quiz = Assignment()
    for q in ass._questions:
      for sq in q._questions:
        with quiz.add_question(sq) as qq:
          if not qq.meta.has('parent_uuid'):
            qq.meta.parent_uuid = None
            if q.meta.has('uuid'):
              qq.meta.parent_uuid = q.meta.uuid

    return quiz
