import pytest
import copy
from pyassignment.assignment.question import Question
from pyassignment.assignment.answers  import MultipleChoice
# from .Utils import Approx

def test_adding_text():
  q = Question()

  q.text = "Th"
  q.text += "is"
  q.text += " is"
  q.text += " a question."

  assert q._text == "This is a question."

def test_namespace():
  q = Question()

  q.NS.a = "A"
  q.NS.b = "B"
  q.NS.one = 1
  q.NS.two = 2.0

  assert q.NS.a == "A"
  assert q.NS.b == "B"
  assert q.NS.one == 1
  assert q.NS.two == 2.0

  assert len(q.NS) == 4

  assert q.NS.has('a')
  del q.NS.a
  assert not q.NS.has('a')
  with pytest.raises(AttributeError):
    a = q.NS.a


  q.NS.f = lambda x : x*x + 2

  assert q.NS.f(1) == 3
  assert q.NS.f(2) == 6

  q.NS.clear()
  assert not q.NS.has('b')
  assert not q.NS.has('one')
  assert len(q.NS) == 0

def test_metadata():
  q = Question()

  q.meta.desc = "a question"
  q.meta.mod = 1
  q.meta.tags = "electric force;vectors"


def test_parts():
  q = Question()
  q.text = "main question."
  with q.add_part() as p:
    p.text = "part of question."

  assert q._text == "main question."
  assert len(q._parts) == 1
  assert q._parts[0]._text == "part of question."

  q = Question()
  q.NS.var1 = 1.1
  assert q.NS.var1 == 1.1
  with q.add_part() as p:
    p.NS.var2 = 2.2
    assert p.NS.var2 == 2.2
    assert q.NS.var1 == 1.1
    assert p.NS.var1 == 1.1
    assert not q.NS.has('var2')


def test_questions():
  q = Question()
  q.text = "main question."
  with q.add_question() as qq:
    qq.text = "quiz question."

  assert q._text == "main question."
  assert len(q._questions) == 1
  assert q._questions[0]._text == "quiz question."

  q = Question()
  q.NS.var1 = 1.1
  assert q.NS.var1 == 1.1
  with q.add_question() as qq:
    qq.NS.var2 = 2.2
    assert qq.NS.var2 == 2.2
    assert q.NS.var1 == 1.1
    assert qq.NS.var1 == 1.1
    assert not q.NS.has('var2')

def test_formatting_text():
  q = Question()

  q.text += "{Length}"
  q.NS.Length = 10

  assert q.text == "{Length}"
  assert q.formatted_text == "10"

def test_text():
  q = Question()

  q.text = ''' \
  setting text.
  '''
  assert q.text == "setting text.\n"

  q.text = '''\
  setting text.
  adding text.
  '''
  assert q.text == "setting text.\nadding text.\n"

  q.text = '''\
  setting text.
  '''
  assert q.text == "setting text.\n"
  q.text += 'adding text.'
  assert q.text == "setting text.\nadding text."

  with q.disable_linter:
    q.text = '''
    setting text.
    '''
  assert q.text == "\n    setting text.\n    "

def test_adding_answer():
  q = Question()
  with q.add_answer(MultipleChoice) as a:
    a.correct += "c1"
    a.incorrect += "i1"

  assert type(q._answer) == MultipleChoice
  assert type(q.answer) == MultipleChoice
  assert len(q.answer.choices) == 2
  assert q.answer.choices[0] == "c1"
  assert q.answer.choices[1] == "i1"

  a = MultipleChoice()
  a.correct = 'correct'
  a.incorrect += 'incorrect 1'
  a.incorrect += 'incorrect 2'

  q.answer = a

  assert type(q.answer) == MultipleChoice
  assert len(q.answer.choices) == 3
  assert q.answer.choices[0] == "correct"
  assert q.answer.choices[1] == "incorrect 1"
  assert q.answer.choices[2] == "incorrect 2"


def test_copying():
  q = Question()
  q.text = "question 1"

  with q.add_answer(MultipleChoice) as a:
    a.correct   += "correct answer"
    a.incorrect += "incorrect answer"

  q2 = copy.deepcopy(q)

  q2.text = q.text.replace('1','2')
  q2.answer.correct = "the correct answer"

  assert q.text == "question 1"
  assert len(list(q.answer.all_formatted_choices)) == 2
  assert "correct answer" in list(q.answer.all_formatted_choices)
  assert "incorrect answer" in list(q.answer.all_formatted_choices)

  assert q2.text == "question 2"
  assert len(list(q2.answer.all_formatted_choices)) == 2
  assert "the correct answer" in list(q2.answer.all_formatted_choices)
  assert "incorrect answer" in list(q2.answer.all_formatted_choices)

  q2.answer.incorrect = "the incorrect answer"
  assert len(list(q2.answer.all_formatted_choices)) == 2
  assert "the correct answer" in list(q2.answer.all_formatted_choices)
  assert "the incorrect answer" in list(q2.answer.all_formatted_choices)
