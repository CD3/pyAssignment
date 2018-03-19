import pytest

import io

from pyAssignment.Assignment import Assignment
import pyAssignment.Readers as Readers
import pyAssignment.Writers as Writers

import yaml

def test_reader_base():

  text = '''
  namespace :
    v1 : 1
    v2 : 1

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
  print(data)

  fh = io.StringIO()

  reader = Readers.ReaderBase()
  writer = Writers.Simple(fh)

  ass = reader._load_from_dict(data)

  writer.dump(ass)

  print()
  print(fh.getvalue())



def test_json():
  pass

def test_yaml()
  pass

def test_markdown()
