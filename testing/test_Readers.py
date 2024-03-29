import pytest

import io

from pyassignment.assignment import Assignment
import pyassignment.readers as Readers
import pyassignment.writers as Writers

import yaml,json

def test_reader_base():
  text = '''
  namespace :
    v1 : 1
    v2 : 2

  questions:
    - text : q1
      parts :
        - text : q1p1
          answer :
            text : "the answer"
        - text : q1p2
          answer :
            choices :
              - first answer
              - second answer
              - ^correct answer
    - text : q2
      answer :
         quantity : 1.23
  '''

  data = yaml.load(text,Loader=yaml.SafeLoader)

  fh = io.StringIO()

  reader = Readers.ReaderBase()
  writer = Writers.Simple(fh)

  ass = reader._load_from_dict(data)

  writer.dump(ass)

  assert fh.getvalue() == '''\
NAMESPACE:
v1 = 1
v2 = 2


QUESTIONS:
1. q1
  1. q1p1
    ANS: the answer
  2. q1p2
    ANS: first answer
         second answer
         correct answer (correct)

2. q2
  ANS: 1.23
'''



@pytest.mark.skip(reason="markdown-to-json has not been updated in several years and is using a deprated function call in the standard library.")
def test_markdown_reader():

  text = '''
---
title: Quiz
randomize: true
---

# Questions

1. q1
    1. ^a1
    1. a2
    1. a3
    1. a4
1. q2
    1. a1
    1. ^a2
    1. a3
    1. a4
'''

  fh = io.StringIO()
  ifh = io.StringIO(text)

  reader = Readers.Markdown()
  writer = Writers.Simple(fh)

  ass = reader.load(ifh)

  writer.dump(ass)

  assert fh.getvalue() == '''\
NAMESPACE:


QUESTIONS:
1. q1
  ANS: a1 (correct)
       a2
       a3
       a4

2. q2
  ANS: a1
       a2 (correct)
       a3
       a4

'''

@pytest.mark.skip(reason="markdown-to-json has not been updated in several years and is using a deprated function call in the standard library.")
def test_markdown_reader_exceptions():

  text = '''
# Questions

1. q1
    1. ^a1
    1. a2
1. q2
1. q3
'''

  fh = io.StringIO()
  ifh = io.StringIO(text)

  reader = Readers.Markdown()
  writer = Writers.Simple(fh)

  with pytest.raises(RuntimeError):
    ass = reader.load(ifh)


