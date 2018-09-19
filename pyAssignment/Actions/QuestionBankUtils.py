
import pyAssignment.Filters as Filters
import random

def PullRandomQuestions( bank, num = None, predicate = None, shuffle = True):
  questions = bank._questions

  if not predicate is None:
    questions = list(filter(predicate, questions))

  if shuffle:
    random.shuffle(questions)

  if num is not None and num > len(questions):
    raise RuntimeError("ERROR: asking for more questions ("+str(num)+") from bank than meet the predicate ("+str(len(questions))+").")

  if num is not None:
    questions = questions[0:num]
  
  return questions


