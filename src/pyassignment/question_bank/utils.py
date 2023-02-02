from .. import filters
import random
import sys
import inspect
import io


def PullRandomQuestions(bank, num=None, predicate=None, shuffle=True):
  questions = bank._questions

  if not predicate is None:
    questions = list(filter(predicate, questions))

  if shuffle:
    random.shuffle(questions)

  if num is not None and num > len(questions):
    raise RuntimeError("ERROR: asking for more questions (" + str(num) +
                       ") from bank than meet the predicate (" +
                       str(len(questions)) + ").")

  if num is not None:
    questions = questions[0:num]

  return questions

def CheckQuestionBank(bank, checks=[], fh=sys.stdout):
  """
  Apply a set of checks to a question bank. Each check is applied to each question in the bank.

  bank: an Assignment object containing questions to check
  checks: a list of callables that return True/False.
          The question being check is passed as the first argument to the check. If the check
          accepts two arguments, a filehandle that can be used by the check to print an error message
          will be passed to the check.
  """
  if not isinstance(checks, list):
    checks = [checks]

  passed = True
  for check in checks:
    check_sig = inspect.signature(check)
    if len(check_sig.parameters) not in [1,2]:
      raise RuntimeError("ERROR: checks pasedd to CheckQuestionBank must take one or two arguments")

    for q in bank._questions:

      try:

        msgfh = io.StringIO()
        if len(check_sig.parameters) == 1:
          passed = check(q)
        if len(check_sig.parameters) == 2:
          passed = check(q,msgfh)

        if not passed:
          passed = False
          fh.write("\n")
          fh.write("A question did not pass a check.\n")
          fh.write("Question: {}\n".format(q))
          fh.write("\tText: {}\n".format(q.formatted_text))
          fh.write("Check: {}\n".format(check))
          fh.write("\tName: {}\n".format(check.__name__))
          fh.write("\tSignature: {}\n".format(inspect.signature(check)))
          fh.write("\tDocString: {}\n".format(inspect.getdoc(check)))
          fh.write("\tMessage: {}\n".format(msgfh.getvalue()))

      except Exception as e:
        passed = False
        fh.write("\n")
        fh.write(
            "An exception was thrown when trying to run a check for a question in the bank\n"
        )
        fh.write("Question: {}\n".format(q))
        fh.write("Check: {}\n".format(check))
        fh.write("Exception: {}\n".format(e))


  return passed

class Checks:
  def has_a_tag(q):
    return len(q.tags) > 0

  def has_answer(q, msgfh):
    '''Check that a question has an answer. If question answer is a MultipleChoice type, then also check that the answer contains choices.'''
    if q._answer is None:
      msgfh.write("Question did not have an answer.")
      return False

    if hasattr(q._answer,'_choices'):
      if len(q._answer._choices) < 1:
        msgfh.write("Multiple choice question did not have any choices.")
        return False

    return True

