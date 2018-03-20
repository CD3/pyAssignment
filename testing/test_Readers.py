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
          answers :
           - text : "the answer"
        - text : q1p2
          answers :
           - choices :
              - first answer
              - second answer
              - ^correct answer
    - text : q2
      answers :
        - quantity : 1.23
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


