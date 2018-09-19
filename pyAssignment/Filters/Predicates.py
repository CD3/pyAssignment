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

@predicate
def has_tag(tag):
    def imp(q):
      return tag in q.tags

    return imp

def has_matching_tag(pattern):
    def imp(q):
      for tag in q.tags:
        if re.match(pattern,tag):
          return True
      return False

    return imp
