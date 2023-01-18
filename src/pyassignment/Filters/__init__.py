from .QuizExtractor import *
from .Predicates import *

from ..Assignment.Assignment import Assignment
import builtins

def filter(predicate, assignment_or_iterable):
  # if an Assignment object is passed in, then we filter
  # to the questions and return a new assignment with
  # those questions
  if isinstance(assignment_or_iterable,Assignment):
    ass = Assignment()
    for q in filter(predicate,assignment_or_iterable._questions):
      with ass.add_question(q): pass
    return ass

  return builtins.filter(predicate, assignment_or_iterable)

