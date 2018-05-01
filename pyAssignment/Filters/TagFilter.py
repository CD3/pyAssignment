from .FilterBase import *

class TagFilter(FilterBase):
  def __init__(self):
    super().__init__()

    self.filter_untagged = True

  def has_tag(self,tag):
    def imp(q):
      if q.meta.has('tag'):
        tags = q.meta.tag.split(',')
        if tag in tags:
          return True

      return False


    return imp

  def filter(self,ass,tag=None):

    predicates = self.predicates
    self.predicates = [ self.has_tag(tag) ]

    quiz = super().filter(ass)

    self.predicates = predicates

    return quiz
