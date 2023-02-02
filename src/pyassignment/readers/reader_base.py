from ..assignment import *
from ..assignment.answers import *

import io

class ReaderBase(object):
  def __init__(self,fh=None):
    self.fh = fh

  def get_fh(self,fh=None):
    if fh is None:
      fh = self.fh
    if fh is None:
      raise(RuntimeError("No filehandle available."))
    return fh

  def _load_from_dict(self,d,ass=None):
    '''
    Creates an assignment from a python dictionary.
    This can be used as the "backend" for many different readers:
    if a reader can get data into a python dictionary, then
    it can pass the dictionary off to this function to generate
    a pyassignment.Assignment instance.

    dict format:

    { 'namespace' : { 'var1' : val1, ...}
    , 'questions' [
        'text' : 'question text',
        'answer' : { See below }
        'parts' : [ See below ]
    ]
    }
    '''
    if ass is None:
      ass = Assignment()

    self._load_namespace_from_dict(d,ass)
    self._load_questions_and_parts_from_dict(d,ass)

    return ass

  def _load_namespace_from_dict(self,d,obj):
    '''Load dictionary into namespace of obj'''
    ns = d.get('namespace',dict())
    for k in ns:
      setattr(obj.NS,k,ns[k])

  def _load_questions_and_parts_from_dict(self,d,obj):

    for e in d.get('questions',list()):
      with obj.add_question() as q:
        self._load_question_from_dict(e,q)

    for e in d.get('parts',list()):
      with obj.add_part() as p:
        self._load_question_from_dict(e,p)

  def _load_question_from_dict(self,d,obj):
    obj.text = d['text']

    self._load_answer_from_dict( d, obj)
    self._load_questions_and_parts_from_dict( d, obj )

  def _load_answer_from_dict(self,d,obj):
    e = d.get('answer',None)
    if e is not None:
      with obj.add_answer(self._get_answer_type(e)) as a:
        if isinstance(a,Numerical):
          a.quantity = e['quantity']

        if isinstance(a,Text):
          a.text = e['text']

        if isinstance(a,MultipleChoice):
          for choice in e['choices']:
            if choice.startswith('^'):
              a.correct += choice[1:]
            else:
              a.incorrect += choice

  def _get_answer_type(self,d):
    if "quantity" in d:
      return Numerical
    if "choices" in d:
      return MultipleChoice
    if "text" in d:
      return Text

    return None

