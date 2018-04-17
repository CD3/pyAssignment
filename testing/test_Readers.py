import pytest

import io

from pyAssignment.Assignment import Assignment
import pyAssignment.Readers as Readers
import pyAssignment.Writers as Writers

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

  data = yaml.load(text)

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



def test_markdown_reader():

  text = '''
# Configuration

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
