from .FilterBase import *
import re

class TagFilter(FilterBase):
  def __init__(self):
    super().__init__()

    self.filter_untagged = True

  def has_tag(self,pattern):
    def imp(q):
      if q.meta.has('tag'):
        tags = q.meta.tag.split(',')
        if len([x for x in tags if re.match(pattern,x)]) > 0:
          return True

      return False


    return imp

  def add_pattern(self,pattern):
    self.predicates.append( self.has_tag(pattern) )
    
    

  def filter(self,ass,tag=None):

    if tag is not None:
      predicates = self.predicates
      self.predicates = [ self.has_tag(tag) ]

    quiz = super().filter(ass)

    if tag is not None:
      self.predicates = predicates

    return quiz
