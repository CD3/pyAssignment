from ..assignment import *

class QuizExtractor:
  def __init__(self):
    pass

  def filter(self,ass):

    quiz = Assignment()
    for q in ass._questions: # loop through assignment questions
      for sq in q._questions: # loop throgh quiz questions
        with quiz.add_question(sq) as qq:
          if not qq.meta.has('parent_uuid'):
            qq.meta.parent_uuid = None
            if q.meta.has('uuid'):
              qq.meta.parent_uuid = q.meta.uuid

      for p in q._parts: # loop through question's parts
        for sq in p._questions: # loop through quiz questions
          with quiz.add_question(sq) as qq:
            if not qq.meta.has('parent_uuid'):
              qq.meta.parent_uuid = None
              if p.meta.has('uuid'):
                qq.meta.parent_uuid = p.meta.uuid

    return quiz
