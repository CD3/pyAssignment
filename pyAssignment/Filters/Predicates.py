from functools import update_wrapper
import re


class Predicate(object):
    """A Predicate class that represents combining predicates with & and |"""
    def __init__(self, predicate):
        self.pred = predicate

    def __call__(self, obj):
        return self.pred(obj)

    def __copy_pred(self):
        return copy.copy(self.pred)

    def __and__(self, predicate):
        def func(obj):
            return self.pred(obj) and predicate(obj)
        return Predicate(func)

    def __or__(self, predicate):
        def func(obj):
            return self.pred(obj) or predicate(obj)
        return Predicate(func)


def predicate(func):
  '''Decorator for making Predicates.'''
  result = Predicate(func)
  update_wrapper(result, func)
  return result

def has_tag(tag):
    def has_tag(q):
      '''Return true if question has a specific tag.'''

      return tag in q.tags

    p = Predicate(has_tag)
    update_wrapper(p,has_tag)
    return p

def has_matching_tag(pattern):
    def has_matching_tag(q):
      '''Return true if question has a tag matching a pattern.'''
      for tag in q.tags:
        if re.match(pattern,tag):
          return True
      return False

    p = Predicate(has_matching_tag)
    update_wrapper(p,has_matching_tag)
    return p
