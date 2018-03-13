import pytest
from pyAssignment.Question import Question
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
